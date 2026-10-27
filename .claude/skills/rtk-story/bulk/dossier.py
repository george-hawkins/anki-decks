"""Grounding dossier for every Mr. T frame in person.md: Heisig's primitives and
text from rtk1-frames.json, the deck card if any, and for each primitive the deck
card that owns it, its notes (where alternative forms are defined) and matching
primitives.md lines. Prints to stdout; redirect to a file and read it in chunks.

usage: uv run --python 3.14 dossier.py [frame ...]
"""
import json, re, sys
from _common import DECK, PERSON, PRIMS, FRAMES_JSON
import ground as g

deck = g.parse_deck(DECK)
prim_lines = PRIMS.read_text(encoding="utf-8").splitlines()
vocab = g.harvest_vocab(deck, prim_lines)
rows, _ = g.parse_person(PERSON)
frames = {str(f["number"]): f for f in json.load(open(FRAMES_JSON)) if f.get("type") == "frame"}
by_kanji = {c.get("Kanji", ""): c for c in deck}
only = set(sys.argv[1:])
for r in rows:
    if r["use"] == "person" or (only and r["frame"] not in only): continue
    f = frames[r["frame"]]
    print("=" * 70)
    print(f"FRAME {r['frame']} {f['glyph']} [{f['keyword']}]   cast: {r['use']}")
    print(f"HEISIG PRIMITIVES: {', '.join(f['primitives'])}")
    print(f"ANGLE: {r['angle']}")
    card = by_kanji.get(f["glyph"])
    print("DECK: " + (f"Story: {card.get('Story') or '[none]'} | Note: {card.get('Note', '')}" if card else "no card"))
    print("HEISIG: " + " ".join(p["md"] for p in f["paras"])[:500])
    for p in f["primitives"]:
        if p == "person": continue
        rx = g.term_regex(p)
        hit = lambda t: rx.search(t.replace("_", " "))
        own = [c for c in deck if hit(c.get("Keyword", ""))]
        for c in own[:3]:
            print(f"  PRIM '{p}': {c.get('Kanji')} [{c.get('Keyword')}]  Story: {c.get('Story', '')}")
            if c.get("Note"): print(f"      Note: {c['Note']}")
        if not own:
            print(f"  PRIM '{p}': NO DECK CARD; nearest: {', '.join(sorted(g.suggest([p], vocab))[:8])}")
        for c in deck:
            if c in own: continue
            for line in c.get("Note", "").splitlines():
                if hit(line): print(f"      ⚠ {c.get('Kanji')} [{c.get('Keyword')}]: {line}")
        for line in prim_lines:
            if hit(line): print(f"      primitives.md: {line.strip()}")
    print()
