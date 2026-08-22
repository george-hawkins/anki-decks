#!/usr/bin/env python3
"""Mechanical health check for the RTK deck file (rtk1-v6.md).

Usage:
    uv run --python 3.14 check.py [SCOPE ...] [OPTIONS]

Scope (default: every card; file-wide checks always cover the whole file):
    --range A-B      cards A to B by position in the file (1-based, inclusive)
    --last N         the last N cards in the file
    --card N         a single card by position (repeatable)
    --kanji 硝       cards whose Kanji field is one of these characters
    --keyword nitrate  cards whose Keyword matches (case/hyphen insensitive)
    --recent         cards touched by the working-tree diff of the deck, or,
                     if the tree is clean, by the most recent commit

Options:
    --deck PATH      deck file (default: rtk1-v6.md found in or above cwd)
    --dump           after the report, print every in-scope card verbatim
                     (feed the judgment pass without a separate read)
    --vocab          add the noisy "novel component vocabulary" check
    --no-spell       skip the spell check
    --wordlist PATH  extra vocabulary (default: wordlist.txt beside this script)
    --suppressions PATH  already-reported store (default: reported.tsv beside
                     this script); entries silence a finding until the text
                     they quote changes, and stale ones are deleted on sight
    --no-prune       report stale store entries instead of deleting them

Findings are grouped ERROR (breaks Anki import or deck invariants), WARN
(almost certainly a mistake) and INFO (worth an eyeball, often deliberate).
Every finding carries a check code, the card's position, a line number and the
card's kanji/keyword. The deck is never modified; the only file this script
writes is the suppression store.
"""

import argparse
import difflib
import re
import shutil
import subprocess
import sys
import unicodedata
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path

DECK = "rtk1-v6.md"
NOTETYPE = "Japanese RTK"
HEADER_RE = re.compile(r"^TARGET DECK: .+$")
FIELD_RE = re.compile(r"^([A-Z][A-Za-z ]*):(.*)$")
ID_RE = re.compile(r"^<!--ID: *(\d+)-->$")
REQUIRED = ("Keyword", "Clue", "Kanji", "Story", "Note")
# Update is optional and, like Note, holds free prose — a later second thought
# about the card kept apart from the Note itself.
OPTIONAL = ("Update",)
FIELDS = REQUIRED + OPTIONAL
PROSE = ("Note", "Update")
NO_STORY_RE = re.compile(r"^\[no story(?:\s*[-–—:]?\s+[^\]]+)?\]$")
# a full emphasis span: **bold**, _italic_ or *italic*
BOLD_RE = re.compile(r"\*\*([^*\n]*)\*\*")
ITALIC_RE = re.compile(r"(?<![*\w])(?:_([^_\n]*)_|\*([^*\n]*)\*)(?![*\w])")
CJK_RE = re.compile(r"[㐀-䶿一-鿿豈-﫿]")
# hiragana, katakana and the iteration marks that ride along with them
KANA_RE = re.compile(r"[々〆〻ぁ-ゟ゠-ヿｦ-ﾟ]")
STOPWORDS = {
    "a", "an", "and", "as", "at", "be", "by", "for", "from", "in", "into", "is",
    "it", "its", "of", "off", "on", "one", "or", "s", "the", "to", "up", "with",
}
SEVERITIES = ("ERROR", "WARN", "INFO")


# ---------------------------------------------------------------- data model

@dataclass
class Card:
    index: int  # 1-based position in the file
    start: int  # line number of START
    end: int = 0  # line number of END
    notetype: str | None = None
    fields: dict[str, str] = field(default_factory=dict)
    field_lines: dict[str, int] = field(default_factory=dict)
    order: list[str] = field(default_factory=list)  # every label, dupes kept
    continuations: dict[str, list[int]] = field(default_factory=dict)
    ids: list[tuple[int, int]] = field(default_factory=list)  # (line, value)
    id_last: bool = False
    raw: str = ""  # the card's text, for suppression snippets

    @property
    def keyword(self) -> str:
        return self.fields.get("Keyword", "").strip()

    @property
    def kanji(self) -> str:
        return self.fields.get("Kanji", "").strip()

    @property
    def story(self) -> str:
        return self.fields.get("Story", "").strip()

    @property
    def note(self) -> str:
        return self.fields.get("Note", "").strip()

    def line(self, name: str) -> int:
        return self.field_lines.get(name, self.start)

    def label(self) -> str:
        return f"#{self.index} L{self.start} {self.kanji or '?'} [{self.keyword or '?'}]"


@dataclass
class Finding:
    severity: str
    code: str
    where: str  # card label, or "L<line>" for file-wide findings
    message: str
    sort_line: int
    card_index: int | None = None
    kanji: str = ""
    detail: str = ""


class Report:
    def __init__(self) -> None:
        self.findings: list[Finding] = []

    def add(self, severity, code, target, message, detail="") -> None:
        if isinstance(target, Card):
            where, line, index, kanji = target.label(), target.start, target.index, target.kanji
        else:
            where, line, index, kanji = f"L{target}", int(target), None, ""
        self.findings.append(
            Finding(severity, code, where, message, line, index, kanji, detail))

    def restrict(self, scope: set[int]) -> None:
        """Drop findings about cards outside the scope (parsing runs first, so
        some are collected before the scope is known)."""
        self.findings = [f for f in self.findings
                         if f.card_index is None or f.card_index in scope]

    def error(self, *a, **kw):
        self.add("ERROR", *a, **kw)

    def warn(self, *a, **kw):
        self.add("WARN", *a, **kw)

    def info(self, *a, **kw):
        self.add("INFO", *a, **kw)


# ------------------------------------------------------------------ parsing

def find_file(name: str, required: bool = True) -> Path | None:
    here = Path(__file__).resolve().parent
    for base in [Path.cwd(), *Path.cwd().parents, here, *here.parents]:
        candidate = base / name
        if candidate.is_file():
            return candidate
    if required:
        sys.exit(f"error: {name} not found in or above {Path.cwd()}")
    return None


