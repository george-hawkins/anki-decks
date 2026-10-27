"""Refit coef.json from data.json (built by extract.py from the session transcripts).

usage: uv run --python 3.14 fit.py /path/to/data.json
"""
import json, math, sys
from _common import feats, COEF

d = json.load(open(sys.argv[1]))
rows = []
for c in d["cands"]:
    t = c["text"]
    head = t.split(":", 1)[0].strip().lower() if ":" in t[:40] else None
    if head == c["target"].strip('"').lower():
        t = t.split(":", 1)[1].strip()
    f, _ = feats(t)
    rows.append((f, 1 if c["status"] != "rejected" else 0))
keys = list(rows[0][0].keys())
X = [[r[0][k] for k in keys] for r in rows]; y = [r[1] for r in rows]
w = [0.0] * len(keys); lr, lam = 0.05, 0.01
for _ in range(4000):
    g = [0.0] * len(keys)
    for xi, yi in zip(X, y):
        p = 1 / (1 + math.exp(-sum(a * b for a, b in zip(w, xi))))
        for j in range(len(keys)):
            g[j] += (p - yi) * xi[j]
    for j in range(len(keys)):
        w[j] -= lr * (g[j] / len(y) + lam * w[j] * (j > 0))
coef = dict(zip(keys, w))
print({k: round(v, 2) for k, v in coef.items()}, "n", len(y), "kept", sum(y))
json.dump(coef, open(COEF, "w"), indent=1)
