#!/usr/bin/env python3
"""Ground an RTK story-writing session in the existing deck.

Usage:
    uv run --python 3.14 ground.py TARGET COMPONENT [COMPONENT ...]

TARGET is the keyword of the kanji being written; the remaining arguments
are its component keywords. An argument may list alternative keywords for
the same component separated by '/' (e.g. 'cauldron/cooking-fire').
Quote multi-word keywords ('rice field').

For every keyword this prints, from rtk1-v6.md and primitives.md:
  * the established deck entry (or the fact that none exists),
  * every other entry whose Story/Note mentions it (Note hits flagged ⚠),
  * matching primitives.md lines.
Matching is case-insensitive and inflection-tolerant (field/fields,
fortune-teller/fortune-telling).
"""

import difflib
import re
import sys
from pathlib import Path

DECK = "rtk1-v6.md"
PRIMITIVES = "primitives.md"
FIELD_RE = re.compile(r"(Keyword|Clue|Kanji|Reading|Story|Note):\s*(.*)")


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
    entries, cur, field = [], None, None
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped == "START":
            cur, field = {}, None
        elif stripped == "END":
            if cur:
                entries.append(cur)
            cur = None
        elif cur is not None:
            m = FIELD_RE.match(line)
            if m:
                field = m.group(1)
                cur[field] = m.group(2).strip()
            elif field and stripped and not stripped.startswith("<!--"):
                cur[field] += "\n" + stripped  # continuation (multi-line notes)
    return entries


def stem(word):
    for suffix in ("ing", "ers", "er", "ed", "es", "s"):
        if word.endswith(suffix) and len(word) - len(suffix) >= 3:
            return word[: -len(suffix)]
    return word


def term_regex(term):
    words = [w for w in re.split(r"[\s-]+", term.strip()) if w]
    pattern = r"\b" + r"[\s-]+".join(re.escape(stem(w)) + r"\w*" for w in words)
    return re.compile(pattern, re.IGNORECASE)


def harvest_vocab(entries, prim_lines):
    """All established deck vocabulary: keywords plus _primitive_ spans."""
    vocab = {}
    for e in entries:
        keyword = e.get("Keyword", "").strip().lower()
        if keyword:
            vocab.setdefault(keyword, f"keyword of {e.get('Kanji', '?')}")
        for field in ("Story", "Note"):
            for span in re.findall(r"_([^_\n]{1,40})_", e.get(field, "")):
                vocab.setdefault(span.strip().lower(),
                                 f"{field.lower()} of {e.get('Kanji', '?')} [{e.get('Keyword', '?')}]")
    for line in prim_lines:
        for span in re.findall(r"_([^_\n]{1,40})_", line):
            vocab.setdefault(span.strip().lower(), "primitives.md")
    return vocab


def suggest(alternatives, vocab):
    """Nearest vocabulary by shared word stems or overall similarity."""
    hits = {}
    for alt in alternatives:
        alt_stems = {stem(w) for w in re.split(r"[\s-]+", alt.lower()) if w}
        for term, source in vocab.items():
            term_stems = {stem(w) for w in re.split(r"[\s/-]+", term) if w}
            if alt_stems & term_stems:
                hits[term] = source
        for term in difflib.get_close_matches(alt.lower(), vocab, n=4, cutoff=0.75):
            hits[term] = vocab[term]
    return hits


def print_entry(entry, indent="    "):
    for field in ("Keyword", "Kanji", "Reading", "Story", "Note"):
        value = entry.get(field, "")
        if value:
            print(f"{indent}{field}: " + value.replace("\n", "\n" + indent + "  "))


def report(label, alternatives, entries, prim_lines, vocab, is_target):
    print("=" * 72)
    role = "TARGET" if is_target else "COMPONENT"
    print(f"{role} KEYWORD: {label}")
    regexes = [term_regex(alt) for alt in alternatives]

    def matches(text):
        # '_' is a regex word character; the deck's _primitive_ markup would
        # defeat \b and \w*, so treat underscores as spaces when matching.
        text = text.replace("_", " ")
        return any(rx.search(text) for rx in regexes)

    own = [e for e in entries if matches(e.get("Keyword", ""))]
    if own:
        header = ("ALREADY IN THE DECK — mention this and quote the existing story:"
                  if is_target else
                  "ESTABLISHED DECK ENTRY — reuse this exact vocabulary:")
        print(header)
        for e in own:
            print_entry(e)
            print()
    else:
        print("  (no deck entry has this keyword" +
              ("" if is_target else " — if it's a primitive, check primitives.md hits below") + ")")

    mentions = []
    for e in entries:
        if e in own:
            continue
        for field in ("Story", "Note"):
            for line in e.get(field, "").splitlines():
                if matches(line):
                    flag = "⚠ " if field == "Note" else "  "
                    mentions.append(f"{flag}{e.get('Kanji', '?')} [{e.get('Keyword', '?')}] {field}: {line}")
    if mentions:
        print("  MENTIONED ELSEWHERE (⚠ = usage note, obey it):")
        for m in mentions:
            print("    " + m)

    prim_hits = [line for line in prim_lines if matches(line)]
    if prim_hits:
        print("  PRIMITIVES.MD:")
        for line in prim_hits:
            print("    " + line.strip())

    if not own and not mentions and not prim_hits:
        suggestions = suggest(alternatives, vocab)
        if suggestions:
            print("  NO MATCHES — nearest established deck vocabulary; consider")
            print("  re-running with one of these (say so if you substitute):")
            for term, source in sorted(suggestions.items())[:12]:
                print(f"    _{term}_  ({source})")
        else:
            print("  NO MATCHES anywhere in the deck — fall back on your own RTK")
            print("  knowledge, and flag that in your output.")
    print()


def main():
    args = sys.argv[1:]
    if len(args) < 2:
        sys.exit(__doc__.strip())
    deck = parse_deck(find_file(DECK))
    prim_path = find_file(PRIMITIVES, required=False)
    prim_lines = [] if prim_path is None else [
        line for line in prim_path.read_text(encoding="utf-8").splitlines()
        if line.lstrip().startswith("*")]
    vocab = harvest_vocab(deck, prim_lines)
    for i, arg in enumerate(args):
        report(arg, arg.split("/"), deck, prim_lines, vocab, is_target=(i == 0))
    print("=" * 72)
    print("Reminder: use the deck's exact primitive vocabulary shown above;")
    print("⚠ lines are established usage warnings — follow them when picking")
    print("between '/' alternatives.")


if __name__ == "__main__":
    main()