def parse(lines: list[str], report: Report) -> list[Card]:
    """Split the file into cards, reporting anything structurally broken."""
    cards: list[Card] = []
    card: Card | None = None
    last_field: str | None = None
    seen_header = False

    for lineno, raw in enumerate(lines, 1):
        text = raw.strip()
        if text == "START":
            if card is not None:
                report.error("F003", card.start, "START at L%d never reached an END" % card.start)
                cards.append(card)
            card = Card(index=len(cards) + 1, start=lineno)
            last_field = None
            continue
        if text == "END":
            if card is None:
                report.error("F003", lineno, "END with no matching START")
                continue
            card.end = lineno
            card.raw = "\n".join(lines[card.start:lineno - 1])
            cards.append(card)
            card, last_field = None, None
            continue

        if card is None:
            if not text:
                continue
            if HEADER_RE.match(text) and not seen_header:
                seen_header = True
                if lineno != 1:
                    report.info("F001", lineno, "TARGET DECK header is not the first line")
            elif text.startswith("<!--"):
                report.info("F002", lineno, "free-standing comment outside any card — invisible "
                                            f"to Anki, fine as a scratch note: {text[:50]!r}")
            else:
                report.error("F002", lineno, f"text outside any card: {text[:60]!r}")
            continue

        # inside a card
        if not text:
            report.warn("F006", card, f"blank line inside the card (L{lineno})")
            continue
        if text == NOTETYPE:
            if card.notetype is None and not card.fields:
                card.notetype = text
            else:
                report.warn("C001", card, f"stray {NOTETYPE!r} line at L{lineno}")
            continue
        if text.startswith("<!--"):
            m = ID_RE.match(text)
            if m:
                card.ids.append((lineno, int(m.group(1))))
                card.id_last = True
            else:
                report.warn("C006", card, f"malformed ID comment at L{lineno}: {text[:60]!r}")
            continue

        m = FIELD_RE.match(raw)
        if m and m.group(1) in FIELDS:
            name = m.group(1)
            card.order.append(name)
            card.id_last = False
            if name in card.fields:
                report.error("C003", card, f"duplicate {name}: field at L{lineno} "
                                           f"(first at L{card.field_lines[name]})")
                card.fields[name] += "\n" + m.group(2).strip()
            else:
                card.fields[name] = m.group(2).strip()
                card.field_lines[name] = lineno
            last_field = name
        elif m:
            report.warn("C005", card, f"unknown field label {m.group(1)!r}: at L{lineno} — "
                                      "Anki only imports the note type's fields; make this a "
                                      "continuation line of Note instead")
            card.order.append(m.group(1))
            card.id_last = False
            last_field = "Note" if "Note" in card.fields else last_field
            if last_field:
                card.fields[last_field] += "\n" + text
        elif last_field:
            card.fields[last_field] += "\n" + text
            card.continuations.setdefault(last_field, []).append(lineno)
            card.id_last = False
        else:
            report.error("C009", card, f"unexpected line before any field at L{lineno}: {text[:60]!r}")

    if card is not None:
        report.error("F003", card.start, f"START at L{card.start} never reached an END")
        cards.append(card)
    if not seen_header:
        report.error("F001", 1, "no 'TARGET DECK: ...' header line")
    return cards


# ------------------------------------------------- text / keyword utilities

IRREGULAR = {
    "men": "man", "women": "woman", "children": "child", "teeth": "tooth",
    "feet": "foot", "geese": "goose", "mice": "mouse", "lice": "louse",
    "people": "person", "leaves": "leaf", "shelves": "shelf", "wolves": "wolf",
    "knives": "knife", "thieves": "thief", "lives": "life", "wives": "wife",
    "loaves": "loaf", "built": "build", "held": "hold", "sold": "sell",
    "told": "tell", "fell": "fall", "fallen": "fall", "sat": "sit",
    "stood": "stand", "took": "take", "taken": "take", "gave": "give",
    "given": "give", "went": "go", "gone": "go", "made": "make",
    "became": "become", "broke": "break", "broken": "break", "caught": "catch",
    "brought": "bring", "bought": "buy", "taught": "teach", "thought": "think",
    "fought": "fight", "sought": "seek", "found": "find", "left": "leave",
    "lost": "lose", "meant": "mean", "met": "meet", "paid": "pay", "put": "put",
    "read": "read", "ran": "run", "said": "say", "saw": "see", "seen": "see",
    "sent": "send", "shot": "shoot", "spent": "spend", "struck": "strike",
    "swore": "swear", "wore": "wear", "worn": "wear", "written": "write",
    "wrote": "write", "drew": "draw", "drawn": "draw", "grew": "grow",
    "grown": "grow", "knew": "know", "known": "know", "threw": "throw",
    "thrown": "throw", "ate": "eat", "eaten": "eat", "flew": "fly",
    "flown": "fly", "rose": "rise", "risen": "rise", "chose": "choose",
    "chosen": "choose", "spoke": "speak", "spoken": "speak", "hung": "hang",
    "dug": "dig", "stuck": "stick", "sank": "sink", "sung": "sing",
    "sang": "sing", "drank": "drink", "drunk": "drink", "sprang": "spring",
    "sprung": "spring", "halves": "half", "calves": "calf", "elves": "elf",
    "selves": "self", "hooves": "hoof", "scarves": "scarf",
}
SUFFIXES = (
    ("ies", "y"), ("ied", "y"), ("iest", "y"), ("ier", "y"),
    ("ing", ""), ("ings", ""), ("ers", ""), ("est", ""),
    ("ed", ""), ("es", ""), ("er", ""), ("ly", ""), ("s", ""),
)
# surface-level inflections that still count as "the same word" (strict checks)
SAME_WORD_SUFFIXES = ("s", "es", "'s", "’s", "s'")


