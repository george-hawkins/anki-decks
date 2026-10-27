"""(Re)write the `score:` line under every candidate in mr-t-stories.md.

J ratings are read from existing `score: x (J n)` lines, or from an optional
ratings file (`<frame> <J1> <J2> <J3>` per line) given as the first argument.

usage: uv run --python 3.14 score.py [ratings.txt]
"""
import json, re, statistics as st, sys
from _common import STORIES, COEF, score, blocks

coef = json.load(open(COEF))
ratings = {}
if len(sys.argv) > 1:
    for l in open(sys.argv[1]):
        if l.strip():
            fr, *js = l.split(); ratings[fr] = [int(j) for j in js]
text = STORIES.read_text(encoding="utf-8")
Js = {}
for frame, _, _, meta, stories in blocks(text):
    if meta.get("status") != "candidates": continue
    for i, (s, sc, J) in enumerate(stories):
        j = ratings.get(frame, [None] * 3)[i] if frame in ratings else J
        if j is None: sys.exit(f"no J rating for {frame} #{i+1}")
        Js[(frame, i)] = j
out, frame, status, i, scores = [], None, None, 0, []
for line in re.sub(r"^  score: .*\n", "", text, flags=re.M).splitlines():
    m = re.match(r"^## (\d+) ", line)
    if m: frame, i = m.group(1), 0
    if line.startswith("status: "): status = line[8:].strip()
    out.append(line)
    if line.startswith("- ") and status == "candidates":
        J = Js[(frame, i)]; i += 1
        sc = score(line[2:], J, coef); scores.append(sc)
        out.append(f"  score: {sc:.2f} (J {J})")
STORIES.write_text("\n".join(out) + "\n", encoding="utf-8")
print(f"n {len(scores)} mean {st.mean(scores):.2f} median {st.median(scores):.2f} "
      f">=0.7: {sum(s >= 0.7 for s in scores)}  <0.4: {sum(s < 0.4 for s in scores)}")
