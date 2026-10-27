"""Validate mr-t-stories.md: every Mr. T frame in person.md present, three stories
per candidate block, <=24 words, keyword bolded, Mr. T and every component marked.
The component check is a loose stem match, so plurals like `rules` for `rule` can
show as false positives; read the flagged line before acting on it.

usage: uv run --python 3.14 check.py
"""
import re
from _common import STORIES, PERSON, blocks
import ground as g

rows, _ = g.parse_person(PERSON)
want = {r["frame"] for r in rows if r["use"] != "person"}
seen, problems = set(), 0
for frame, kanji, kw, meta, stories in blocks(STORIES.read_text(encoding="utf-8")):
    seen.add(frame)
    comps = [c.strip() for c in re.sub(r"\(.*?\)", "", meta["components"]).split(",")]
    if meta["status"] == "candidates" and len(stories) != 3:
        print(f"{frame} {kanji}: {len(stories)} stories"); problems += 1
    for s, _, _ in stories:
        plain = re.sub(r'[*_"]', "", s); n = len(plain.split()); issues = []
        if n > 24: issues.append(f"{n} words")
        if not re.search(r"\*\*[^*]*" + re.escape(kw.split()[0][:3]), s, re.I): issues.append("keyword not bolded")
        for c in comps:
            if c.startswith("Mr. T"):
                if not re.search(r"_" + re.escape(c) + r"(?:'s)?_", s): issues.append("Mr. T unmarked")
                continue
            ok = False
            for a in c.split("/"):
                stems = [g.stem(w) for w in a.split()]
                for span in re.findall(r"_([^_]+)_", s):
                    sw = [g.stem(w) for w in span.lower().split()]
                    if all(any(st.startswith(x[:4]) for st in sw) for x in stems): ok = True
            if not ok: issues.append(f"component {c!r} not marked")
        if issues:
            print(f"{frame} {kanji} [{kw}]: {'; '.join(issues)}\n    {s}"); problems += 1
print("missing frames:", sorted(want - seen, key=int), "extra:", sorted(seen - want, key=int))
print("blocks", len(seen), "problems", problems)