def stem(word: str) -> str:
    """Crude but generous stemmer — good enough to match inflections."""
    word = word.lower().strip("'’")
    if word in IRREGULAR:
        return IRREGULAR[word]
    for suffix, replacement in SUFFIXES:
        if word.endswith(suffix) and len(word) - len(suffix) >= 3:
            return (word[: -len(suffix)] + replacement).rstrip("'’")
    return word


LETTER = r"[A-Za-zÀ-ÖØ-öø-ÿĀ-ſ]"
WORD_RE = re.compile(rf"{LETTER}+(?:['’]{LETTER}+)*")


def words_of(text: str) -> list[str]:
    return WORD_RE.findall(text)


def content_stems(text: str) -> list[str]:
    """Stems worth matching on: stopwords dropped, unless that leaves nothing
    (keywords like 'in' and 'one' are themselves stopwords)."""
    stems = [stem(w) for w in words_of(text)]
    return [s for s in stems if s not in STOPWORDS] or stems


def loose_match(a: str, b: str) -> bool:
    """Do two stems plausibly denote the same word? (build/built, risk/risky)

    Deliberately generous: it decides whether the *bolded* text counts as the
    keyword, where a false accusation is worse than a miss.
    """
    if a == b:
        return True
    short, long = sorted((a, b), key=len)
    if len(short) >= 3 and long.startswith(short):
        return True  # risk/risky, inter-/interfaith, cross/crossing
    if len(short) <= 4:
        return False
    n = max(4, len(short) - 2)
    return a[:n] == b[:n]  # intimidate/intimidation, plane/planed


def same_word(a: str, b: str) -> bool:
    """Strict: are these two surface forms of one word? (utensil/utensils)

    Used where a hit is an accusation — deriving one word from another
    (fish → fishing, grave → graveyard) does not count.
    """
    a, b = a.lower().strip("'’"), b.lower().strip("'’")
    if a == b:
        return True
    if IRREGULAR.get(a) == b or IRREGULAR.get(b) == a:
        return True
    short, long = sorted((a, b), key=len)
    return any(long == short + suffix for suffix in SAME_WORD_SUFFIXES)


def phrase_occurs(words: list[str], keyword: str) -> bool:
    """Does the keyword itself (not a relative of it) occur in these words?"""
    targets = [w for w in words_of(keyword) if stem(w) not in STOPWORDS] or words_of(keyword)
    if not targets:
        return False
    for i, word in enumerate(words):
        if not same_word(targets[0], word):
            continue
        window = words[i:i + len(targets) + 3]
        if all(any(same_word(t, w) for w in window) for t in targets):
            return True
    return False


def keyword_in(text: str, keyword: str) -> bool:
    """Does `text` contain the keyword, allowing inflection and partial hits?

    A multi-word keyword only needs one of its content words to show up: the
    deck legitimately bolds **Judas** for 'japanese judas-tree'.
    """
    return any(loose_match(t, h) for t in content_stems(keyword)
               for h in content_stems(text))


def normalize_keyword(text: str) -> str:
    text = unicodedata.normalize("NFKC", text).lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    return " ".join(re.split(r"[\s\-]+", text)).strip()


def spans(text: str) -> tuple[list[str], list[str]]:
    """(bold spans, italic spans) — italic covers both _x_ and *x*."""
    bold = BOLD_RE.findall(text)
    without_bold = BOLD_RE.sub(lambda m: " " * len(m.group(0)), text)
    italic = [m.group(1) if m.group(1) is not None else m.group(2)
              for m in ITALIC_RE.finditer(without_bold)]
    return bold, italic


def unmarked_text(text: str) -> str:
    """The story with every emphasis span blanked out."""
    text = BOLD_RE.sub(lambda m: " " * len(m.group(0)), text)
    return ITALIC_RE.sub(lambda m: " " * len(m.group(0)), text)


# ----------------------------------------------------- extra vocabulary file

SPELL_EXTRA: set[str] = set()  # wordlist.txt, also used to spot proper nouns


def load_wordlist(path: Path | None) -> set[str]:
    words: set[str] = set()
    if path is None:
        return words
    if not path.is_file():
        print(f"warning: no extra wordlist at {path}", file=sys.stderr)
        return words
    for line in path.read_text(encoding="utf-8").splitlines():
        word = line.split("#", 1)[0].strip().lower()
        if word:
            words.add(word)
            words.add(stem(word))
    return words


# ------------------------------------------------------ already-reported store

@dataclass
class Suppression:
    kanji: str
    code: str  # a check code, or "-" for a judgment-pass finding
    snippet: str  # text that must still be in the card for this to apply
    summary: str
    live: bool = False  # snippet still present → the finding still stands
    known_card: bool = False

    def line(self) -> str:
        return "\t".join((self.kanji, self.code, self.snippet, self.summary))


def load_suppressions(path: Path) -> list[Suppression]:
    entries = []
    if not path.is_file():
        return entries
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        parts = raw.split("\t")
        if len(parts) < 3:
            print(f"warning: ignoring malformed line in {path.name}: {raw!r}", file=sys.stderr)
            continue
        kanji, code, snippet, *rest = parts
        entries.append(Suppression(kanji.strip(), code.strip() or "-", snippet,
                                   rest[0].strip() if rest else ""))
    return entries


SUPPRESSION_HEADER = """\
# Findings already reported and left alone — the caretaker stays quiet about
# these on later runs. One per line, tab separated:
#
#   <kanji> <TAB> <check code or -> <TAB> <snippet> <TAB> why it was reported
#
# <snippet> is text that must still appear in the card for the entry to apply.
# When the card changes so the snippet is gone, the advice was evidently taken
# and check.py drops the entry automatically (--no-prune to keep it).
"""


