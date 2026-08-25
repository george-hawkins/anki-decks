---
name: rtk-caretaker
description: Audit this repo's RTK deck (rtk1-v6.md) for broken cards, mismarked keywords, out-of-sync kanji/keyword/story triples, duplicates, typos and clumsy grammar; fix the unambiguous ones automatically and report what needs your decision. Use when the user invokes /rtk-caretaker or asks for a check-up, review or proof-read of the deck.
argument-hint: "[nothing = whole deck] | recent | 341-360 | 硝 | nitrate"
---

# RTK Deck Caretaker

You are the proof-reader of this repo's deck (`rtk1-v6.md`), a hand-written
*Remembering the Kanji* deck in Anki markdown-import form. Find what is broken
or off-key, **fix the mechanical half yourself, without asking**, and **report
the half that needs the user's judgment** — in severity order, with line
numbers.

Two rules about touching things:

- **Never commit, never push, never stage.** Fixing the deck is in scope;
  recording it in git is the user's call, always. Don't run `git commit`,
  `git add` or `git push`, and don't offer to.
- **Only ever edit `rtk1-v6.md` and this skill's own `wordlist.txt` /
  `reported.tsv` / `audited.tsv`.** `primitives.md`, the backups and the exports are read-only
  reference.

The deck lives in git and is pushed to GitHub, so an edit is recoverable — that
is why mechanical fixes are offered up front rather than hedged.

## Card format

Each card is a `START` … `END` block, in RTK frame order, one blank line
between blocks:

```
START
Japanese RTK
Keyword: nitrate
Clue:
Kanji: 硝
Story: The miner held a _candle_ to the newly mined _stones_ to check for **nitrate**. Too much though and it might explode!
Note: introduces non-jōyō kanji 卆 as primitive meaning _game of cricket_.
<!--ID: 1785183563274-->
END
```

- `Japanese RTK` is the note type; the five fields always appear in the order
  `Keyword, Clue, Kanji, Story, Note`; the `<!--ID: …-->` comment is Anki's note
  id and must be unique and last.
- **`Keyword`, `Kanji` and `Story` are mandatory and non-empty** — a card with
  no story still says `[no story]`. `Keyword` must additionally be unique across
  the deck, as must `Kanji`. These are invariants, never judgment calls: a blank
  `Kanji:` or a duplicated keyword gets filled in or fixed like any other
  mechanical error. **An empty `Story` is the exception** — never write
  `[no story]` yourself. Marking a card as deliberately storyless is the user's
  decision to make, so report it and leave it. So is a **misspelled `Keyword`** — the
  keyword is the front of the card, and `check.py` feeds every keyword into the
  spell checker's dictionary, so K009 is the only thing that can catch it.
- `Update:` is an accepted sixth field, after `Note`, holding a later second
  thought about the card (see 可 [can]). It is optional, follows the same
  conventions as `Note`, and is never a finding in itself — but any *other*
  field label is.
- `Clue` is usually empty; it disambiguates a keyword when needed
  (`not OLD MAN`, `think area of expertise`). It is a terse aside, not a
  sentence: it **never ends in a full stop** (dropping a trailing `.` is a
  mechanical fix) and it **never contains parentheses** — the card renders the
  Clue already wrapped in parentheses, so inner ones look odd. Report those for
  the user to reword rather than touching them yourself, and say briefly *why*
  (the rendering), since it is easy to forget.
- `Story` and `Note` may run onto continuation lines. `Note` is free-form: it
  declares primitive meanings, records stroke-order and etymology asides, and
  warns about confusable characters.
- A `Story` opens with a capital and closes with punctuation — including when
  the keyword comes first (`**Nightbreak** happens when …`) — while a `Note`
  opens in lowercase, proper nouns, `I` and ALL-CAPS keyword references
  excepted. All three are mechanical fixes. The exception: a sentence that ends
  on a kanji or kana character (`… written 上`) needs no full stop — leave it
  alone, in a `Story` or a `Note`.
- In a story, **the keyword is wrapped in `**bold**`** (once) and **each
  component primitive in `_underscores_`** — or `*single asterisks*` where the
  component is glued inside a larger word (`*gold*fish`, `*water*-pistol`,
  `*king*-size`).
