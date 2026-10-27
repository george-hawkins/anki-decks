#!/usr/bin/env python3
"""Ground an /rtk-story session in the existing deck.

Usage:
    uv run --python 3.14 ground.py TARGET COMPONENT [COMPONENT ...]

TARGET is the keyword of the kanji being written; the COMPONENTs are the
keywords of its primitives. 'a/b/c' lists alternative names for ONE
component (e.g. 'fire/fireplace'). Quote multi-word keywords ('rice field').
A lone kanji anywhere in the arguments is taken as the target kanji and used
to sanity-check (or, if no keyword is given, to look up) the target card.

For every keyword the script prints, from rtk1-v6.md and primitives.md:
  * the deck card that owns it, or that none does;
  * every other card whose Story/Note uses it (⚠ = a Note, i.e. a usage
    rule) — matching is case-insensitive and inflection-tolerant
    (field/fields, woman/women, fortune-teller/fortune-telling);
  * matching primitives.md lines;
  * for an unknown component, the nearest established vocabulary.
A component of 'person' (人/⺅, Mr. T) gets the casting block from
person.md instead — see SKILL.md.
"""

import difflib
import re
import sys
from pathlib import Path

DECK = "rtk1-v6.md"
PRIMITIVES = "primitives.md"
PERSON = "person.md"
STORIES = "mr-t-stories.md"
FIELD_RE = re.compile(r"(Keyword|Clue|Kanji|Reading|Story|Note|Update):\s*(.*)")
CJK_RE = re.compile(r"^[㐀-䶿一-鿿豈-﫿]$")
# a marked primitive span: _x_ (asterisk-glued forms are matched as plain words)
SPAN_RE = re.compile(r"(?<![\w*])_([^_\n]{1,40})_(?![\w*])")
PERSON_ALIASES = {"person", "mr t", "mrt", "人", "⺅", "亻"}
MR_T_RE = re.compile(r"\bMr\.?\s*T\b(?!\w)")
IRREGULAR = [
    ("woman", "women"), ("man", "men"), ("child", "children"), ("foot", "feet"),
    ("tooth", "teeth"), ("mouse", "mice"), ("leaf", "leaves"), ("knife", "knives"),
    ("wolf", "wolves"), ("shelf", "shelves"), ("thief", "thieves"), ("wife", "wives"),
    ("calf", "calves"), ("half", "halves"), ("life", "lives"), ("goose", "geese"),
    ("ox", "oxen"), ("person", "people"), ("die", "dice"),
]
IRREGULAR_MAP = {w: group for group in IRREGULAR for w in group}
SUFFIXES = ("ies", "ing", "ers", "er", "ed", "es", "s")


# ----------------------------------------------------------------- files

def find_file(name, required=True):
    here = Path(__file__).resolve().parent
    for base in [Path.cwd(), *Path.cwd().parents, here, *here.parents]:
        p = base / name
        if p.is_file():
            return p
    if required:
        sys.exit(f"error: {name} not found in or above {Path.cwd()}")
    return None


def parse_deck(path):
    """START…END cards as dicts of field -> text (continuation lines joined)."""
    cards, cur, field = [], None, None
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped == "START":
            cur, field = {}, None
        elif stripped == "END":
            if cur:
                cards.append(cur)
            cur = None
        elif cur is not None:
            m = FIELD_RE.match(line)
            if m:
                field = m.group(1)
                cur[field] = m.group(2).strip()
            elif field and stripped and not stripped.startswith("<!--"):
                cur[field] += "\n" + stripped
    return cards


def parse_person(path):
    """person.md: the casting table and the 'excluded' list."""
    rows, excluded, in_excluded = [], [], False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## ") and "xclude" in line:
            in_excluded = True
        elif line.startswith("|") and not line.startswith("|---"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) == 5 and cells[0].isdigit():
                rows.append(dict(zip(("frame", "kanji", "keyword", "use", "angle"), cells)))
        elif in_excluded and line.startswith("- ") and ":" in line:
            left, right = line[2:].split(":", 1)
            component = re.sub(r"\s*\(.*\)\s*$", "", left).strip()
            for item in right.split(","):
                parts = item.strip().split(None, 1)
                if len(parts) == 2:
                    excluded.append((component, parts[0], parts[1]))
    return rows, excluded


# -------------------------------------------------------------- matching

def words_of(term):
    return [w for w in re.split(r"[\s\-_/]+", term.strip().lower()) if w]


def normalize(term):
    return " ".join(words_of(term))