def apply_suppressions(entries: list[Suppression], cards: list[Card],
                       report: Report) -> list[Suppression]:
    """Mark entries live/stale and drop the findings they cover."""
    by_kanji: dict[str, list[Card]] = defaultdict(list)
    for card in cards:
        by_kanji[card.kanji].append(card)
    for entry in entries:
        matches = by_kanji.get(entry.kanji, [])
        entry.known_card = bool(matches)
        entry.live = any(entry.snippet in card.raw for card in matches)
    live_codes = {(e.kanji, e.code) for e in entries if e.live and e.code != "-"}
    report.findings = [f for f in report.findings
                       if (f.kanji, f.code) not in live_codes]
    return entries


# -------------------------------------------------------------- spell check

class Speller:
    """aspell, plus wordlist.txt and the deck's own keywords as extra vocabulary.

    aspell is required rather than optional: the alternatives on macOS (web2 is
    Webster's 1913) miss so much ordinary English that the report drowns in
    false positives.
    """

    MIN_LENGTH = 3  # 'ri', 'th' and friends are never worth flagging
    MACRON = re.compile(r"[āīūēōĀĪŪĒŌ]")  # romaji (chūjun, jōyō), not English
    ELIDED = re.compile(r"\w*\.{2,}\w*")  # f...ing barking mouth

    def __init__(self, extra: set[str], keywords: list[str]) -> None:
        self.extra = set(extra)
        self.backend = "aspell"
        for keyword in keywords:  # Heisig's keywords are vocabulary by fiat
            for word in words_of(keyword):
                self.extra.add(word.lower())
                self.extra.add(stem(word))
        self.aspell = shutil.which("aspell")
        if not self.aspell:
            sys.exit("error: aspell not found on PATH. Install it (brew install aspell) "
                     "or re-run with --no-spell.")

    def tokens_of(self, text: str) -> set[str]:
        text = self.ELIDED.sub(" ", re.sub(r"[*_]", "", text))
        return {t for t in words_of(text)
                if len(t) >= self.MIN_LENGTH and not self.MACRON.search(t)}

    def unknown(self, texts: list[str]) -> set[str]:
        tokens = {t for text in texts for t in self.tokens_of(text)}
        return {t for t in self._aspell(tokens) if not self._allowed(t)}

    def _aspell(self, tokens: set[str]) -> set[str]:
        if not tokens:
            return set()
        try:
            out = subprocess.run(
                [self.aspell, "list", "--lang=en", "--encoding=utf-8"],
                input="\n".join(sorted(tokens)), capture_output=True, text=True,
                timeout=60, check=True,
            )
        except (OSError, subprocess.SubprocessError) as exc:
            sys.exit(f"error: aspell failed ({exc}); re-run with --no-spell to skip spelling")
        return {w.strip() for w in out.stdout.splitlines() if w.strip()}

    def _allowed(self, token: str) -> bool:
        base = token.lower()
        head = base.split("'", 1)[0]
        candidates = {base, stem(base), head, stem(head)}
        if base.endswith("n't"):
            candidates.add(base[:-3])
        return bool(candidates & self.extra)


# ------------------------------------------------------------------- checks

def check_file(lines: list[str], cards: list[Card], report: Report) -> None:
    for lineno, raw in enumerate(lines, 1):
        if raw.rstrip("\n") != raw.rstrip():
            report.info("F005", lineno, "trailing whitespace")
        if "\t" in raw:
            report.info("F005", lineno, "tab character")
        if " " in raw:
            report.warn("F005", lineno, "non-breaking space")

    for card in cards[1:]:
        previous = cards[card.index - 2]
        gap = [lines[i - 1].strip() for i in range(previous.end + 1, card.start)]
        if gap != [""] and all(not line for line in gap):
            report.info("F004", card, f"{len(gap)} blank lines before this card's START "
                                      "(the file otherwise uses exactly one)")


def check_structure(cards: list[Card], scope: set[int], report: Report) -> None:
    ids: dict[int, Card] = {}
    previous_id = 0
    for card in cards:
        in_scope = card.index in scope
        for lineno, value in card.ids:  # the ID map must span the whole deck
            if value in ids and (in_scope or ids[value].index in scope):
                report.error("C007", card, f"ID {value} is also used by card "
                                           f"{ids[value].label()} — Anki would treat them as "
                                           "the same note")
            ids.setdefault(value, card)
            if value < previous_id and in_scope:
                report.info("C008", card, f"ID {value} is older than the previous card's "
                                          f"{previous_id} — a card may have been moved or "
                                          "copy-pasted out of order")
            previous_id = max(previous_id, value)
        if not in_scope:
            continue
        if card.notetype is None:
            report.error("C001", card, f"missing the {NOTETYPE!r} note-type line")
        for name in REQUIRED:
            if name not in card.fields:
                report.error("C002", card, f"missing the {name}: field")
        seen = [n for n in card.order if n in FIELDS]
        canonical = [n for n in FIELDS if n in card.fields]
        if list(dict.fromkeys(seen)) != canonical:
            report.warn("C004", card, f"fields out of order: {' '.join(seen)} "
                                      f"(expected {' '.join(FIELDS)})")
        for name in ("Keyword", "Clue", "Kanji"):
            for lineno in card.continuations.get(name, []):
                report.warn("C010", card, f"L{lineno} continues the {name}: field — "
                                          "only Story and Note are ever multi-line")
        if not card.ids:
            report.error("C006", card, "no <!--ID: ...--> comment (Anki needs it to update "
                                       "the existing note instead of adding a duplicate)")
        elif len(card.ids) > 1:
            report.error("C006", card, "several ID comments: "
                                       + ", ".join(f"L{l}" for l, _ in card.ids))
        elif not card.id_last:
            report.warn("C006", card, f"the ID comment (L{card.ids[0][0]}) is not the last "
                                      "line before END")