- A card with no story yet says exactly `[no story]`, optionally with a hint:
  `[no story - but think _vermilion_]`. That is fine and not a finding.
- Not every story has component markup: early pictogram frames (日, 木, 川) and
  the odd pseudo-explanation legitimately have none.

## Pass 1 — run the mechanical checks

```
uv run --python 3.14 <base-dir>/check.py [scope] [--dump]
```

`<base-dir>` is this skill's base directory (stated when the skill is invoked).
Read the **entire** output. Scope arguments, mapped from what the user asked
for:

| user says | flag |
| --- | --- |
| nothing | *(omit — the cards pass 2 has not signed off on; see the audit ledger)* |
| "everything", "the whole deck", "a full audit" | `--all` |
| "the new batch", "recent", "what I just added" | `--recent` (working-tree diff, else the last commit) |
| "341-360", "the last twenty" | `--range 341-360`, `--last 20` |
| a kanji or keyword | `--kanji 硝`, `--keyword nitrate` |

Useful extras: `--dump` prints the in-scope cards verbatim (saves a separate
read for pass 2), `--vocab` adds a noisier check for component wording the deck
has not established elsewhere, `--no-spell` skips spelling.

Scope limits *reporting and reading*, never parsing: the script always reads the
whole file, so duplicate keywords, duplicate kanji and duplicate ids are caught
across the entire deck however narrow the scope, and the `reported.tsv` prune
still sees every card.

The script needs `aspell` (`brew install aspell`) and exits with an error
without it — say so rather than silently skipping the spell check.

The report groups findings as **ERROR** (breaks the Anki import or a deck
invariant: missing/duplicate fields, duplicate note ids, duplicate keyword or
kanji, a Kanji field that is not one kanji), **WARN** (almost certainly a
mistake: keyword not bolded, keyword marked as a component, bold on something
that is not the keyword, unbalanced markers, misspellings, duplicated stories,
a Story that starts lowercase or ends unpunctuated — unless it ends on a kanji
or kana character, which the script accepts as-is — a Note that starts
capitalized, a Clue that ends in a full stop or contains parentheses, a
misspelled Keyword) and **INFO** (often deliberate: no component markup, an ID
out of sequence, a keyword that doubles as a primitive name).

A keyword bolded more than once is not a finding — the deck does it on purpose.

Treat the codes as *claims to verify*, not verdicts. Check each one against the
card before repeating it, and drop the ones that are actually fine — say how
many you dropped rather than listing them.

The output opens with an **ALREADY REPORTED** section (see below). Everything
listed there is off limits for this run's report — including the judgment
findings, which the script cannot filter for you.

## Pass 2 — read the cards and judge

The script cannot tell whether a story is *about the right character*. That is
the part that matters most, so read the cards in scope (`--dump` output, or
`Read` the line ranges) and check each triple:

1. **Kanji ↔ Keyword.** Is that Heisig's v6 keyword for that character, and is
   the character the jōyō form? A card copied from its neighbour and then
   half-edited is the classic failure. Only raise a keyword/character mismatch
   when you are genuinely confident.
2. **Story ↔ Kanji.** Do the marked components actually make up the character,
   and are any real components missing from the story? Allow the deck's
   licence: 一/丨 filler strokes, "horns can't float free" cases, and elements
   too awkward to name are routinely skipped — the user's rule is a *little*
   leeway. A component the character does not contain is a real finding; so is
   a story whose primitives belong to a different kanji.
3. **Story ↔ Keyword.** Does the story earn *this* keyword, rather than a
   neighbouring frame's? A story that reads as a definition of another card's
   keyword is a copy-paste symptom.
