import json, sys, glob, re, difflib, os
P = os.path.expanduser("~/.claude/projects/-Users-georgehawkins-git-anki-decks")
DECK = "rtk1-v6.md"

# ---- deck
cards, cur = [], None
for line in open(DECK, encoding="utf-8"):
    s = line.strip()
    if s == "START": cur = {}
    elif s == "END":
        if cur: cards.append(cur)
        cur = None
    elif cur is not None:
        m = re.match(r"(Keyword|Clue|Kanji|Story|Note|Update):\s*(.*)", line)
        if m: cur[m.group(1)] = m.group(2).strip(); last = m.group(1)
        elif s and not s.startswith("<!--") and cur: cur[last] += "\n" + s
for i, c in enumerate(cards): c["frame"] = i + 1

def norm(t):
    t = t.lower()
    t = re.sub(r"[*_]", "", t)
    t = re.sub(r"[^a-z0-9' ]+", " ", t)
    return re.sub(r"\s+", " ", t).strip()

deck_stories = [(c["frame"], c["Keyword"], c["Kanji"], c["Story"]) for c in cards
                if c.get("Story") and not c["Story"].startswith("[no story")]
deck_norm = {f: norm(s) for f, k, kj, s in deck_stories}

# ---- transcripts
def texts(content):
    if isinstance(content, str): return [content]
    out = []
    for it in content or []:
        if it.get("type") == "text": out.append(it["text"])
    return out

events = []  # (session, ts, role, text)
for f in sorted(glob.glob(P + "/*.jsonl")):
    sid = os.path.basename(f)[:8]
    for line in open(f, encoding="utf-8"):
        try: d = json.loads(line)
        except Exception: continue
        if d.get("type") not in ("user", "assistant"): continue
        if d.get("isSidechain"): continue
        msg = d.get("message", {})
        for t in texts(msg.get("content")):
            if d["type"] == "user":
                if "<command-name>/rtk-story</command-name>" in t:
                    m = re.search(r"<command-args>(.*?)</command-args>", t, re.S)
                    events.append((sid, d["timestamp"], "invoke", m.group(1).strip() if m else ""))
                elif t.startswith("Base directory for this skill") or t.startswith("<command-") or "<local-command" in t or "<system-reminder>" in t[:20]:
                    continue
                elif d.get("origin", {}).get("kind") == "human" or d.get("userType") == "external":
                    if not t.startswith("<"): events.append((sid, d["timestamp"], "user", t))
            else:
                events.append((sid, d["timestamp"], "assistant", t))

# ---- candidates: assistant lines with a bold span, attributed to the latest invoke
cands = []
ctx = None; reply_idx = 0
for sid, ts, role, text in events:
    if role == "invoke":
        ctx = (sid, ts, text); reply_idx = 0; cand_idx = 0
    elif role == "user":
        reply_idx += 1
    elif role == "assistant" and ctx and ctx[0] == sid:
        for ln in text.splitlines():
            ln = ln.strip().lstrip("-*0123456789. ").strip()
            if "**" in ln and "_" in ln and len(ln) > 20 and not ln.startswith("#"):
                cands.append(dict(session=sid, ts=ts, args=ctx[2], target=ctx[2].split()[0] if ctx[2] else "",
                                  reply=reply_idx, idx=cand_idx, text=ln))
                cand_idx += 1

# ---- match candidates to deck (keyword-first, quick_ratio prefilter)
deck_by_kw = {}
for f, k, kj, st in deck_stories:
    deck_by_kw.setdefault(norm(k), []).append(f)
for c in cands:
    n = norm(c["text"])
    kw = norm(c["target"].strip('"'))
    best, bf = 0, None
    pool = deck_by_kw.get(kw) or list(deck_norm)
    sm = difflib.SequenceMatcher(None, n)
    for f in pool:
        dn = deck_norm[f]
        sm.set_seq2(dn)
        if sm.real_quick_ratio() < 0.6 or sm.quick_ratio() < 0.6: continue
        r = sm.ratio()
        if r > best: best, bf = r, f
    c["match"] = best; c["frame"] = bf
    c["status"] = "exact" if best >= 0.97 else "edited" if best >= 0.6 else "rejected"

json.dump(dict(cands=cands, events=events, deck=deck_stories), open("/tmp/rtk_analysis/data.json", "w"), ensure_ascii=False, indent=0)
import collections
print("candidates", len(cands), collections.Counter(c["status"] for c in cands))
print("invocations", sum(1 for e in events if e[2] == "invoke"))
print("user follow-ups", sum(1 for e in events if e[2] == "user"))
# acceptance by position in first reply
pos = collections.defaultdict(collections.Counter)
for c in cands:
    if c["reply"] == 0: pos[min(c["idx"], 3)][c["status"]] += 1
for k in sorted(pos): print("first-reply idx", k, dict(pos[k]))
rep = collections.defaultdict(collections.Counter)
for c in cands: rep[min(c["reply"], 3)][c["status"]] += 1
for k in sorted(rep): print("reply#", k, dict(rep[k]))
# deck frames in transcript range with no matching candidate
matched_frames = {c["frame"] for c in cands if c["status"] != "rejected"}
frames_in_range = [f for f, k, kj, s in deck_stories if f >= 741]
print("deck stories >=741:", len(frames_in_range), "matched to a candidate:", len([f for f in frames_in_range if f in matched_frames]))