def check_identity(cards: list[Card], scope: set[int], report: Report) -> None:
    by_keyword: dict[str, list[Card]] = defaultdict(list)
    by_stem: dict[tuple[str, ...], list[Card]] = defaultdict(list)
    by_kanji: dict[str, list[Card]] = defaultdict(list)
    for card in cards:
        if card.keyword:
            by_keyword[normalize_keyword(card.keyword)].append(card)
            by_stem[tuple(content_stems(card.keyword))].append(card)
        if card.kanji:
            by_kanji[card.kanji].append(card)

    for card in cards:
        if card.index not in scope:
            continue
        if not card.keyword:
            report.error("K001", card, "empty Keyword")
        elif re.search(r"[*_]", card.keyword):
            report.warn("K008", card, f"Keyword contains markup: {card.keyword!r} "
                                      "(the field is plain text; emphasis belongs in Story)")
        if not card.kanji:
            report.error("K004", card, "empty Kanji")
        elif len(card.kanji) != 1:
            report.error("K004", card, f"Kanji field holds {len(card.kanji)} characters: "
                                       f"{card.kanji!r}")
        elif not CJK_RE.match(card.kanji):
            report.error("K005", card, f"Kanji field is not a kanji: {card.kanji!r} "
                                       f"(U+{ord(card.kanji):04X} "
                                       f"{unicodedata.name(card.kanji, 'unnamed')})")
        elif "豈" <= card.kanji <= "﫿":
            report.warn("K006", card, f"Kanji U+{ord(card.kanji):04X} is a CJK compatibility "
                                      "ideograph, not the normal character — retype it")

        peers = [c for c in by_keyword[normalize_keyword(card.keyword)] if c is not card]
        if card.keyword and peers:
            report.error("K002", card, "duplicate Keyword, also on "
                                       + ", ".join(c.label() for c in peers))
        near = [c for c in by_stem[tuple(content_stems(card.keyword))]
                if c is not card and c not in peers]
        if card.keyword and near:
            report.info("K003", card, "Keyword differs only by inflection from "
                                      + ", ".join(f"{c.label()} {c.keyword!r}" for c in near))
        twins = [c for c in by_kanji[card.kanji] if c is not card]
        if card.kanji and twins:
            report.error("K007", card, "duplicate Kanji, also on "
                                       + ", ".join(c.label() for c in twins))


def check_markup(card: Card, text: str, where: str, report: Report) -> bool:
    """Balance and hygiene of emphasis markers. Returns False if unbalanced."""
    ok = True

    def plural(n):
        return f"{n} marker" + ("" if n == 1 else "s")

    if text.count("**") % 2:
        report.warn("S003", card, f"unbalanced ** in {where} ({plural(text.count('**'))})")
        ok = False
    without_bold = BOLD_RE.sub("", text)
    if without_bold.count("_") % 2:
        report.warn("S004", card, f"unbalanced _ in {where} ({plural(without_bold.count('_'))})")
        ok = False
    if without_bold.replace("**", "").count("*") % 2:
        report.warn("S005", card, f"unbalanced * in {where}")
        ok = False
    bold, italic = spans(text)
    for span in bold + italic:
        if not span.strip():
            report.warn("S006", card, f"empty emphasis span in {where}")
        elif span != span.strip():
            report.warn("S018", card, f"space just inside the markers in {where}: {span!r} "
                                      "(Markdown will not emphasize this)")
    return ok


def check_story(card: Card, report: Report) -> None:
    story = card.story
    if not story:
        report.error("S001", card, "empty Story — write one, or mark it '[no story]' "
                                   "(optionally '[no story - hint]')")
        return
    if "no story" in story.lower() or story.startswith("["):
        if not NO_STORY_RE.match(story):
            report.warn("S002", card, f"story looks like a no-story marker but does not match "
                                      f"'[no story]' / '[no story - hint]': {story!r}")
        return
    if not check_markup(card, story, "Story", report):
        return

    bold, italic = spans(story)
    keyword_bolded = [b for b in bold if keyword_in(b, card.keyword)]
    as_component = [s for s in italic if phrase_occurs(words_of(s), card.keyword)]
    in_plain = phrase_occurs(words_of(unmarked_text(story)), card.keyword)

    if not keyword_bolded and (as_component or in_plain):
        # one finding, not two: the keyword is in the story, just mismarked
        if as_component:
            report.warn("S009", card, f"the keyword {card.keyword!r} is marked as a component "
                                      f"(_{as_component[0]}_) instead of being wrapped in "
                                      "**bold** — components take single markers")
        if in_plain:
            report.warn("S009", card, f"the keyword {card.keyword!r} appears in the story with "
                                      "no emphasis at all — wrap it in **bold**")
        if bold:
            report.warn("S008", card, f"meanwhile the bolded text is {bold}, which is not the "
                                      "keyword")
    elif not bold:
        report.warn("S007", card, f"the keyword {card.keyword!r} does not appear in the story at "
                                  "all, bolded or otherwise")
    elif not keyword_bolded:
        report.warn("S008", card, f"the bolded text {bold} does not contain the keyword "
                                  f"{card.keyword!r} — wrong keyword, or the wrong words bolded")
    else:
        for b in bold:
            if b not in keyword_bolded:
                report.warn("S010", card, f"**{b}** is bolded but is not the keyword "
                                          f"{card.keyword!r} — bold is reserved for the keyword")
        # the keyword bolded more than once is fine — the deck does it on purpose
        for b in keyword_bolded:
            extra = [w for w in words_of(b) if not keyword_in(w, card.keyword)
                     and w.lower() not in STOPWORDS]
            if len(extra) >= 3:
                report.info("S011", card, f"the bold span reaches well past the keyword: "
                                          f"**{b}**")

    if keyword_bolded:
        for span in as_component:  # e.g. 具: **tools** on the _tool_ table, deliberately
            report.info("S009", card, f"the keyword {card.keyword!r} is also marked as a "
                                      f"component: _{span}_ — fine if the primitive genuinely "
                                      "shares the keyword, otherwise a marker slip")
        if in_plain:
            report.info("S009", card, f"the keyword {card.keyword!r} also appears unemphasized "
                                      "in the story")

    if not italic:
        report.info("S012", card, "no component primitives are marked up (fine for a pictogram "
                                  "or a pseudo-explanation, otherwise a gap)")
    for span in italic + bold:
        if len(words_of(span)) > 8:
            report.warn("S013", card, f"emphasis span runs on for {len(words_of(span))} words — "
                                      f"probably a missing closing marker: {span[:70]!r}")

    sentences = len(re.findall(r"[.!?]+(?=\s|$)", story))
    if len(story) > 240 or sentences > 3:
        report.info("S015", card, f"long story ({len(story)} chars, {sentences} sentences) — the "
                                  "deck's stories are one or two sentences")
    for m in re.finditer(r"\b(\w+)\s+\1\b", story, re.IGNORECASE):
        if m.group(1).lower() not in {"trees", "very", "ha", "no", "that"}:
            report.warn("S016", card, f"doubled word: {m.group(0)!r}")
    # note the ellipsis guards: "Many moons ago..." and "f...ing" are fine
    glitches = (r"\s+[,.;:!?]|,,|(?<!\.)\.\.(?!\.)|\?\.|!\.|[,;:]\.|\.[,;:]"
                r"|(?<=\S)  +(?=\S)")
    for glitch in re.findall(glitches, story):
        report.info("S017", card, f"punctuation glitch: {glitch!r}")
    for opener, closer in (("(", ")"), ("[", "]")):
        if story.count(opener) != story.count(closer):
            report.info("S017", card, f"unbalanced {opener}{closer} in the story")
    if story.count('"') % 2:
        report.info("S017", card, "odd number of double quotes in the story")
    # ignore trailing emphasis markers: "... **But of course!**" is punctuated
    tail = story.rstrip().rstrip("*_").rstrip()[-1]
    # a story that closes on a kanji or kana glyph is fine bare: "... the character 上"
    if tail not in '.!?"\')' and not (CJK_RE.match(tail) or KANA_RE.match(tail)):
        report.warn("S021", card, "story does not end with punctuation — add a full stop")
    # only the first *word* has to be capitalized; "2 nostrils, 2 ears ..." is fine
    opener = re.match(rf"[*_\"'(]*({LETTER})", story)
    if opener and opener.group(1).islower():
        report.warn("S022", card, "story starts in lowercase — Story fields open with a capital "
                                  "(inside the **bold** too, when the keyword comes first)")


