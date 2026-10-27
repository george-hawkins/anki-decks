"""Shared paths and the surface-feature extractor used by the bulk Mr. T tooling."""
import json, math, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
REPO = SKILL.parents[2]          # .claude/skills/rtk-story/bulk -> repo root
sys.path.insert(0, str(SKILL))   # for `import ground`
DECK = REPO / "rtk1-v6.md"
PERSON = REPO / "person.md"
PRIMS = REPO / "primitives.md"
STORIES = REPO / "mr-t-stories.md"
FRAMES_JSON = Path.home() / "git/rtk-frames/rtk1-frames.json"
COEF = HERE / "coef.json"
BASE, CAP = 0.18, 0.45           # historical base rate; likelihood mapped to score 1.0


def feats(s):
    """Surface features of a story line, matching those coef.json was fitted on."""
    plain = re.sub(r"[*_]", "", s)
    plain = re.sub(r"\b(Mr|St|Dr|Mrs|Ms|e\.g|i\.e|vs)\. ?", r"\1 ", plain)
    words = re.findall(r"[A-Za-z'’-]+", plain)
    n = len(words)
    sents = len(re.findall(r"[.!?](?:\s|$)", plain.strip()))
    bold = re.search(r"\*\*(.+?)\*\*", s)
    kw = bold.group(1).lower() if bold else ""
    pos = plain.lower().find(kw) / max(len(plain), 1) if kw else 0.5
    rest = plain.split(" ", 1)[1] if " " in plain else ""
    named = bool(re.search(r"(?<![.!?]\s)(?<!^)\b[A-Z][a-z]{2,}", rest))
    return {
        "bias": 1.0,
        "w13_18": 1.0 if 13 <= n <= 18 else 0.0,
        "w19_24": 1.0 if 19 <= n <= 24 else 0.0,
        "w25": 1.0 if n >= 25 else 0.0,
        "multi": 1.0 if sents > 1 else 0.0,
        "colon": 1.0 if ":" in plain else 0.0,
        "semi": 1.0 if ";" in plain else 0.0,
        "quest": 1.0 if "?" in plain else 0.0,
        "excl": 1.0 if "!" in plain else 0.0,
        "quote": 1.0 if re.search(r'["“”]', plain) else 0.0,
        "paren": 1.0 if "(" in plain else 0.0,
        "first": 1.0 if re.search(r"\b(I|I'm|I'd|my|me|we|our)\b", plain) else 0.0,
        "you": 1.0 if re.search(r"\b(you|your|you'll|you're)\b", plain, re.I) else 0.0,
        "defn": 1.0 if re.search(r"\b(is|are|means|takes|needs)\b", plain) and pos < 0.4 else 0.0,
        "named": 1.0 if named else 0.0,
        "kwlate": 1.0 if pos > 0.66 else 0.0,
    }, n


def prior(s, coef=None):
    """P(kept) from surface features alone, per the logistic fit in coef.json."""
    coef = coef or json.load(open(COEF))
    f, _ = feats(s)
    return 1 / (1 + math.exp(-sum(coef[k] * v for k, v in f.items())))


def score(s, J, coef=None):
    """Judged rating J (0-10) plus surface prior -> score in [0, 1]."""
    return min(1.0, (0.02 + 0.006 * J * J) * prior(s, coef) / BASE / CAP)


def blocks(text):
    """Yield (frame, kanji, keyword, meta, stories) per '## ' block of mr-t-stories.md.
    stories: list of (story_text, score, J) with score/J None when absent."""
    for b in re.split(r"^## ", text, flags=re.M)[1:]:
        head, *lines = b.splitlines()
        frame, kanji, kw = head.split(" ", 2)
        meta = dict(re.findall(r"^([a-z]+): (.*)$", b, re.M))
        stories = []
        for i, l in enumerate(lines):
            if l.startswith("- "):
                sc = J = None
                if i + 1 < len(lines) and lines[i + 1].startswith("  score: "):
                    m = re.match(r"  score: ([\d.]+)(?: \(J (\d+)\))?", lines[i + 1])
                    sc = float(m.group(1)); J = int(m.group(2)) if m.group(2) else None
                stories.append((l[2:], sc, J))
        yield frame, kanji, kw, meta, stories