def word_pattern(word):
    """Regex for one word and its ordinary inflections."""
    if word in IRREGULAR_MAP:
        return "(?:" + "|".join(re.escape(w) for w in IRREGULAR_MAP[word]) + ")"
    base, stripped = word, False
    for suf in SUFFIXES:
        if word.endswith(suf) and len(word) - len(suf) >= 3:
            base = word[: -len(suf)] + ("y" if suf == "ies" else "")
            stripped = True
            break
    if stripped and len(base) >= 4 and base[-1] == base[-2] and base[-1] not in "aeiouy":
        base = base[:-1]  # running -> run (the doubled letter is optional below)
        core = re.escape(base) + re.escape(base[-1]) + "?"
    else:
        core = re.escape(base)
    if base.endswith("y"):
        return re.escape(base[:-1]) + "(?:y|ys|ies|ied|ier|iers|ying)"
    if base.endswith("e"):  # stone, stones, stony; tree, trees
        return re.escape(base[:-1]) + "(?:e|es|ed|ing|er|ers|y|en)"
    if stripped:  # glued -> glu: glue, glues, gluing; water -> wat: watery
        return core + "(?:e|es|ed|d|s|ing|er|ers|y|en|ery)?"
    return core + "(?:s|es|ed|ing|er|ers|y|en)?"  # wood, wooden, woody


def term_regex(term):
    return re.compile(r"\b" + r"[\s\-]+".join(word_pattern(w) for w in words_of(term)) + r"\b",
                      re.IGNORECASE)


def stem(word):
    for suf in SUFFIXES:
        if word.endswith(suf) and len(word) - len(suf) >= 3:
            return word[: -len(suf)]
    return word


def harvest_vocab(cards, prim_lines):
    """Every established name: card keywords plus _marked_ primitive spans."""
    vocab = {}
    for c in cards:
        keyword = c.get("Keyword", "").strip().lower()
        if keyword:
            vocab.setdefault(keyword, f"keyword of {c.get('Kanji', '?')}")
        for field in ("Story", "Note"):
            for span in SPAN_RE.findall(c.get(field, "")):
                vocab.setdefault(span.strip().lower(),
                                 f"{field.lower()} of {c.get('Kanji', '?')} [{c.get('Keyword', '?')}]")
    for line in prim_lines:
        for span in SPAN_RE.findall(line):
            vocab.setdefault(span.strip().lower(), "primitives.md")
    return vocab


def suggest(alternatives, vocab):
    """Nearest established names, by shared word stems or string similarity."""
    hits = {}
    for alt in alternatives:
        alt_stems = {stem(w) for w in words_of(alt)}
        for term, source in vocab.items():
            if alt_stems & {stem(w) for w in words_of(term)}:
                hits[term] = source
        for term in difflib.get_close_matches(normalize(alt), vocab, n=4, cutoff=0.75):
            hits[term] = vocab[term]
    return hits


# -------------------------------------------------------------- printing

def hr():
    print("=" * 72)


def print_card(card, indent="    "):
    for field in ("Keyword", "Clue", "Kanji", "Story", "Note", "Update"):
        value = card.get(field, "")
        if value:
            print(f"{indent}{field}: " + value.replace("\n", "\n" + indent + "  "))


def mentions(cards, skip, hit):
    """Lines of other cards' Story/Note for which hit(line) is true."""
    out = []
    for c in cards:
        if c in skip:
            continue
        for field in ("Story", "Note"):
            for line in c.get(field, "").splitlines():
                if hit(line):
                    flag = "⚠ " if field == "Note" else "  "
                    out.append(f"{flag}{c.get('Kanji', '?')} [{c.get('Keyword', '?')}] {field}: {line}")
    return out


def has_story(card):
    story = card.get("Story", "").strip()
    return bool(story) and not story.startswith("[no story")


def report_target(keyword_alts, kanji, cards):
    hr()
    label = keyword_alts[0] if keyword_alts else "?"
    print(f"TARGET: {label}" + (f"  ({kanji})" if kanji else ""))
    wanted = {normalize(a) for a in keyword_alts}
    own = [c for c in cards if normalize(c.get("Keyword", "")) in wanted]
    by_kanji = [c for c in cards if kanji and c.get("Kanji", "") == kanji]
    if not own and by_kanji:
        own = by_kanji
        if keyword_alts:
            print(f"  ⚠ no card has keyword '{label}'; the card for {kanji} is:")
        else:
            print(f"  card found by kanji — its keyword is '{own[0].get('Keyword', '?')}':")
    elif own and by_kanji and own[0] is not by_kanji[0]:
        print(f"  ⚠ KEYWORD/KANJI MISMATCH: '{label}' is the card for "
              f"{own[0].get('Kanji', '?')}, but {kanji} is [{by_kanji[0].get('Keyword', '?')}].")
    if own:
        for c in own:
            if has_story(c):
                print("  ⚠ ALREADY HAS A STORY — probably a mistyped keyword, or a story was")
                print("    already written. Say so, quote it, and still offer fresh stories:")
            else:
                print("  deck card awaiting a story (the normal case):")
            print_card(c)
    else:
        print("  no card has this keyword yet — as expected for a new kanji.")
    regexes = [term_regex(a) for a in keyword_alts]
    used = mentions(cards, own, lambda line: any(rx.search(line.replace("_", " ")) for rx in regexes))
    if used:
        print("  THE KEYWORD IS USED IN OTHER CARDS (is it also a primitive name?):")
        for m in used:
            print("    " + m)
    print()


