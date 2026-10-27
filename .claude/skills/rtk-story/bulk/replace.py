"""Swap better candidates into mr-t-stories.md.

Reads a candidates file of `<frame>|<J>|<story>` lines (at most 8 per frame).
For each frame whose best score is below the threshold, the highest-scoring new
candidate replaces the block's weakest story if it beats it. Run score.py after.

usage: uv run --python 3.14 replace.py candidates.txt [threshold=0.7]
"""
import collections, json, re, sys
from _common import STORIES, COEF, score

coef = json.load(open(COEF))
thr = float(sys.argv[2]) if len(sys.argv) > 2 else 0.7
cands = collections.defaultdict(list)
for l in open(sys.argv[1], encoding="utf-8"):
    if l.strip():
        fr, J, t = l.rstrip("\n").split("|", 2)
        cands[fr].append((score(t, int(J), coef), int(J), t))
too_many = [fr for fr, v in cands.items() if len(v) > 8]
if too_many: sys.exit(f"more than 8 candidates for {too_many}")
lines = STORIES.read_text(encoding="utf-8").split("\n")
blocks_, cur = [], None
for i, l in enumerate(lines):
    m = re.match(r"^## (\d+) ", l)
    if m: cur = (m.group(1), []); blocks_.append(cur)
    elif l.startswith("- ") and i + 1 < len(lines) and lines[i + 1].startswith("  score: "):
        cur[1].append((i, i + 1, float(lines[i + 1].split()[1])))
replaced, unmet = [], []
for fr, items in blocks_:
    if not items or max(s for *_, s in items) >= thr or fr not in cands: continue
    best = max(cands[fr]); lo = min(items, key=lambda x: x[2])
    if best[0] > lo[2]:
        lines[lo[0]] = "- " + best[2]; lines[lo[1]] = f"  score: {best[0]:.2f} (J {best[1]})"
        replaced.append((fr, lo[2], best[0], best[2]))
    if best[0] < thr: unmet.append(fr)
STORIES.write_text("\n".join(lines), encoding="utf-8")
print(f"replaced {len(replaced)}, still below {thr}: {sorted(unmet, key=int)}")
for fr, old, new, t in replaced: print(f"{fr} {old:.2f} -> {new:.2f}  {t}")
