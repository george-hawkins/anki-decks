"""Flag candidates that share content words with an existing deck story on the same
component (a cheap proxy for re-staging a scene the deck already has), and count
Mr. T trope words across the file.

usage: uv run --python 3.14 clash.py
"""
import re
from _common import STORIES, DECK, blocks
import ground as g

deck = g.parse_deck(DECK)
STOP = set("""a an the and or but so of to in on at by for with from as is was were be been are it its his her he she they them their him my me i you your we our one two
that this these those who what when where which while until after before into out up down off over under than then there here not no nor if just only ever never
every all any some more most much very too still again like has have had do does did done get got gets go goes went come came put puts said says say made make makes
can could would should will own old new first last whole once same other another way thing things man men mr""".split())
def words(t):
    t = re.sub(r"[*_\"'’,.!?;:()]", " ", t.lower())
    return {g.stem(w) for w in t.split() if w not in STOP and len(w) > 2}
hits, all_stories = 0, []
for frame, kanji, kw, meta, stories in blocks(STORIES.read_text(encoding="utf-8")):
    all_stories += [s for s, _, _ in stories]
    if meta["status"] != "candidates": continue
    comps = [a for c in re.sub(r"\(.*?\)", "", meta["components"]).split(",")
             for a in c.strip().split("/") if not a.strip().startswith("Mr. T")]
    compwords = set().union(*[words(c) for c in comps]) | words(kw)
    rxs = [g.term_regex(c.strip()) for c in comps]
    related = [c for c in deck if any(rx.search(c.get("Story", "").replace("_", " ")) for rx in rxs)]
    for i, (s, _, _) in enumerate(stories, 1):
        cw = words(s) - compwords
        for c in related:
            shared = cw & (words(c.get("Story", "")) - compwords)
            if len(shared) >= 2:
                hits += 1
                print(f"{frame} {kanji} [{kw}] #{i} ~ {c['Kanji']} [{c['Keyword']}] shares {sorted(shared)}\n    {s}\n    {c['Story']}")
print("pairs flagged:", hits)
TROPES = {"mohawk": r"mohawk", "chains": r"\bchains?\b", "fool": r"\bfools?\b", "pity": r"\bpit(y|ies)\b",
          "van": r"\bvan\b", "flying": r"\b(fly|flying|plane|flies)\b", "milk": r"\bmilk", "jibber": r"jibber",
          "A-Team": r"A-Team", "Clubber/Rocky": r"Clubber|Rocky", "gold": r"\bgold"}
for k, rx in TROPES.items():
    n = [s for s in all_stories if re.search(rx, s)]
    print(f"{k}: {len(n)}" + "".join("\n    " + s for s in n))