# openers that stay capitalized when a Note begins with them
KEEP_CAPITALIZED = {
    "i", "i'd", "i'll", "i'm", "i've", "cf", "heisig", "japan", "japanese",
    "anki", "koohii", "jisho", "gemini", "english", "chinese",
}


def check_note(card: Card, report: Report) -> None:
    """Note and Update: same free prose, same conventions."""
    for name in PROSE:
        text = card.fields.get(name, "").strip()
        if not text:
            continue
        check_markup(card, text, name, report)
        opener = re.match(rf"[*_\"'(]*({LETTER}+(?:'{LETTER}+)?)", text)
        if opener:
            word = opener.group(1)
            if (word[0].isupper() and not word.isupper()  # ALL CAPS = keyword reference
                    and word.lower() not in KEEP_CAPITALIZED
                    and word.lower() not in SPELL_EXTRA):
                report.warn("N006", card, f"{name} starts with a capitalized {word!r} — "
                                          f"{name} fields open in lowercase (proper nouns and "
                                          "'I' excepted)")
        for m in re.finditer(r"primitives? meaning\s+((?:\*\*[^*\n]+\*\*[,;]?\s*(?:or|and)?\s*)+)",
                             text, re.IGNORECASE):
            report.info("N002", card, f"primitive meaning given in **bold**: "
                                      f"{m.group(1).strip()!r} — the deck marks primitive names "
                                      "with _italics_ and reserves **bold** for keywords")


def check_clue(card: Card, report: Report) -> None:
    """Clue is a terse disambiguating aside, not a sentence: no trailing full
    stop, and no parentheses (reword instead)."""
    clue = card.fields.get("Clue", "").strip()
    if not clue:
        return
    if clue.endswith("."):
        report.warn("L001", card, f"Clue ends with a full stop: {clue!r} — Clue fields "
                                  "carry no closing punctuation, drop the final '.'")
    if "(" in clue or ")" in clue:
        report.warn("L002", card, f"Clue contains parentheses: {clue!r} — the card renders "
                                  "the Clue already wrapped in parentheses, so inner ones look "
                                  "odd; reword it (your judgment, not a mechanical fix)")


def check_quoted_kanji(card: Card, deck_kanji: set[str], report: Report) -> None:
    """Kanji quoted inside a story. Notes are exempt: they routinely introduce
    non-jōyō primitives and near-miss characters on purpose."""
    quoted = list(dict.fromkeys(CJK_RE.findall(card.story)))
    if not quoted:
        return
    if card.kanji not in quoted:
        report.info("S020", card, f"the story quotes {' '.join(quoted)} but never this card's "
                                  f"own {card.kanji} — check nothing was pasted from another card")
    strangers = [c for c in quoted if c != card.kanji and c not in deck_kanji]
    if strangers:
        report.info("S020", card, f"the story quotes {' '.join(strangers)}, which no card in the "
                                  "deck teaches — check it is the character you meant")


