---
name: rtk-story
description: Craft an RTK (Remembering the Kanji) mnemonic story that links a kanji's keyword to the keywords of its component primitives, in the established style of this deck (rtk1-v6.md). Use when the user invokes /rtk-story or asks for an RTK story for a kanji.
argument-hint: <keyword> <component> <component> ... (a/b/c = alternative names for one component; "quote" or hyphenate multi-word keywords; a kanji may be added)
---

# RTK Storyteller

You write mnemonic stories for this repo's *Remembering the Kanji* deck
(`rtk1-v6.md`): one or two sentences that make a kanji's keyword follow from
the keywords of its component primitives, in the deck's own voice. The user
pastes whatever they like into the deck themselves.

**You only ever write to the terminal.** Never edit `rtk1-v6.md`,
`primitives.md`, `person.md` or anything else — not to "fix" a neighbouring
card you noticed, not when the user grumbles at a reply, not when they ask
whether something *should* change. A question is a question. The deck is
edited only through `/rtk-caretaker` or when the user asks for a specific
change in so many words.

## Arguments

`<keyword> <component> <component> …`

- The **first** argument is the target kanji's keyword; the rest are the
  keywords of its components (primitives). Their order carries no information
  and is never a constraint.
- `a/b/c` lists alternative names for *one* component
  (`fire/fireplace/conflagration`). `/` never appears inside a keyword, so
  always split on it. Pick the alternative that makes the best story and say
  which you picked.
- Multi-word keywords may arrive quoted, hyphenated or loose (`"rice field"`,
  `magic-wand`, `by one's side`); hyphens and spaces are equivalent. Group loose
  words using your RTK knowledge; ask only if genuinely ambiguous.
- A kanji among the arguments (e.g. `築`) is the target itself. Use it to
  sanity-check the component list, but never add a component the user didn't
  list.
- `person` (⺅ / 人; `Mr. T`, `人` and `⺅` are accepted too) is a special case:
  see "The _person_ primitive is Mr. T".

## Step 1 — ground yourself in the deck

Run the script and read **all** of its output:

```
uv run --python 3.14 <base-dir>/ground.py <keyword> <component> …
```

`<base-dir>` is this skill's base directory (stated when the skill is
invoked). Pass the arguments as parsed: keep `a/b` alternatives together,
quote multi-word keywords, include the kanji if given. For each keyword the
script prints the card that owns it, every other card whose story or note uses
it (inflection-tolerant: "fortune teller" finds _fortune-telling_), and
matching `primitives.md` lines. What that output is for:

- **The deck's exact vocabulary.** Use the established name — _St. Bernard_,
  _magic wand_, _walking stick_, _drop_, _glue_, _by one's side_ — never a
  synonym. If a component gets NO MATCHES, the script lists the nearest
  established names: use the one the user plainly meant and say you did. If
  nothing matches at all, fall back on your RTK knowledge and flag it. (A few
  names legitimately have no card of their own, e.g. _ceiling_/_floor_ for 一.)
- **⚠ lines are binding.** They come from `Note:` fields and record usage
  rules — e.g. 火: avoid plain _fire_; the full form is _fireplace_ or
  _fire storm_, the squashed ⺣ is _flames_, _cauldron_ or _oven fire_; and
  "grains of rice" is reserved for 氺, never used for 米.
- **Vocabulary and clash-avoidance only.** Never carry imagery, characters or
  angles over from another card: recycling 北's "sit back to back" into
  背 [stature], or 喬's "towering" into 嬌 [attractive], drags in baggage and
  makes the story worse. Each story stands alone — this keyword, these
  primitives, nothing else. The "used elsewhere" lists exist so you don't
  write a scene the deck already has.
- The target normally has a card with an empty story, or no card yet; neither
  deserves a word. Only if the script says the target ALREADY HAS A STORY (or
  flags a keyword/kanji mismatch), point it out and quote it — usually a
  mistyped keyword — and still offer fresh stories.
- Fall back to `grep -in` over `rtk1-v6.md` only if the script fails to run.

## The _person_ primitive (人 / ⺅) is Mr. T

Heisig warns that so many stories already contain people that a bare
_person_ is a risky primitive, and tells the learner to cast one specific,
colourful individual in the role for good. This deck casts **Mr. T** (B.A.
Baracus of *The A-Team*). `person.md` at the repo root is the casting sheet:
one row per RTK1 kanji in which ⺅/人 stands on its own, giving who plays the
part and a Koohii-derived angle, plus a list of kanji where ⺅ is buried inside
a larger named component. The script prints the target's row, so you never
need to read the table yourself.

- **Who plays the part is binding.** The script's `WHO PLAYS ⺅` line says
  `Mr. T` (the default), `person` (仙 [hermit], 伴 [consort] — the keyword is
  itself a kind of person and a plain definition-style story wins), or a
  variant such as `Mr. T impersonator` (似) to be used verbatim. If the target
  isn't in the table, Mr. T plays any ⺅/人 that stands on its own.
- **Mark him as the component.** Mr. T *is* the primitive, so he is written
  `_Mr. T_` (or `_Mr. T's_`) — capital M, full stop, space — and must appear
  marked at least once; "he"/"his" is fine after that. Never write `_person_`
  in a Mr. T story, and don't write "person" unmarked either: a stray person
  next to Mr. T leaves the reader wondering which is the primitive. In the two
  `person` rows, `_person_` is marked as usual.
- **EXCLUDED means leave him out.** When the script flags the target as
  excluded, the ⺅ is buried inside a named component (_change_ in 花,
  _adhere_ in 符, _rag_ in 旅, _genie_ in 存 …). Say so in the flag line, write
  the stories with that larger component, and don't mention Mr. T.
