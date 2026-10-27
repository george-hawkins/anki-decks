# Bulk Mr. T tooling

Scripts behind `mr-t-stories.md`, the bulk-generated candidates for every kanji in which Mr. T plays ⺅ (see `person.md`). The single-shot `/rtk-story` skill does not use these. Run everything with `uv run --python 3.14 <script>` from anywhere; paths are resolved relative to the repo. They import `ground.py` from the parent skill folder.

| script | what it does |
|---|---|
| `dossier.py` | Grounding dossier for every Mr. T frame (or the frames given as arguments): Heisig primitives and text from `~/git/rtk-frames/rtk1-frames.json`, deck card, owning card and notes for each primitive. Written before drafting stories. |
| `check.py` | Validates `mr-t-stories.md`: frame coverage against `person.md`, three stories per block, length, bolding, marked components. |
| `clash.py` | Flags candidates sharing content words with a deck story on the same component, and counts Mr. T trope words (chains, "pity the fool", the van …). |
| `score.py` | Writes the `score: 0.74 (J 6)` line under every candidate. J is the judged quality rating (0–10), read from the existing score lines or from an optional ratings file. |
| `replace.py` | Given a `<frame>|<J>|<story>` candidates file, swaps the best new line into each block whose top score is below a threshold, if it beats the block's weakest. Run `score.py` afterwards. |
| `fit.py` | Refits `coef.json`, the surface prior, from a `data.json` produced by `extract.py`. |
| `extract.py` | From the 2026-10-26 analysis session: matches every story offered in the Claude session transcripts against the deck to label it kept, edited or rejected, and writes `data.json`. Needs the transcripts under `~/.claude/projects/`. |
| `_common.py` | Paths, the feature extractor, the scoring function and the block parser. |

## The score

`score = min(1, (0.02 + 0.006·J²) × prior(story) / 0.18 / 0.45)`

- **J** (0–10) is a judged quality rating: does the link force the keyword, are the components literal, is it one plain beat, does the image click, does Mr. T sit naturally. It is assigned by the model when the stories are written and stored in the score line so the number is reproducible.
- **prior** is P(kept) from surface features only, a logistic regression (`coef.json`) over the 885 candidates offered in sessions up to 2026-10-26 and whether each survived into the deck. It rewards 13–18 words and penalises a second sentence, a colon, a question, a quote and a parenthesis. 0.18 is the base rate.
- 0.45 is the cap: score 1.0 means a likelihood of about 45%, score 0.5 about 22%.

A story needs J 6 at 13–18 words, or J 7 otherwise, to reach 0.7.