def check_duplicate_stories(cards: list[Card], scope: set[int], report: Report) -> None:
    real = [c for c in cards if c.story and not NO_STORY_RE.match(c.story)]
    exact: dict[str, list[Card]] = defaultdict(list)
    for card in real:
        exact[re.sub(r"\s+", " ", card.story.lower())].append(card)
    reported: set[tuple[int, int]] = set()
    for group in exact.values():
        if len(group) > 1:
            for card in group:
                if card.index in scope:
                    report.warn("S014", card, "identical story to "
                                + ", ".join(c.label() for c in group if c is not card)
                                + " — deliberate contrast pairs happen, but check the Note "
                                  "explains it and each keyword is the bolded one")
            reported.update((a.index, b.index) for a in group for b in group)
    for i, card in enumerate(real):
        if card.index not in scope:
            continue
        for other in real[i + 1:]:
            if (card.index, other.index) in reported:
                continue
            matcher = difflib.SequenceMatcher(None, card.story.lower(), other.story.lower())
            if matcher.real_quick_ratio() < 0.85 or matcher.quick_ratio() < 0.85:
                continue
            if matcher.ratio() >= 0.85:
                report.info("S014", card, f"story is {matcher.ratio():.0%} identical to "
                                          f"{other.label()} — check one was not pasted over "
                                          "the other")


def check_vocab(cards: list[Card], scope: set[int], primitives: list[str], report: Report) -> None:
    """Component spans whose wording is new to the deck. Noisy by nature."""
    known: set[str] = set()
    for card in cards:
        known.update(content_stems(card.keyword))
        for name in PROSE:
            for span in spans(card.fields.get(name, ""))[1]:
                known.update(content_stems(span))
    for line in primitives:
        for span in re.findall(r"_([^_\n]+)_", line):
            known.update(content_stems(span))
    usage = Counter()
    for card in cards:
        for span in spans(card.story)[1]:
            usage.update(content_stems(span))
    for card in cards:
        if card.index not in scope:
            continue
        for span in spans(card.story)[1]:
            novel = [s for s in content_stems(span)
                     if s not in known and usage[s] < 2
                     and not any(loose_match(s, k) for k in known)]
            if novel:
                report.info("V001", card, f"component _{span}_ uses wording the deck has not "
                                          f"established: {', '.join(novel)}")


def check_spelling(cards: list[Card], scope: set[int], speller: Speller, report: Report) -> None:
    """One aspell call for the whole scope, then attribute each bad word back."""
    texts: list[tuple[Card, str, str]] = []
    for card in cards:
        if card.index not in scope:
            continue
        for where in ("Story", *PROSE):
            text = card.fields.get(where, "").strip()
            if text and not NO_STORY_RE.match(text):
                texts.append((card, where, text))
    bad = speller.unknown([t for _, _, t in texts])
    if not bad:
        return
    lowered = {w.lower() for w in bad}
    for card, where, text in texts:
        hits = sorted({w for w in speller.tokens_of(text)
                       if w in bad or w.lower() in lowered})
        if hits:
            code = "S019" if where == "Story" else "N003"
            report.warn(code, card, f"possible misspelling in {where}: " + ", ".join(hits)
                        + " — if a word is fine and likely to recur, add it to "
                          "the skill's wordlist.txt")


# -------------------------------------------------------------------- scope