def parse_stories(path):
    """mr-t-stories.md: one dict per '## frame kanji keyword' block."""
    blocks = []
    for chunk in re.split(r"^## ", path.read_text(encoding="utf-8"), flags=re.M)[1:]:
        head, *lines = chunk.splitlines()
        parts = head.split(" ", 2)
        if len(parts) < 3:
            continue
        b = {"frame": parts[0], "kanji": parts[1], "keyword": parts[2], "stories": []}
        for i, line in enumerate(lines):
            m = re.match(r"([a-z]+): (.*)", line)
            if m and not line.startswith(" "):
                b[m.group(1)] = m.group(2).strip()
            elif line.startswith("- "):
                score = None
                if i + 1 < len(lines):
                    sm = re.match(r"\s+score: ([\d.]+)", lines[i + 1])
                    score = float(sm.group(1)) if sm else None
                b["stories"].append((score, line[2:].strip()))
        blocks.append(b)
    return blocks


def report_prewritten(keyword_alts, kanji):
    """Stories already written in bulk for this target, best score first."""
    path = find_file(STORIES, required=False)
    if path is None:
        return False
    wanted = {normalize(a) for a in keyword_alts}
    hits = [b for b in parse_stories(path)
            if normalize(b["keyword"]) in wanted or (kanji and b["kanji"] == kanji)]
    if not hits:
        return False
    hr()
    for b in hits:
        print(f"PRE-WRITTEN STORIES ({STORIES}): {b['frame']} {b['kanji']} [{b['keyword']}]")
        print("  Present these instead of drafting new ones (see the skill's")
        print("  'Pre-written Mr. T stories' section). Highest score first:")
        print(f"  components: {b.get('components', '?')}")
        if b.get("status") == "in deck":
            print("  ⚠ status: in deck — the deck already holds this story")
        if b.get("flag"):
            print(f"  flag: {b['flag']}")
        ranked = sorted(b["stories"], key=lambda t: -(t[0] if t[0] is not None else -1))
        for score, story in ranked:
            print(f"  {score:.2f}  {story}" if score is not None else f"  ----  {story}")
    print()
    return True


def report_component(label, alternatives, cards, prim_lines, vocab):
    hr()
    print(f"COMPONENT: {label}")
    regexes = [term_regex(a) for a in alternatives]

    def hit(text):
        text = text.replace("_", " ")  # '_' is a word char; markup would defeat \b
        return any(rx.search(text) for rx in regexes)

    own = [c for c in cards if hit(c.get("Keyword", ""))]
    if own:
        print("  ESTABLISHED NAME — the card that owns it; reuse this exact vocabulary:")
        for c in own:
            print_card(c)
            print()
    else:
        print("  no card has this keyword (if it is a Heisig primitive, see primitives.md hits)")
    used = mentions(cards, own, hit)
    if used:
        print("  USED ELSEWHERE — vocabulary and clash-avoidance only, never borrow the")
        print("  imagery (⚠ = a Note, i.e. a binding usage rule):")
        for m in used:
            print("    " + m)
    prim_hits = [line.strip() for line in prim_lines if hit(line)]
    if prim_hits:
        print("  PRIMITIVES.MD:")
        for line in prim_hits:
            print("    " + line)
    if not own and not used and not prim_hits:
        suggestions = suggest(alternatives, vocab)
        if suggestions:
            print("  NO MATCHES — nearest established names; use the one the user plainly")
            print("  meant and say that you substituted it:")
            for term, source in sorted(suggestions.items())[:12]:
                print(f"    _{term}_  ({source})")
        else:
            print("  NO MATCHES anywhere in the deck — fall back on your own RTK knowledge")
            print("  and flag that in your output.")
    print()