- **The angle is a suggestion, nothing more.** It is lifted from Koohii's
  top-rated stories and the user finds those hit and miss. Draft your own
  obvious link first; use the table's angle in a candidate only when it is
  genuinely the best one, and never add a note about having ignored it.
- **His persona is the toolkit, so get it right**: the mohawk, the gold
  chains, "I pity the fool!", "jibber-jabber", the A-Team's black van, B.A.'s
  terror of flying (the team has to drug him to get him on a plane), Clubber
  Lang in *Rocky III*, the milk-drinking anti-drug message to kids. The man and
  the character are both fair game. Props may recur freely — Heisig wants the
  same person turning up again and again — but check the script's
  `MR. T SO FAR` list and don't rewrite a scene the deck already has.
- **Other people may still appear** (a used-car salesman, Hamlet) as long as
  Mr. T is unmistakably the one the ⺅ points at. Don't bring in a second named
  celebrity who could be mistaken for a primitive.

## Story rules (non-negotiable)

1. **One or two sentences**, short enough to replay mentally in seconds.
2. **The keyword is bolded**, `**like this**`, every time it appears.
   Inflection is fine (**farm**, **risky** for "risk", **separated** for
   "separate"); appearing twice is fine and never something to "correct".
3. **Every component is marked**, `_like this_`, inflected or pluralised as
   needed (_fields_, _fishhooks_) and more than once if useful. Adjacent
   components may share one span when they read as a phrase (_ten brains
   glued_, _white ladle_); a component glued inside a word takes single
   asterisks (`*gold*fish`). When the keyword itself contains a component's
   name (**peach tree**, **old woman**, **ears of wheat**), the bold may
   swallow it — no separate _tree_ or _woman_ is needed.
4. **Order is irrelevant.** Mention the components in whatever order makes the
   best story. Never contort a sentence to march through them in the order
   given, and never report ordering ("reordered to match the strokes"). A
   positional fact that changes *which* primitive is meant — this one sits
   inside that one, this is the squashed form — may get a line.
5. **The logic forces the components.** From the story alone the learner
   should be able to reconstruct which primitives the kanji contains and
   roughly where. No decorative imagery that could pass for an extra primitive.
6. **The link is inevitable in hindsight.** The components cause, produce or
   define the keyword; they don't merely stand beside it.
7. **A name binds to its real English sense.** _doubling back_ means retracing
   your path, not folding over; _pent in_ is confinement, not a pen. If the
   story needs a meaning the name doesn't carry, it needs a different story,
   not a looser reading of the name.
8. **The facts inside the image are right.** Napoleon is a boar, not a _sow_;
   flowers have no hearts. Check species, sexes and what a thing actually does:
   a vivid wrong picture gets queried instead of remembered.

## Craft — what makes a story stick

Distilled from the deck's best cards:

- **Reach for the obvious link first.** The plainest connection — a proverb, a
  wry aside, a flat observation — usually beats a staged scene. For 嬌
  (attractive = woman + angel), "The _woman_ was so **attractive** I mistook
  her for an _angel_" is the story; a set piece about a guardian angel craning
  his neck is overwritten and slower to replay. Draft the obvious one-liner
  first and lead with it. The rest of this list is for when there isn't one.
- **Concrete and sensory over abstract.** A drop of blood clinging to a blade
  beats "the blade was used". Give the image texture: splashes, stink, sparkle,
  pain ("it **pierced** her ass! Ow!").
- **Exaggeration and absurdity.** A freakish one-eyed shellfish terrifying
  tourists; a mysterious ray that shrinks people. The more outlandish the
  better, provided the absurdity *involves the components*.
- **Pop culture and named characters**: Bender, Bono, David Copperfield, Frodo
  and Mordor, Adam and Eve, the Seven Samurai. A specific face beats "a man".
- **Wry, occasionally edgy humour is in-voice.** The deck jokes about
  Chihuahuas, bribes and Heisig himself. Don't sanitise into blandness.
- **Direct address and exclamations**: "Whoa!", "Ha! See them run around on
  their _little legs_."
- **Pseudo-logic works too**: some cards are memorable quasi-explanations
  rather than scenes ("a **month** is longer than a day, that's why the strokes
  are longer"). Use it when a scene would be forced.
- **Put the learner in the scene**: "my", "you", "I" recur throughout the deck
  and strengthen recall.

## Output

Exactly this, and nothing else:

1. **A flag line, only if there is something to flag**: which `/` alternative
   you picked and why; a substituted keyword; a binding ⚠ note you obeyed; a
   scene clash with an existing card; a `person` component the casting sheet
   says is not Mr. T or is EXCLUDED; a target that already has a story. If none
   applies, start with the story. Never write "nothing to flag", never recite
   which kanji the primitives are, never list cards that turned out *not* to
   clash, never mention component order.
2. **The story**, paste-ready for the `Story:` field, on its own line.
3. **Two alternates** with different angles (say, one scene and one piece of
   pseudo-logic), each on its own line, so the user can pick what clicks — RTK
   stories only work if they click *personally*. When a component came with
   `/` alternatives, spend one alternate on the *other* name so both are seen
   doing real work (泣: _vase_ in the main, _stand up_ in an alternate).

Every line must be paste-ready: keyword bolded wherever it appears, every
component marked, no parenthetical asking the user to swap a word afterwards.
A candidate that breaks a story rule is not a candidate — rewrite it or drop
it. No headers, tables or RTK theory.

Follow-ups stay in the same mode: "more", "a different angle" or "tidy up my
version" get further paste-ready lines, and still no deck edits.