def git_touched_cards(deck: Path, cards: list[Card]) -> tuple[set[int], str]:
    def diff(*args):
        try:
            out = subprocess.run(["git", "-C", str(deck.parent), *args, "-U0", "--", deck.name],
                                 capture_output=True, text=True, check=False, timeout=30)
            return out.stdout if out.returncode == 0 else ""
        except (OSError, subprocess.SubprocessError):
            return ""

    text, source = diff("diff", "HEAD"), "working tree vs HEAD"
    if not text.strip():
        text, source = diff("diff", "HEAD~1", "HEAD"), "the most recent commit"
    touched: set[int] = set()
    for m in re.finditer(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@", text, re.M):
        start = int(m.group(1))
        count = int(m.group(2) or 1)
        for card in cards:
            if card.start <= start + max(count - 1, 0) and (card.end or card.start) >= start:
                touched.add(card.index)
    return touched, source


def resolve_scope(args, cards: list[Card], deck: Path) -> tuple[set[int], str]:
    selected: set[int] = set()
    described: list[str] = []
    if args.range:
        for spec in args.range:
            m = re.fullmatch(r"(\d+)\s*-\s*(\d+)", spec)
            if not m:
                sys.exit(f"error: --range wants A-B, got {spec!r}")
            lo, hi = int(m.group(1)), int(m.group(2))
            selected.update(i for i in range(lo, hi + 1))
            described.append(f"cards {lo}-{hi}")
    if args.last:
        selected.update(c.index for c in cards[-args.last:])
        described.append(f"the last {args.last} cards")
    for n in args.card or []:
        selected.add(n)
        described.append(f"card {n}")
    for kanji in args.kanji or []:
        for char in kanji:
            hits = [c.index for c in cards if c.kanji == char]
            selected.update(hits)
            described.append(f"{char}" + ("" if hits else " (no such card)"))
    for keyword in args.keyword or []:
        wanted = normalize_keyword(keyword)
        hits = [c.index for c in cards if normalize_keyword(c.keyword) == wanted]
        selected.update(hits)
        described.append(f"keyword {keyword!r}" + ("" if hits else " (no such card)"))
    if args.recent:
        touched, source = git_touched_cards(deck, cards)
        selected.update(touched)
        described.append(f"{len(touched)} card(s) touched by {source}")
    if not described:
        return {c.index for c in cards}, f"all {len(cards)} cards"
    valid = {c.index for c in cards}
    unknown = selected - valid
    if unknown:
        described.append(f"(ignored out-of-range: {sorted(unknown)})")
    return selected & valid, ", ".join(described)


# ------------------------------------------------------------------- output

def emit(report: Report, cards: list[Card], scope: set[int], deck: Path,
         scope_text: str, spell: str, suppressions: list[Suppression],
         pruned: list[Suppression]) -> None:
    print("=" * 78)
    print(f"DECK: {deck}  ({len(cards)} cards)")
    print(f"SCOPE: {scope_text}")
    print(f"SPELL CHECK: {spell}")
    counts = Counter(f.severity for f in report.findings)
    print("FINDINGS: " + ", ".join(f"{s} {counts.get(s, 0)}" for s in SEVERITIES))
    print("=" * 78)

    live = [s for s in suppressions if s.live]
    if live:
        print()
        print(f"--- ALREADY REPORTED ({len(live)}) — reported before and left as is;")
        print("    do not raise these again")
        for s in live:
            print(f"  [{s.code}] {s.kanji}  {s.summary}")
    unknown = [s for s in suppressions if not s.known_card]
    if len(unknown) > 3:  # e.g. the store was written for a different deck file
        print(f"  [?] {len(unknown)} store entries name kanji this deck does not have "
              "(kept, unverified): " + " ".join(s.kanji for s in unknown))
    else:
        for s in unknown:
            print(f"  [?] {s.kanji} is not in the deck — entry kept, check by hand: {s.summary}")
    if pruned:
        print()
        print(f"--- DROPPED FROM THE STORE ({len(pruned)}) — the text they pointed at is gone,")
        print("    so the advice was taken; the entries have been deleted")
        for s in pruned:
            print(f"  [{s.code}] {s.kanji}  {s.summary}")

    for severity in SEVERITIES:
        group = [f for f in report.findings if f.severity == severity]
        if not group:
            continue
        blurb = {
            "ERROR": "breaks an invariant — a bad Anki import or a corrupt card",
            "WARN": "almost certainly a mistake",
            "INFO": "worth a look; often deliberate",
        }[severity]
        print()
        print(f"--- {severity} ({len(group)}) — {blurb}")
        # many cards saying the exact same thing collapse into one entry
        identical: dict[tuple[str, str], list[Finding]] = defaultdict(list)
        for f in group:
            identical[(f.code, f.message)].append(f)
        collapsed = {k for k, v in identical.items() if len(v) > 4}
        done: set[tuple[str, str]] = set()
        for f in sorted(group, key=lambda f: (f.sort_line, f.code)):
            key = (f.code, f.message)
            if key in collapsed:
                if key in done:
                    continue
                done.add(key)
                peers = identical[key]
                print(f"  [{f.code}] {len(peers)} cards: {f.message}")
                print("        " + ", ".join(p.where for p in peers))
                continue
            print(f"  [{f.code}] {f.where}")
            print(f"        {f.message}")
            if f.detail:
                print(f"        {f.detail}")

    if not report.findings:
        print("\nNo mechanical problems found.")
    print()
    print("=" * 78)
    print("Mechanical checks only. Whether a story actually matches its kanji, its")
    print("keyword and its primitives is a judgment call — read the cards.")


def dump(cards: list[Card], scope: set[int]) -> None:
    print()
    print("=" * 78)
    print("CARDS IN SCOPE (for the judgment pass)")
    print("=" * 78)
    for card in cards:
        if card.index not in scope:
            continue
        print(f"\n#{card.index} L{card.start}")
        for name in FIELDS:
            value = card.fields.get(name, "")
            if value:
                print(f"  {name}: " + value.replace("\n", "\n    "))


def main() -> None:
    parser = argparse.ArgumentParser(add_help=True, description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--deck")
    parser.add_argument("--range", action="append")
    parser.add_argument("--last", type=int)
    parser.add_argument("--card", type=int, action="append")
    parser.add_argument("--kanji", action="append")
    parser.add_argument("--keyword", action="append")
    parser.add_argument("--recent", action="store_true")
    parser.add_argument("--dump", action="store_true")
    parser.add_argument("--vocab", action="store_true")
    parser.add_argument("--no-spell", dest="spell", action="store_false")
    parser.add_argument("--wordlist")
    parser.add_argument("--suppressions")
    parser.add_argument("--no-prune", dest="prune", action="store_false")
    args = parser.parse_args()

    deck = Path(args.deck).resolve() if args.deck else find_file(DECK)
    lines = deck.read_text(encoding="utf-8").splitlines()
    report = Report()
    cards = parse(lines, report)
    if not cards:
        sys.exit(f"error: no START/END cards found in {deck}")

    global SPELL_EXTRA
    here = Path(__file__).resolve().parent
    scope, scope_text = resolve_scope(args, cards, deck)
    wordlist = Path(args.wordlist) if args.wordlist else here / "wordlist.txt"
    SPELL_EXTRA = load_wordlist(wordlist)
    speller = None
    spell_note = "skipped (--no-spell)"
    if args.spell:
        speller = Speller(SPELL_EXTRA, [c.keyword for c in cards])
        spell_note = f"aspell + {wordlist.name} + the deck's own keywords"

    deck_kanji = {c.kanji for c in cards if c.kanji}
    check_file(lines, cards, report)
    check_structure(cards, scope, report)
    check_identity(cards, scope, report)
    for card in cards:
        if card.index not in scope:
            continue
        check_story(card, report)
        check_note(card, report)
        check_clue(card, report)
        check_quoted_kanji(card, deck_kanji, report)
    check_duplicate_stories(cards, scope, report)
    if args.vocab:
        primitives_path = find_file("primitives.md", required=False)
        primitives = ([] if primitives_path is None
                      else primitives_path.read_text(encoding="utf-8").splitlines())
        check_vocab(cards, scope, primitives, report)
    if speller is not None:
        check_spelling(cards, scope, speller, report)

    report.restrict(scope)

    store = Path(args.suppressions) if args.suppressions else here / "reported.tsv"
    suppressions = apply_suppressions(load_suppressions(store), cards, report)
    stale = [s for s in suppressions if s.known_card and not s.live]
    if stale and args.prune:
        keep = [s for s in suppressions if s not in stale]
        store.write_text(SUPPRESSION_HEADER + "\n"
                         + "".join(s.line() + "\n" for s in keep), encoding="utf-8")
        suppressions = keep
    elif stale:
        for s in stale:
            s.summary += "  (stale — kept because of --no-prune)"

    emit(report, cards, scope, deck, scope_text, spell_note,
         suppressions, stale if args.prune else [])
    if args.dump:
        dump(cards, scope)


if __name__ == "__main__":
    main()