def report_person(keyword_alts, kanji, cards, prim_lines):
    hr()
    print("COMPONENT: person  ->  special case, cast from person.md")
    path = find_file(PERSON, required=False)
    if path is None:
        print("  ⚠ person.md not found — default: Mr. T plays every standalone ⺅/人.")
        print()
        return
    rows, excluded = parse_person(path)
    wanted = {normalize(a) for a in keyword_alts}
    kanji_set = {c.get("Kanji", "") for c in cards if normalize(c.get("Keyword", "")) in wanted}
    kanji_set.discard("")
    if kanji:
        kanji_set.add(kanji)

    excl = [x for x in excluded if normalize(x[2]) in wanted or x[1] in kanji_set]
    rows_hit = [r for r in rows if normalize(r["keyword"]) in wanted or r["kanji"] in kanji_set]
    if excl:
        for component, k, keyword in excl:
            print(f"  ⚠ EXCLUDED: in {k} [{keyword}] the ⺅ is buried inside the named")
            print(f"    component _{component}_. Leave Mr. T out and use _{component}_ as")
            print(f"    the component (re-run with it instead of 'person').")
    elif rows_hit:
        for r in rows_hit:
            print(f"  person.md: frame {r['frame']} {r['kanji']} [{r['keyword']}]")
            print(f"    WHO PLAYS ⺅: {r['use']}")
            print(f"    suggested angle (Koohii-derived, optional): {r['angle']}")
    else:
        print("  target not listed in person.md — if ⺅/人 stands on its own, Mr. T")
        print("  plays it; if it is buried inside a named component, use that name.")
    print()

    own = [c for c in cards if normalize(c.get("Keyword", "")) == "person"]
    if own:
        print("  DECK CARD for the primitive itself:")
        for c in own:
            print_card(c)
        print()
    so_far = mentions(cards, [], lambda line: bool(MR_T_RE.search(line)))
    if so_far:
        print("  MR. T SO FAR (he should recur; a scene should not):")
        for m in so_far:
            print("    " + m)
    else:
        print("  MR. T SO FAR: no card features him yet.")
    word = re.compile(r"\bpersons?\b", re.IGNORECASE)
    marked = mentions(cards, own, lambda line: any(word.search(m.group(1)) for m in SPAN_RE.finditer(line)))
    if marked:
        print("  _person_ MARKED AS A PRIMITIVE ELSEWHERE:")
        for m in marked:
            print("    " + m)
    prim_hits = [line.strip() for line in prim_lines if re.search(r"\bperson", line, re.IGNORECASE)]
    if prim_hits:
        print("  PRIMITIVES.MD:")
        for line in prim_hits:
            print("    " + line)
    print()


# ------------------------------------------------------------------ main

def main():
    args = sys.argv[1:]
    kanji_args = [a for a in args if CJK_RE.match(a)]
    args = [a for a in args if not CJK_RE.match(a)]
    if len(kanji_args) > 1:
        sys.exit(f"error: more than one kanji given: {' '.join(kanji_args)}")
    kanji = kanji_args[0] if kanji_args else None
    if not args or (not kanji and len(args) < 2):
        sys.exit(__doc__.strip())

    cards = parse_deck(find_file(DECK))
    prim_path = find_file(PRIMITIVES, required=False)
    prim_lines = [] if prim_path is None else [
        line for line in prim_path.read_text(encoding="utf-8").splitlines()
        if line.lstrip().startswith("*")]
    vocab = harvest_vocab(cards, prim_lines)

    # the keyword is the first argument — unless a kanji was given that has a
    # deck card, in which case the card's keyword wins and a first argument
    # that doesn't match it is just another component
    keyword_alts, components = args[:1], args[1:]
    card = next((c for c in cards if kanji and c.get("Kanji") == kanji), None)
    if card and normalize(card.get("Keyword", "")) != normalize(args[0]):
        keyword_alts, components = [card["Keyword"]], args
    if normalize(keyword_alts[0]) in PERSON_ALIASES:
        print(f"⚠ '{keyword_alts[0]}' is the TARGET keyword here — did you leave the keyword out?")

    report_target(keyword_alts, kanji, cards)
    report_prewritten(keyword_alts, kanji)
    for arg in components:
        alts = arg.split("/")
        if any(normalize(a).replace(".", "") in PERSON_ALIASES or a.strip() in PERSON_ALIASES
               for a in alts):
            report_person(keyword_alts, kanji, cards, prim_lines)
        else:
            report_component(arg, alts, cards, prim_lines, vocab)
    hr()
    print("Use the deck's exact vocabulary; ⚠ lines are binding; never borrow another")
    print("card's imagery — the lists above are for clash-avoidance only.")


if __name__ == "__main__":
    main()