4. **Established vocabulary.** Primitive names should match what the deck
   already uses (`_St. Bernard_`, `_magic wand_`, `_by one's side_`,
   `_vermilion_`, `_housetop_`). A synonym invented for one card
   (`_home_` for 宀, `_middle_` for 中 where the Note says use _in_) weakens
   recall — flag it, quoting the established name. Notes marked with usage
   warnings (e.g. 火: don't use plain _fire_) are binding.
5. **Note ↔ Story.** Notes that contradict the story, or claim something plainly
   wrong about a character. Don't fact-check etymology you are unsure of.
6. **Grammar and typos — be lenient.** Flag real errors: a missing or repeated
   word, subject/verb disagreement, a mangled clause, the wrong homophone, a
   misspelling. Do **not** flag informal register, comma splices, sentence
   fragments, a lowercase opening, a missing final full stop, dashes used as
   punctuation, exclamations, or the deck's edgy humour. Casual speech and a
   little punctuation abuse are the house style; only call out what actually
   trips a reader.
7. **Markup judgment.** Keyword in `**bold**` exactly once, components in
   `_…_`/`*…*`; bold on a non-keyword word (`**opening**` on the card for
   *stone*) is a finding; a keyword doubling as a genuine primitive name
   (具: `**tools**` … `_tool_` table) is not.
8. **Duplication.** Repeated keywords or kanji are errors the script catches;
   also watch for two cards leaning on the same image or scene in a way that
   would blur them, and for near-identical stories. A deliberate contrast pair
   (未/末) is fine when the Note says so.

For a whole-deck run, work through the file in chunks of roughly 100 cards so
nothing is skimmed, and keep a running list. Don't re-derive the mechanical
findings while doing this — they are already in hand.

## Reporting: fix what is unambiguous, report the rest

Sort every finding by two questions — *is it definitely wrong?* and *is there
exactly one obvious fix?* — into three piles.

**1. Fix it yourself.** Definitely wrong, one obvious correction, no taste
required: a misspelling (in a `Story`, a `Note` or the `Keyword` itself), a
stray or duplicated field line, `_keyword_` that should be `**keyword**`, bold
on a word that plainly isn't the keyword, an unbalanced or space-padded marker,
a doubled word, a punctuation slip, a field label Anki won't import, an
unemphasized keyword that only needs wrapping, a trailing full stop on a
`Clue`, an empty `Kanji` whose character is obvious from the keyword and story.
**Apply these before you write the report, without asking and without listing
them** — quietly and exactly, one `Edit` per card, changing nothing else on the
line. They are not part of the report; one closing line saying how many you
applied is enough.

**2. Must-fix.** Definitely wrong — an invariant is broken or the card teaches
something false — but choosing the repair is the user's:

- duplicate `Keyword` or duplicate `Kanji`: which card is the mistake, and what
  it should have been, is theirs to say;
- duplicate note id: Anki would merge the two notes on import;
- empty `Kanji` where the character is *not* inferable, or a `Kanji` field
  holding several characters with no obvious winner;
- empty `Keyword` — Heisig's keyword is often recoverable, but a wrong guess
  plants a false keyword;
- empty `Story` — never write `[no story]` yourself (see Card format);
- a story whose primitives compose some *other* character — the copy-paste-then-
  half-edit failure;
- a `Keyword` that is not Heisig's v6 keyword for that character, or a `Kanji`
  that is not the jōyō form.

These are not suggestions. Report them first, say plainly that the deck stays
broken until each is resolved, and name the repair you would make — but do not
apply it and do not ask to.

**3. Judgment calls.** Arguably off, and reasonable people could leave them:
missing or phantom components, a keyword that appears nowhere in the story,
invented primitive vocabulary, grammar that wants recasting, a near-duplicate
story, a `Clue` with parentheses in it. Note that mismarked components and
absent keywords live *here*, not in must-fix: the store shows the user
knowingly keeping several (戚, 語, 成, 弐), so the deck's rule is a little
leeway, not a hard invariant.

Piles 2 and 3 are the report. Most serious first, one line each:
`rtk1-v6.md:LINE` + `#card 漢 [keyword]` + what is wrong + the concrete fix,
quoting the replacement story text where a rewrite is the answer. Group
identical findings instead of repeating the explanation.

**Applying piles 2 and 3 is not your job.** Report them and stop. Don't apply
them, don't offer to, and don't close by asking which ones the user wants done
— they do the applying themselves, in their own time, and an unanswered
question just adds a round trip. A later message asking you to make a specific
change is of course an instruction like any other; a blanket "fix the
mechanical stuff" is not.

Close with a one-line tally that includes the count of fixes you applied. If the
deck is clean, say so plainly. Don't paste the script's raw output back at the
user, and don't pad with praise.

## Reading each card once: the audit ledger

`audited.tsv` beside this skill records which cards pass 2 has actually read
and what they contained at the time — a hash of `Keyword`/`Clue`/`Kanji`/
`Story`/`Note`/`Update`, with the `<!--ID:-->` comment deliberately excluded so
importing into Anki never invalidates it. **With no scope flag, the run covers
exactly the cards missing from that ledger**: brand new cards, cards edited
since they were last read, and everything if the ledger doesn't exist yet. This
is what keeps a full audit affordable as the deck grows; pass 1 is cheap and
runs over everything regardless.

At the **end** of a run — after the fixes are applied and the report is
written — stamp what you read:

```
uv run --python 3.14 <base-dir>/check.py [same scope flags] --mark-audited \
    [--skip 漢漢]
```

- `--skip` takes the kanji of any card left in a **must-fix** state. Never stamp
  those: an unstamped card comes back on the next run, which is exactly what a
  broken card should do. Judgment calls *are* stamped — `reported.tsv` is what
  keeps those quiet, and it stays quiet for as long as the user leaves the card
  alone.
- Stamp only what you genuinely read. A run scoped with `--kanji 硝` stamps one
  card, not the deck.
- **Bump `CHECKS_VERSION` in `check.py` whenever you add or change a check.**
  Every ledger entry written by an older version is then treated as unaudited,
  so the new check gets its chance over cards signed off before it existed.

The two stores answer different questions and neither can stand in for the
other: `audited.tsv` says *"this card has been looked at, at this exact
content"*, `reported.tsv` says *"this particular advice was heard and
declined"*. Absence from `reported.tsv` never means a card is fine — it may
just mean nobody has read it yet.

## Saying it once: the already-reported store

`reported.tsv` beside this skill is the memory of what has already been raised.
Silence is the point: a suggestion the user didn't act on is a suggestion they
don't want to hear again.

- **Before reporting**, drop anything the run's ALREADY REPORTED section covers.
- **After reporting**, append one line per *judgment* finding you raised —
  tab separated, `kanji`, a check code or `-`, a snippet, and the reason:

  ```
  亭	-	_Crown street_	'Crown' reads as the 冖 crown primitive, which 亭 lacks
  ```

  The snippet is the hinge: quote text from the card that would *change* if the
  advice were taken (the marked-up phrase, not a whole sentence). If a finding
  came from a check code, record the code so the script suppresses it too; if
  it covers a pair of cards (a duplicated story), write one line per card.
  Mechanical fixes need no entry — they are already fixed.
- **Pruning happens by itself.** On each run the script checks every snippet
  against its card; when a snippet is gone the advice was evidently taken and
  the entry is deleted, listed under DROPPED FROM THE STORE. Mention those in a
  closing line — they are the things the user fixed since last time.
- If you *do* re-raise something deliberately (the user asked, or the card
  changed enough to make it a different problem), say that you are doing so.
- **A must-fix finding that ends up in the store is a bug in this skill, not a
  stubborn user.** Everything in `reported.tsv` was, by definition, something
  they chose to live with — so if pile 2 keeps landing there, that class of
  finding was never really must-fix. When you write such an entry, say so in a
  closing line and propose the amendment to this file (demote the class to a
  judgment call, or narrow it until it only catches the genuinely broken case).

## Maintaining the wordlist

`wordlist.txt` beside this skill holds vocabulary aspell does not know: the
names the stories borrow (Frodo, Momotarō, Geppetto), deck jargon (jōyō, Koohii)
and modern words missing from aspell's dictionary. Heisig's keywords are added
automatically.

When a run flags a word that is genuinely fine and will recur, append the base
form (lowercase, alphabetical) yourself — no need to ask — and mention it in a
single closing line. Judge it: a name, a brand, a loanword or a real word
aspell simply lacks belongs in the file; a word that is only *probably* right,
or that appears once, is better raised in the report. Never add a word to
silence a finding you haven't checked.
