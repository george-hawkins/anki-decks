# Mr. T stories

One block per RTK1 kanji in which Mr. T plays ⺅, i.e. every row of the table in person.md except hermit (仙) and consort (伴), plus seven kanji (久 囚 内 丙 以 不 幾) that rtk1-frames.json lists with a *person* primitive but person.md omits; those carry a flag line. Generated in bulk with /rtk-story on 2026-10-27. Nothing here is in rtk1-v6.md unless the block says `status: in deck`, in which case the single story listed is the deck's.

Block format, deliberately like rtk1-frames.md so it is easy to parse:

    ## <frame> <kanji> <keyword>
    primitives: <Heisig's list, copied from rtk1-frames.md>
    components: <the names the stories actually mark, in deck vocabulary; a/b lists the forms used>
    status: candidates | in deck
    flag: <optional, one line>
    - <story, paste-ready for a Story: field>
    - <story>
    - <story>

Each candidate carries a `score:` line, 0 to 1, estimating how likely the user is to pick that line (verbatim or lightly edited) for the deck. The scale is stretched: 1.0 corresponds to a likelihood of about 45%, which is as high as any story here is judged to reach, and 0.5 to about 22%, a little above the 18% that offered stories have historically achieved. The score is the product of two parts, divided by that cap. The first is a judged quality rating J from 0 to 10 (does the link force the keyword, are the components literal, is it one plain beat, does the image click, does Mr. T sit naturally), mapped to a likelihood by 0.02 + 0.006 J². The second is a surface prior fitted by logistic regression to the 885 candidates offered in earlier sessions and whether each survived: it rewards 13 to 18 words and penalises a second sentence, a colon, a question, a quote or a parenthesis, and is expressed as a ratio to the 18% base rate. The J rating is recorded in the score line as `(J n)` so the score can be regenerated. Scores are for ranking within and across blocks, not for pasting. The scripts, the fitted prior and a fuller description are in `.claude/skills/rtk-story/bulk/`.

Primitives whose own kanji is beyond the deck's current frame (puzzle, yarn, blame, surface, dedicate, cabbage, Old West, jail cell, dart, locket, awl, move, stamps, pup tent, shape, strung together, scrapbook, door, calling card, director, do, elephant, saw, mop, demand, broom, screwdriver, once upon a time, leg, by means of, in a row upside down) use Heisig's name and may need renaming when the deck reaches them.

## 1024 佐 assistant
primitives: person, left
components: Mr. T, left
status: in deck
- _Mr. T_ keeps his **assistant** on his _left_, within reach but out of his way.

## 1025 侶 partner
primitives: person, spine
components: Mr. T, spine
status: in deck
- Only someone with a _spine_ of steel would volunteer to be _Mr. T's_ **partner**.

## 1026 但 however
primitives: person, nightbreak
components: Mr. T, nightbreak
status: candidates
- _Mr. T_ says he's a night owl, **however** he's never once slept through _nightbreak_.
  score: 0.74 (J 6)
- _Mr. T_ agreed to the plan, **however** by _nightbreak_ he had changed his mind.
  score: 0.54 (J 5)
- **However** late _Mr. T_ gets in, _nightbreak_ finds him up and dressed.
  score: 0.67 (J 6)

## 1027 住 dwell
primitives: person, candlestick
components: Mr. T, candlestick
status: candidates
- _Mr. T_ **dwells** in a lighthouse, the lamp is just a _candlestick_ he holds up all night.
  score: 0.80 (J 6)
- You can tell where _Mr. T_ **dwells** by the _candlestick_ burning in the window every night.
  score: 0.67 (J 6)
- A **dwelling** is anywhere _Mr. T_ has set down his _candlestick_ and called it home.
  score: 0.57 (J 5)

## 1028 位 rank
primitives: person, vase
components: Mr. T, vase/stand up
status: candidates
- _Mr. T's_ **rank** in the army is shown by the size of the _vase_ on his desk.
  score: 0.57 (J 5)
- _Mr. T_ pulled **rank** and took the biggest _vase_ for himself.
  score: 0.67 (J 6)
- **Rank** in the army comes with a _vase_, and _Mr. T's_ needs two men to carry it.
  score: 0.80 (J 6)

## 1029 仲 go-between
primitives: person, in
components: Mr. T, in
status: candidates
- _Mr. T_ is the **go-between**, he carries the message _in_ and the answer back out.
  score: 0.80 (J 6)
- A **go-between** is someone like _Mr. T_ who can get _in_ to see both sides.
  score: 0.57 (J 5)
- When the two gangs wouldn't talk, _Mr. T_ went _in_ as the **go-between**.
  score: 0.54 (J 5)

## 1030 体 body
primitives: person, book
components: Mr. T, book
status: candidates
- _Mr. T_ built his **body** without ever opening a _book_ on it.
  score: 0.67 (J 6)
- _Mr. T's_ **body** is on the cover of every _book_ about weight training.
  score: 0.57 (J 5)
- _Mr. T's_ **body** was so big the anatomy _book_ needed a fold-out page.
  score: 0.99 (J 7)

## 1031 悠 remote
primitives: person, walking stick, taskmaster, heart
components: Mr. T, walking stick, taskmaster, heart
status: candidates
- _Mr. T's_ _taskmaster_ has a _walking stick_, a bad _heart_ and a cabin so **remote** nobody visits.
  score: 0.54 (J 5)
- _Mr. T's_ _heart_ was set on somewhere **remote**, so he took a _walking stick_ and left the _taskmaster_ behind.
  score: 0.29 (J 4)
- The _taskmaster_ sent _Mr. T_ and his _walking stick_ to the most **remote** post he could find, to break his _heart_.
  score: 0.29 (J 4)

## 1032 件 affair
primitives: person, cow
components: Mr. T, cow
status: candidates
- _Mr. T_ denies the **affair**, but the _cow's_ calf was born with a mohawk.
  score: 0.99 (J 7)
- The _cow_ **affair** is the one thing _Mr. T_ won't talk about.
  score: 0.52 (J 5)
- Half of _Mr. T's_ **affairs** are about _cows_, the ranch doesn't run itself.
  score: 0.39 (J 4)

## 1033 仕 attend
primitives: person, samurai
components: Mr. T, samurai
status: candidates
- _Mr. T_ **attends** the _samurai_, carrying his swords and pouring his tea.
  score: 0.67 (J 6)
- To **attend** a _samurai_ you walk three steps behind him, which _Mr. T_ hated.
  score: 0.48 (J 5)
- _Mr. T_ **attends** the _samurai_, carries his swords and pours his tea without being asked.
  score: 0.74 (J 6)

## 1034 他 other
primitives: person, scorpion
components: Mr. T, scorpion
status: candidates
- _Mr. T_ shook one _scorpion_ out of his boot and stood on the **other**.
  score: 0.74 (J 6)
- _Mr. T_ kept one _scorpion_ as a pet and ate the **other**.
  score: 0.89 (J 7)
- Every **other** _scorpion_ in the desert has tried to sting _Mr. T_ and died.
  score: 0.23 (J 3)

## 1035 伏 prostrated
primitives: person, chihuahua
components: Mr. T, chihuahua
status: candidates
- _Mr. T_ lay **prostrated** on the floor so the _chihuahua_ could lick his face.
  score: 0.74 (J 6)
- Even a _chihuahua_ goes **prostrated**, belly to the floor, when _Mr. T_ walks in.
  score: 0.74 (J 6)
- **Prostrated** means flat on your face, like _Mr. T_ after tripping over the _chihuahua_.
  score: 0.52 (J 5)

## 1036 伝 transmit
primitives: person, rising cloud
components: Mr. T, rising cloud
status: candidates
- _Mr. T_ **transmits** his messages the old way, by _rising clouds_ of smoke.
  score: 0.74 (J 6)
- A _rising cloud_ of smoke is how _Mr. T_ **transmits** that the barn is on fire.
  score: 0.54 (J 5)
- _Mr. T_ **transmits** the dinner call to the camp with a single _rising cloud_.
  score: 0.54 (J 5)

## 1037 仏 Buddha
primitives: person, elbow
components: Mr. T, elbow
status: candidates
- _Mr. T_ nudged the **Buddha** with his _elbow_ to see if he was still meditating.
  score: 1.00 (J 7)
- _Mr. T_ shoved past the **Buddha** with an _elbow_ and the **Buddha** just smiled.
  score: 0.55 (J 5)
- **Buddha** had the calm, _Mr. T_ had the _elbows_, the fight was short.
  score: 0.37 (J 4)

## 1038 休 rest
primitives: person, tree
components: Mr. T, tree
status: candidates
- _Mr. T_ sat down for a **rest** with his back against a _tree_, and the _tree_ gave first.
  score: 0.74 (J 6)
- A **rest** for _Mr. T_ is five minutes in the shade of a _tree_, then back to work.
  score: 0.57 (J 5)
- Lumberjacks **rest** against a _tree_, _Mr. T_ **rests** by pulling one up and sitting on it.
  score: 0.37 (J 4)

## 1039 仮 provisional
primitives: person, anti
components: Mr. T, anti
status: candidates
- _Mr. T_ is _anti_ anything **provisional**, he does things once and for good.
  score: 0.57 (J 5)
- The **provisional** government lasted a week, _Mr. T_ was _anti_ it from day one.
  score: 0.54 (J 5)
- _Mr. T_ turned down the **provisional** contract, he's _anti_ anything that can be taken back.
  score: 0.74 (J 6)

## 1040 伎 performing artist
primitives: person, branch
components: Mr. T, branch
status: candidates
- _Mr. T_ became a **performing artist** by dancing on a _branch_ without breaking it.
  score: 0.54 (J 5)
- A **performing artist** is anyone like _Mr. T_ who can sing while swinging from a _branch_.
  score: 0.39 (J 4)
- _Mr. T_ snapped the _branch_ he was dancing on, which ended his career as a **performing artist**.
  score: 0.74 (J 6)

## 1041 伯 chief
primitives: person, white dove
components: Mr. T, dove/white bird
status: candidates
flag: the deck names 白 _white_, _white bird_ or _dove_, not "white dove"
- The tribe's **chief** is whoever the _white bird_ lands on, and it landed on _Mr. T_.
  score: 0.80 (J 6)
- _Mr. T_ became **chief** of the tribe by wearing a _white bird_ on his head.
  score: 0.54 (J 5)
- A **chief** sends out a _dove_ to make peace, _Mr. T_ sends it out to pick a fight.
  score: 0.54 (J 5)

## 1042 俗 vulgar
primitives: person, valley
components: Mr. T, valley
status: candidates
- _Mr. T_ shouted something **vulgar** into the _valley_ and the echo repeated it for a minute.
  score: 0.74 (J 6)
- Everyone in the _valley_ is **vulgar**, so _Mr. T_ fits right in.
  score: 0.67 (J 6)
- _Mr. T_ was run out of the _valley_ for being **vulgar**, by people who swear at their cows.
  score: 0.37 (J 4)

## 1043 信 faith
primitives: person, words
components: Mr. T, words
status: candidates
- _Mr. T_ gives you his _word_ and that's all the **faith** you need.
  score: 0.89 (J 7)
- _Mr. T_ put his **faith** in the _words_ on the map and drove into a lake.
  score: 0.54 (J 5)
- **Faith** is believing a man's _words_ before he's done anything, and _Mr. T_ doesn't give it cheaply.
  score: 0.39 (J 4)

## 1044 佳 excellent
primitives: person, ivy
components: Mr. T, ivy
status: candidates
- _Mr. T_ got an **excellent** grade for climbing the _ivy_ instead of taking the stairs.
  score: 0.54 (J 5)
- _Mr. T_ got into an **excellent** college, he climbed in over the _ivy_.
  score: 0.74 (J 6)
- _Mr. T_ is an **excellent** gardener, his _ivy_ climbs exactly where he tells it to.
  score: 0.39 (J 4)

## 1045 依 reliant
primitives: person, garment
components: Mr. T, garment
status: candidates
- _Mr. T_ is **reliant** on one _garment_, a vest, he owns nothing else to wear.
  score: 0.57 (J 5)
- Being **reliant** on a single _garment_, _Mr. T_ washes it while he's wearing it.
  score: 0.74 (J 6)
- A man like _Mr. T_ is not **reliant** on anyone, except the tailor who makes his _garments_.
  score: 0.39 (J 4)

## 1046 例 example
primitives: person, file
components: Mr. T, file
status: candidates
- An **example** is what _Mr. T_ makes of the first man in the _file_ who steps out of line.
  score: 0.64 (J 6)
- _Mr. T_ picks one man out of the _file_ and makes an **example** of him.
  score: 0.74 (J 6)
- Walking down a _file_ of recruits, _Mr. T_ pulls out one as an **example** of what he wants.
  score: 0.54 (J 5)

## 1047 個 individual
primitives: person, harden
components: Mr. T, harden
status: candidates
- _Mr. T_ was _hardened_ by the army into a single, solid **individual**.
  score: 0.48 (J 5)
- Every **individual** in _Mr. T's_ squad was _hardened_ by him personally.
  score: 0.48 (J 5)
- _Mr. T_ was _hardened_ young, and came out an **individual** who takes orders from nobody.
  score: 0.74 (J 6)

## 1048 健 healthy
primitives: person, build
components: Mr. T, build
status: candidates
- _Mr. T_ stays **healthy** by _building_ walls, then knocking them down and _building_ them again.
  score: 0.74 (J 6)
- To stay **healthy**, _Mr. T_ _builds_ something heavy every morning before breakfast.
  score: 0.48 (J 5)
- A **healthy** man, _Mr. T_ says, is one who _builds_ rather than buys.
  score: 0.39 (J 4)

## 1049 側 side
primitives: person, rule
components: Mr. T, rule
status: candidates
- _Mr. T_ makes the _rules_, so everybody wants to be on his **side**.
  score: 0.74 (J 6)
- The first _rule_ at _Mr. T's_ table is that nobody sits on his left **side**.
  score: 0.54 (J 5)
- **Side** with _Mr. T_ and the _rules_ bend, **side** against him and they don't.
  score: 0.37 (J 4)

## 1050 侍 waiter
primitives: person, Buddhist temple
components: Mr. T, Buddhist temple
status: candidates
- _Mr. T_ is the **waiter** at the _Buddhist temple_, which is why nobody complains about the rice.
  score: 0.82 (J 6)
- A **waiter** at a _Buddhist temple_ serves rice and silence, and _Mr. T_ is good at the silence.
  score: 0.59 (J 5)
- _Mr. T_ took a job as **waiter** at the _Buddhist temple_ and the monks have put on weight.
  score: 0.55 (J 5)

## 1051 停 halt
primitives: person, pavilion
components: Mr. T, pavilion
status: candidates
- _Mr. T_ stands at the door of the _pavilion_ and everyone **halts** without being asked.
  score: 0.54 (J 5)
- The carriages **halt** at the _pavilion_ because _Mr. T_ is standing in the road.
  score: 0.57 (J 5)
- _Mr. T_ held up one hand at the _pavilion_ and the whole army came to a **halt**.
  score: 0.74 (J 6)

## 1052 値 price
primitives: person, straightaway
components: Mr. T, straightaway
status: candidates
- _Mr. T_ asks the **price** _straightaway_, he doesn't haggle and he doesn't browse.
  score: 0.74 (J 6)
- The **price** doubled _straightaway_ when the dealer saw _Mr. T_ walk in.
  score: 0.67 (J 6)
- When _Mr. T_ sells a car the **price** is paid _straightaway_, in cash, no questions.
  score: 0.57 (J 5)

## 1053 倣 emulate
primitives: person, set free
components: Mr. T, set free
status: candidates
- Boys **emulate** _Mr. T_, so when he _set free_ the lions at the zoo, so did they.
  score: 0.74 (J 6)
- _Mr. T_ **emulates** his hero by _setting free_ every chained dog he passes.
  score: 0.54 (J 5)
- To **emulate** someone is to copy them, and copying _Mr. T_ means _setting free_ whatever is caged.
  score: 0.39 (J 4)

## 1054 傲 arrogance
primitives: person, soil, compass, taskmaster
components: Mr. T, soil/dirt, compass, taskmaster (third story uses emulate + dirt, Heisig's alternative)
status: candidates
- _Mr. T's_ **arrogance** showed when he dropped the _taskmaster's_ _compass_ in the _dirt_ and said he knew the way.
  score: 0.43 (J 5)
- **Arrogance** is _Mr. T_ grinding the _taskmaster's_ _compass_ into the _soil_ with his heel.
  score: 0.80 (J 6)
- In his **arrogance** _Mr. T_ won't _emulate_ anyone, he'd sooner eat _dirt_.
  score: 0.33 (J 4)

## 1055 倒 overthrow
primitives: person, arrival
components: Mr. T, arrival
status: candidates
- The dictator was **overthrown** within an hour of _Mr. T's_ _arrival_.
  score: 0.67 (J 6)
- The regime survived the rebels but not the _arrival_ of _Mr. T_, it was **overthrown** by teatime.
  score: 0.74 (J 6)
- The revolution waited for _Mr. T_ to _arrive_ before it **overthrew** anybody.
  score: 0.48 (J 5)

## 1056 偵 spy
primitives: person, upright
components: Mr. T, upright
status: candidates
- _Mr. T_ makes a poor **spy**, he's too _upright_ to lie about anything.
  score: 0.74 (J 6)
- The best **spy** is an _upright_ man like _Mr. T_, nobody suspects the honest one.
  score: 0.39 (J 4)
- _Mr. T_ was sacked as a **spy** for being so _upright_ he reported himself.
  score: 0.99 (J 7)

## 1057 僧 Buddhist priest
primitives: person, increase
components: Mr. T, increase
status: candidates
- _Mr. T_ became a **Buddhist priest** and the temple's takings _increased_ immediately.
  score: 0.49 (J 5)
- _Mr. T_ became a **Buddhist priest** and the temple's rice bill _increased_ fourfold.
  score: 0.76 (J 6)
- _Mr. T_ joined the **Buddhist priests**, and the number of broken begging bowls _increased_.
  score: 0.55 (J 5)

## 1058 億 hundred million
primitives: person, idea
components: Mr. T, idea
status: candidates
- _Mr. T_ has one _idea_ and it's worth a **hundred million**.
  score: 0.48 (J 5)
- One good _idea_ is worth a **hundred million**, and _Mr. T_ has had exactly one.
  score: 0.80 (J 6)
- A **hundred million** people had the same _idea_ as _Mr. T_, but he got there first.
  score: 0.37 (J 4)

## 1059 儀 ceremony
primitives: person, righteousness
components: Mr. T, righteousness
status: candidates
- _Mr. T_ is master of **ceremonies** because nobody doubts his _righteousness_.
  score: 0.52 (J 5)
- Every **ceremony** has one _righteous_ man glaring at the latecomers, and that's _Mr. T_.
  score: 0.74 (J 6)
- _Mr. T_ sat through the whole **ceremony** with the _righteousness_ of a man who had organised it.
  score: 0.37 (J 4)

## 1060 償 reparation
primitives: person, prize
components: Mr. T, prize
status: candidates
- _Mr. T_ took the _prize_ money as **reparation** for the years they'd cheated him.
  score: 0.54 (J 5)
- **Reparation** is a _prize_ you're owed rather than won, and _Mr. T_ collects what he's owed.
  score: 0.52 (J 5)
- _Mr. T_ handed his _prize_ to the man he'd flattened in the final as **reparation**.
  score: 0.74 (J 6)

## 1062 催 sponsor
primitives: hermit, turkey
components: Mr. T, mountain, turkey
status: candidates
flag: Heisig reads the left side as hermit (仙); person.md casts Mr. T, so the stories use Mr. T plus a raised _mountain_ and the _turkey_
- _Mr. T_ **sponsors** the _turkey_ shoot up the _mountain_ every Thanksgiving.
  score: 0.49 (J 5)
- A **sponsor** pays, so _Mr. T_ paid for the _turkeys_ and the _mountain_ to roast them on.
  score: 0.37 (J 4)
- _Mr. T's_ **sponsor** dropped him after he ate the mascot, a _turkey_, on the _mountain_.
  score: 0.74 (J 6)

## 1063 仁 humanity
primitives: person, two
components: Mr. T, two
status: candidates
- _Mr. T_ shows his **humanity** by splitting his lunch in _two_ with whoever's hungry.
  score: 0.74 (J 6)
- **Humanity** takes _two_, _Mr. T_ and the man he decided not to hit.
  score: 0.57 (J 5)
- It takes _two_ to show **humanity**, one to fall and _Mr. T_ to pick him up.
  score: 0.80 (J 6)

## 1064 侮 scorn
primitives: person, every
components: Mr. T, every
status: candidates
- _Mr. T_ has **scorn** for _every_ man who skips leg day.
  score: 0.67 (J 6)
- _Every_ bully in the yard got the same look of **scorn** from _Mr. T_.
  score: 0.54 (J 5)
- _Every_ excuse gets the same **scorn** from _Mr. T_, a long look and no reply.
  score: 0.74 (J 6)

## 1065 使 use
primitives: person, officer
components: Mr. T, officer
status: candidates
- _Mr. T_ **uses** the _officer_ as a battering ram when the door's locked.
  score: 0.74 (J 6)
- The _officer_ **used** _Mr. T_ to carry the cannon up the hill.
  score: 0.48 (J 5)
- The _officer_ had no **use** for _Mr. T_ until the cannon got stuck in the mud.
  score: 0.37 (J 4)

## 1066 便 convenience
primitives: person, grow late
components: Mr. T, grow late
status: candidates
- The **convenience** store is the only place _Mr. T_ can buy socks once it's _grown late_.
  score: 0.57 (J 5)
- _Mr. T_ waits until it _grows late_ to use the **conveniences**, he wants the place to himself.
  score: 0.54 (J 5)
- **Convenience** food is what _Mr. T_ eats once it's _grown late_ and he can't be bothered to cook.
  score: 0.57 (J 5)

## 1067 倍 double
primitives: person, muzzle
components: Mr. T, muzzle
status: candidates
- _Mr. T_ **doubles** the _muzzle_ on his dog, one strap never holds it.
  score: 0.54 (J 5)
- The dog needed a **double** _muzzle_ once it had bitten _Mr. T_ and lived.
  score: 0.74 (J 6)
- A **double** _muzzle_ is _Mr. T's_ idea of a safe dog.
  score: 0.52 (J 5)

## 1068 優 tenderness
primitives: person, melancholy
components: Mr. T, melancholy
status: candidates
- _Mr. T_ sat beside the _melancholy_ boy with surprising **tenderness** until he stopped crying.
  score: 0.54 (J 5)
- **Tenderness** from _Mr. T_ is a hand on the shoulder when your _melancholy_ is showing.
  score: 0.35 (J 4)
- The _melancholy_ old dog gets more **tenderness** from _Mr. T_ than any human ever has.
  score: 0.74 (J 6)

## 1069 伐 fell
primitives: person, fiesta
components: Mr. T, fiesta
status: candidates
- _Mr. T_ **felled** the tree in the square, which is how the _fiesta_ got its bonfire.
  score: 0.57 (J 5)
- The _fiesta_ got out of hand and _Mr. T_ **felled** three men with one swing.
  score: 0.74 (J 6)
- For the _fiesta_ they needed a maypole, so _Mr. T_ **felled** the nearest pine with his hands.
  score: 0.54 (J 5)

## 1070 宿 inn
primitives: house, person, hundred
components: Mr. T, house, hundred
status: candidates
- The **inn** is a _house_ that sleeps a _hundred_ travellers, or _Mr. T_ and his luggage.
  score: 0.57 (J 5)
- An **inn** is a _house_ with a _hundred_ beds, and _Mr. T_ took the two nearest the door.
  score: 0.57 (J 5)
- The **inn** is a _house_ with a _hundred_ beds, and _Mr. T_ needs three of them pushed together.
  score: 0.80 (J 6)

## 1071 傷 wound
primitives: person, reclining, piggy bank
components: Mr. T, reclining, piggy bank
status: candidates
- _Mr. T_ got his **wound** _reclining_ on a _piggy bank_ that broke under him.
  score: 0.74 (J 6)
- _Mr. T_ lay _reclining_ with his **wound** on a _piggy bank_, the only pillow he had.
  score: 0.37 (J 4)
- A **wound** needs rest, so _Mr. T_ lay _reclining_ with his _piggy bank_ within reach.
  score: 0.39 (J 4)

## 1072 保 protect
primitives: person, mouth, tree
components: Mr. T, mouth, tree
status: candidates
- To **protect** the village, _Mr. T_ put a _tree_ across the _mouth_ of the valley.
  score: 0.74 (J 6)
- _Mr. T_ **protects** the _tree_ by standing in front of it with his _mouth_ shut.
  score: 0.37 (J 4)
- A _tree_ wedged in the cave _mouth_ is how _Mr. T_ **protects** his sleep from bears.
  score: 0.54 (J 5)

## 1074 傑 greatness
primitives: person, sunglasses, tree
components: Mr. T, sunglasses, tree
status: candidates
- _Mr. T's_ **greatness** shines so bright that the _trees_ wear _sunglasses_.
  score: 0.89 (J 7)
- **Greatness** is _Mr. T_ pulling up a _tree_ without taking his _sunglasses_ off.
  score: 0.57 (J 5)
- _Mr. T_ sat in _sunglasses_ under a _tree_ and let his **greatness** speak for itself.
  score: 0.37 (J 4)

## 1075 付 adhere
primitives: person, glue
components: Mr. T, glue
status: candidates
- Whatever _Mr. T_ _glues_ **adheres** for good, he uses far too much.
  score: 0.48 (J 5)
- _Mr. T_ **adhered** to the chair after sitting in the _glue_, and stayed polite about it.
  score: 0.74 (J 6)
- _Mr. T_ **adheres** to one rule, if it moves, _glue_ it.
  score: 0.48 (J 5)

## 1078 任 responsibility
primitives: person, porter
components: Mr. T, porter
status: candidates
- _Mr. T_ is the _porter_, so the **responsibility** for every bag is on his shoulders, literally.
  score: 0.57 (J 5)
- The _porter_ dropped the trunk, but _Mr. T_ took **responsibility** because he'd packed it.
  score: 0.54 (J 5)
- _Mr. T_ took the **responsibility** off the _porter_ along with the heaviest trunk.
  score: 0.74 (J 6)

## 1080 代 substitute
primitives: person, arrow
components: Mr. T, arrow
status: candidates
- _Mr. T_ was the **substitute** archer, he threw the _arrows_ by hand and still won.
  score: 0.74 (J 6)
- When the _arrows_ ran out, _Mr. T_ **substituted** a fence post.
  score: 0.67 (J 6)
- _Mr. T_ hates **substitutes**, when his _arrows_ ran out he stopped shooting rather than borrow some.
  score: 0.23 (J 3)

## 1083 化 change
primitives: person, spoon
components: Mr. T, spoon/sitting on the ground
status: candidates
- _Mr. T_ **changed** a _spoon_ into a bracelet by bending it round his wrist.
  score: 0.54 (J 5)
- Prison **changed** _Mr. T_, he learned to dig with a _spoon_.
  score: 0.67 (J 6)
- Prison **changed** _Mr. T_, he came out able to dig through concrete with a _spoon_.
  score: 0.74 (J 6)

## 1087 何 what
primitives: person, can
components: Mr. T, can
status: candidates
- **What** _Mr. T_ _can_ do is lift a car, **what** he _can't_ is parallel park it.
  score: 0.57 (J 5)
- **What** _Mr. T_ _can_ eat in one sitting, a normal family calls a week's shopping.
  score: 0.74 (J 6)
- Nobody asks _Mr. T_ **what** he _can_ do, they ask what he _can't_.
  score: 0.37 (J 4)

## 1089 俊 sagacious
primitives: person, license, walking legs
components: Mr. T, license, walking legs
status: candidates
- _Mr. T_ was **sagacious** enough to lose his _license_ before he lost his _walking legs_.
  score: 0.54 (J 5)
- _Mr. T_ is **sagacious**, he lost his _license_ and his _walking legs_ got him fitter than driving ever did.
  score: 0.32 (J 4)
- A **sagacious** man, _Mr. T_ got his _license_ renewed before his _walking legs_ gave out.
  score: 0.37 (J 4)

## 1090 傍 bystander
primitives: person, stand up, crown, compass
components: Mr. T, stand up, crown, compass
status: candidates
- Every **bystander** _stood up_ when the _crown_ went past, _Mr. T_ pulled out a _compass_ and followed it.
  score: 0.54 (J 5)
- _Mr. T_ _stood up_ among the **bystanders** at the coronation and the _crown_ swung towards him like a _compass_ needle.
  score: 0.43 (J 5)
- **Bystanders** just _stand_ there, so _Mr. T_ borrowed one's _compass_ and another's _crown_ and nobody objected.
  score: 0.37 (J 4)

## 1091 俺 myself
primitives: person, St. Bernard dog, eel
components: Mr. T, St. Bernard, eel
status: candidates
- "Caught that _eel_ **myself**," says _Mr. T_, "the _St. Bernard_ just barked at it."
  score: 0.35 (J 4)
- Asked who fed the _eel_ to the _St. Bernard_, _Mr. T_ says **myself**.
  score: 0.55 (J 5)
- **Myself** is how _Mr. T_ answers when asked who ate the _eel_ and who's walking the _St. Bernard_.
  score: 0.26 (J 3)

## 1092 久 long time
primitives: bound up, person
components: Mr. T, bound up
status: candidates
flag: not in person.md (the ⺅ here is the full-form 人, not the left-side radical); cast as Mr. T by the default rule
- A **long time** _bound up_ in bandages turns even _Mr. T_ into a mummy.
  score: 0.74 (J 6)
- _Mr. T_ stayed _bound up_ for a **long time**, nobody had the nerve to untie him.
  score: 0.74 (J 6)
- It takes a **long time** to get _Mr. T_ _bound up_, and about a second for him to get loose.
  score: 0.64 (J 6)

## 1094 囚 captured
primitives: pent in, person
components: Mr. T, pent in
status: candidates
flag: not in person.md (the ⺅ here is the full-form 人, not the left-side radical); cast as Mr. T by the default rule
- **Captured** at last, _Mr. T_ was _pent in_ a cell built specially wide.
  score: 0.74 (J 6)
- You haven't **captured** _Mr. T_ until he's _pent in_, and nothing has held him yet.
  score: 0.48 (J 5)
- **Captured** means _pent in_, and no cell has kept _Mr. T_ _pent in_ past breakfast.
  score: 0.39 (J 4)

## 1095 内 inside
primitives: belt, person
components: Mr. T, belt
status: candidates
flag: not in person.md (the ⺅ here is the full-form 人, not the left-side radical); cast as Mr. T by the default rule
- _Mr. T_ keeps his money **inside** his _belt_, and nobody has ever gone looking for it.
  score: 0.54 (J 5)
- **Inside** _Mr. T's_ _belt_ there's room for exactly one _Mr. T_.
  score: 0.48 (J 5)
- _Mr. T_ keeps his money **inside** his _belt_, and his _belt_ is the one thing nobody touches.
  score: 0.57 (J 5)

## 1096 丙 third class
primitives: ceiling, belt, person
components: Mr. T, ceiling, belt
status: candidates
flag: not in person.md (the ⺅ here is the full-form 人, not the left-side radical); cast as Mr. T by the default rule; the second story leans on his fear of flying because the keyword is a no-frills flight
- In **third class** the _ceiling_ is low, the _belt_ is tight and _Mr. T_ is in the middle seat.
  score: 0.64 (J 6)
- In **third class** _Mr. T's_ head is on the _ceiling_ and his _belt_ won't fasten.
  score: 0.80 (J 6)
- **Third class** means a _belt_ round _Mr. T_ and a _ceiling_ an inch above his head.
  score: 0.57 (J 5)

## 1105 以 by means of
primitives: person, plow, drop of
components: Mr. T, plow, drop
status: candidates
flag: not in person.md (the ⺅ here is the full-form 人, not the left-side radical); cast as Mr. T by the default rule
- **By means of** a _plow_ and a few _drops_ of sweat, _Mr. T_ feeds the whole farm.
  score: 0.57 (J 5)
- _Mr. T_ farms **by means of** a _plow_ he drags himself, one _drop_ of sweat per furrow.
  score: 0.57 (J 5)
- Farmers _plow_ with oxen, _Mr. T_ _plows_ **by means of** his own back and a _drop_ of sweat.
  score: 0.74 (J 6)

## 1106 似 similar
primitives: person, by means of
components: Mr. T impersonator, by means of
status: candidates
flag: person.md casts a Mr. T impersonator here, used verbatim; the gold paint and mohawk are what the impersonation is made of, not decoration
- A _Mr. T impersonator_ gets **similar** to the real thing _by means of_ a razor and a lot of gold paint.
  score: 0.64 (J 6)
- _By means of_ a wig and a scowl, the _Mr. T impersonator_ is **similar** enough for weddings.
  score: 0.74 (J 6)
- **Similar** isn't the same, which the _Mr. T impersonator_ learns _by means of_ a punch from the real one.
  score: 0.46 (J 5)

## 1107 併 join
primitives: person, puzzle
components: Mr. T, puzzle
status: candidates
- _Mr. T_ **joins** two _puzzle_ pieces that don't fit by pressing until they do.
  score: 0.54 (J 5)
- A _puzzle_ is a thousand pieces waiting to be **joined**, and _Mr. T_ does it with a hammer.
  score: 0.54 (J 5)
- Two _puzzle_ pieces **join** when _Mr. T_ presses them, whether they match or not.
  score: 0.74 (J 6)

## 1115 夜 night
primitives: top hat, person, walking legs, drop
components: Mr. T, top hat, walking legs, drop
status: candidates
- A _top hat_, a _drop_ to drink and his _walking legs_ to get home, that's _Mr. T's_ **night**.
  score: 0.54 (J 5)
- Every **night** _Mr. T_ goes out in a _top hat_ on his _walking legs_, not a _drop_ of rain stops him.
  score: 0.29 (J 4)
- A **night** out, for _Mr. T_, is a _top hat_, a _drop_ of whisky and _walking legs_ to get him home.
  score: 0.32 (J 4)

## 1199 伸 expand
primitives: person, monkey
components: Mr. T, monkey
status: candidates
- _Mr. T_ **expands** his chest and the _monkey_ sitting on it slides off.
  score: 0.74 (J 6)
- _Mr. T's_ gang **expanded** by six when the _monkeys_ signed up.
  score: 0.48 (J 5)
- A _monkey_ **expands** its territory by climbing, _Mr. T_ by standing there.
  score: 0.33 (J 4)

## 1224 作 make
primitives: person, saw
components: Mr. T, saw
status: candidates
- _Mr. T_ **makes** all his own furniture with a _saw_ and no measuring.
  score: 0.54 (J 5)
- _Mr. T_ **made** the table with a _saw_ and no nails, the joints are just frightened into place.
  score: 0.80 (J 6)
- Anything _Mr. T_ **makes** with a _saw_ comes out slightly too strong.
  score: 0.67 (J 6)

## 1231 侵 encroach
primitives: person, broom, crown, crotch
components: Mr. T, broom, crown, crotch
status: candidates
- Whenever the neighbours **encroach**, _Mr. T_ in his _crown_ gets the _broom_ and jabs them in the _crotch_.
  score: 0.54 (J 5)
- The sea **encroaches** on the sandcastle, so _Mr. T_ in a paper _crown_ sweeps it back with a _broom_, waves at his _crotch_.
  score: 0.43 (J 5)
- When the neighbours **encroach**, _Mr. T_ puts on his _crown_, takes the _broom_ and aims for the _crotch_.
  score: 0.57 (J 5)

## 1245 伊 Italy
primitives: person, mop
components: Mr. T, mop
status: candidates
- In **Italy** _Mr. T_ got a job _mopping_ the Sistine Chapel floor.
  score: 0.69 (J 6)
- **Italy** is shaped like a boot, so _Mr. T_ took a _mop_ to it.
  score: 0.57 (J 5)
- _Mr. T_ got a job in **Italy** _mopping_ the Leaning Tower, which is why it leans.
  score: 0.82 (J 6)

## 1250 儒 Confucian
primitives: person, demand
components: Mr. T, demand
status: candidates
- A **Confucian** _demands_ respect for elders, so _Mr. T_ carries his grandmother everywhere.
  score: 0.74 (J 6)
- _Mr. T_ became a **Confucian** because it _demands_ you honour your mother, and he already did.
  score: 0.34 (J 4)
- **Confucians** _demand_ ritual and order, and _Mr. T_ lines his boots up by size.
  score: 0.54 (J 5)

## 1267 備 equip
primitives: person, flowers, cliff, screwdriver
components: Mr. T, flowers, cliff, screwdriver
status: candidates
- _Mr. T_ **equipped** himself with a _screwdriver_ to climb the _cliff_ and pick the _flowers_ at the top.
  score: 0.54 (J 5)
- The _flowers_ on the _cliff_ are **equipped** with thorns, so _Mr. T_ brought a _screwdriver_ to prise them off.
  score: 0.32 (J 4)
- _Mr. T_ climbed the _cliff_ for the _flowers_ **equipped** with only a _screwdriver_, and the _cliff_ lost.
  score: 0.54 (J 5)

## 1270 借 borrow
primitives: person, once upon a time
components: Mr. T, once upon a time
status: candidates
- _Once upon a time_ _Mr. T_ **borrowed** a tenner from me and I'm still waiting.
  score: 0.76 (J 6)
- _Mr. T_ **borrowed** my lawnmower _once upon a time_ and it never came back.
  score: 0.76 (J 6)
- **Borrowing** from _Mr. T_ happened _once upon a time_, nobody has dared since.
  score: 0.37 (J 4)

## 1302 不 negative
primitives: ceiling, person, a drop of
components: Mr. T, ceiling, drop
status: candidates
flag: not in person.md (the ⺅ here is the full-form 人, not the left-side radical); cast as Mr. T by the default rule
- The pregnancy test was **negative**, _Mr. T_ stared at the _ceiling_ while a _drop_ ran down his cheek.
  score: 0.54 (J 5)
- One _drop_ of _Mr. T's_ blood and the drug test came back **negative**, he stared at the _ceiling_ throughout.
  score: 0.43 (J 5)
- _Mr. T_ gave a **negative**, then put a fist through the _ceiling_ and a _drop_ of plaster fell.
  score: 0.37 (J 4)

## 1373 促 stimulate
primitives: person, leg
components: Mr. T, leg
status: candidates
- The doctor **stimulated** _Mr. T's_ _leg_ with a hammer and lost two teeth.
  score: 0.74 (J 6)
- A slap on the _leg_ from _Mr. T_ **stimulates** any horse into a gallop.
  score: 0.54 (J 5)
- To **stimulate** the crowd, _Mr. T_ stamps one _leg_ until the floor shakes.
  score: 0.54 (J 5)

## 1481 幾 how many
primitives: cocoons, person, fiesta
components: Mr. T, cocoons, fiesta
status: candidates
flag: not in person.md (the ⺅ here is the full-form 人, not the left-side radical); cast as Mr. T by the default rule
- _Mr. T_ brought two _cocoons_ to the _fiesta_ and the kids asked **how many** moths were inside.
  score: 0.54 (J 5)
- **How many** _cocoons_ for the _fiesta_ lanterns, _Mr. T_ says two is plenty and he's counting.
  score: 0.39 (J 4)
- At the _fiesta_, the game is guessing **how many** moths are in _Mr. T's_ two _cocoons_.
  score: 0.74 (J 6)

## 1493 係 person in charge
primitives: person, yarn
components: Mr. T, yarn
status: candidates
- _Mr. T_ is the **person in charge** of the _yarn_, and the knitting circle has never been so quiet.
  score: 0.46 (J 5)
- Whoever holds the ball of _yarn_ is the **person in charge**, and _Mr. T_ holds it.
  score: 0.54 (J 5)
- The **person in charge** of the _yarn_ is _Mr. T_, and the cat has given up.
  score: 0.80 (J 6)

## 1664 債 bond
primitives: person, blame
components: Mr. T, blame
status: candidates
- _Mr. T_ bought government **bonds** and _blames_ his broker when they lose money.
  score: 0.54 (J 5)
- A **bond** is a loan with the _blame_ attached, and _Mr. T_ knows who to _blame_.
  score: 0.57 (J 5)
- When the **bonds** defaulted, _Mr. T_ went to find someone to _blame_, in person.
  score: 0.74 (J 6)

## 1667 俵 bag
primitives: person, surface
components: Mr. T, surface
status: candidates
- _Mr. T_ punches the **bag** so much that one _surface_ is worn smooth.
  score: 0.57 (J 5)
- _Mr. T_ hauls the rice **bag** on one shoulder, so only one _surface_ gets dirty.
  score: 0.37 (J 4)
- _Mr. T's_ punch **bag** has one _surface_ left, the rest is on the floor.
  score: 0.80 (J 6)

## 1696 俸 stipend
primitives: person, dedicate
components: Mr. T, dedicate
status: candidates
- _Mr. T_ gets a **stipend** from the temple for _dedicating_ himself to its training.
  score: 0.54 (J 5)
- A **stipend** is the small sum a man like _Mr. T_ gets for _dedicating_ his life to the monastery.
  score: 0.32 (J 4)
- _Mr. T_ _dedicated_ a year to the temple and his **stipend** was a bowl of rice a day.
  score: 0.74 (J 6)

## 1699 僅 trifle
primitives: person, cabbage
components: Mr. T, cabbage
status: candidates
- Eating a whole _cabbage_ raw is a **trifle** to _Mr. T_.
  score: 0.67 (J 6)
- _Mr. T_ paid a **trifle** for the _cabbage_ and ate it on the way home.
  score: 0.54 (J 5)
- A _cabbage_ is a **trifle** to _Mr. T_, he eats one the way you'd eat an apple.
  score: 0.72 (J 6)

## 1729 価 value
primitives: person, Old West
components: Mr. T, Old West
status: candidates
- In the _Old West_, _Mr. T's_ **value** was printed on wanted posters.
  score: 0.69 (J 6)
- A man's **value** in the _Old West_ was his gun, _Mr. T's_ was his fists.
  score: 0.55 (J 5)
- In the _Old West_ a man's **value** was on a poster, and _Mr. T's_ was the highest in the territory.
  score: 0.61 (J 6)

## 1761 俳 haiku
primitives: person, jail cell
components: Mr. T, jail cell
status: candidates
- _Mr. T_ wrote his first **haiku** in a _jail cell_, he had the time and not the paper.
  score: 0.54 (J 5)
- Seventeen syllables fit on a _jail cell_ wall, so _Mr. T_ took up **haiku**.
  score: 0.74 (J 6)
- A **haiku** is what _Mr. T_ scratches on the _jail cell_ wall with his thumbnail.
  score: 0.57 (J 5)

## 1767 侯 marquis
primitives: person, key, dart
components: Mr. T, key, dart
status: candidates
- _Mr. T_ beat the **marquis** at _darts_ and won the _key_ to his wine cellar.
  score: 0.54 (J 5)
- _Mr. T_ pinned the **marquis** to the wall with a _dart_ and took the _key_.
  score: 0.74 (J 6)
- _Mr. T_ became **marquis** by taking the old one's _key_ and pinning him to the door with a _dart_.
  score: 0.43 (J 5)

## 1772 偉 admirable
primitives: person, locket
components: Mr. T, locket
status: candidates
- _Mr. T_ is so **admirable** that children wear his picture in a _locket_.
  score: 0.80 (J 6)
- The only **admirable** thing _Mr. T_ owns is a _locket_ with his mother in it.
  score: 0.57 (J 5)
- _Mr. T_ found an **admirable** _locket_ in the gutter and spent a year finding its owner.
  score: 0.37 (J 4)

## 1804 倹 frugal
primitives: person, awl
components: Mr. T, awl
status: candidates
- _Mr. T_ is so **frugal** he repairs his own boots with a single _awl_.
  score: 0.80 (J 6)
- **Frugal** means one _awl_ for every job, and _Mr. T_ has had the same one for forty years.
  score: 0.57 (J 5)
- A **frugal** man like _Mr. T_ makes new belt holes with an _awl_ rather than buy a new belt.
  score: 0.43 (J 5)

## 1809 働 work
primitives: person, move
components: Mr. T, move
status: candidates
- _Mr. T's_ line of **work** is _moving_ pianos, one under each arm.
  score: 0.72 (J 6)
- **Work**, for _Mr. T_, means something heavy gets _moved_.
  score: 0.52 (J 5)
- _Mr. T_ went to **work** for a _moving_ company and they sold the lorry.
  score: 0.54 (J 5)

## 1836 仰 faceup
primitives: person, box, stamps
components: Mr. T, box, stamps
status: candidates
- _Mr. T_ lies **faceup** in the _box_ with _stamps_ all over the lid, they're posting him home.
  score: 0.74 (J 6)
- _Mr. T_ keeps every _stamp_ in his collection _box_ **faceup**, and heaven help anyone who turns one.
  score: 0.54 (J 5)
- **Faceup** is how _Mr. T_ sleeps, flat in a _box_ of _stamps_ like a letter waiting to go.
  score: 0.39 (J 4)

## 1842 僚 colleague
primitives: person, pup tent
components: Mr. T, pup tent
status: candidates
- _Mr. T's_ new **colleague** sleeps in a _pup tent_ in the car park.
  score: 0.54 (J 5)
- A **colleague** is someone you share a _pup tent_ with on the work trip, and nobody shares with _Mr. T_.
  score: 0.28 (J 4)
- _Mr. T_ and his **colleague** share one _pup tent_, so the **colleague** sleeps outside.
  score: 0.74 (J 6)

## 1858 修 discipline
primitives: person, walking stick, taskmaster, shape
components: Mr. T, walking stick, taskmaster, shape
status: candidates
- The _taskmaster_ beat _Mr. T_ into _shape_ with a _walking stick_, that's **discipline**.
  score: 0.74 (J 6)
- **Discipline** is a _taskmaster_, a _walking stick_ and _Mr. T_ slowly taking _shape_.
  score: 0.57 (J 5)
- _Mr. T_ learned **discipline** from a _taskmaster_ whose _walking stick_ left its _shape_ on his back.
  score: 0.54 (J 5)

## 1933 僕 me
primitives: person, husbands, in a row upside down
components: Mr. T, husbands, in a row upside down
status: candidates
- The _husbands_ hang _in a row upside down_, and the one shouting let **me** down is _Mr. T_.
  score: 0.55 (J 5)
- Pick **me**, says _Mr. T_, from the line of _husbands_ hung _in a row upside down_.
  score: 0.38 (J 4)
- The _husbands_ hung _in a row upside down_, and when the wife asked who did it, _Mr. T_ said **me**.
  score: 0.30 (J 4)

## 1935 供 submit
primitives: person, strung together
components: Mr. T, strung together
status: candidates
- _Mr. T_ **submitted** the three thieves to the sheriff _strung together_ like onions.
  score: 0.74 (J 6)
- _Mr. T_ **submits** the prisoners to the sheriff _strung together_ on one rope.
  score: 0.54 (J 5)
- To **submit** his catch, _Mr. T_ laid the fish _strung together_ through the gills at the chief's feet.
  score: 0.37 (J 4)

## 1962 倫 ethics
primitives: person, meeting, scrapbook
components: Mr. T, meeting, scrapbook
status: candidates
- At the **ethics** _meeting_, _Mr. T_ passed round a _scrapbook_ of every wrong he'd ever righted.
  score: 0.54 (J 5)
- The **ethics** _meeting_ went quiet when _Mr. T_ opened a _scrapbook_ of everyone present.
  score: 0.74 (J 6)
- **Ethics** is what a _meeting_ discusses, _Mr. T_ just keeps a _scrapbook_ of who lied.
  score: 0.39 (J 4)

## 1964 偏 partial
primitives: person, door, scrapbook
components: Mr. T, door, scrapbook
status: candidates
- _Mr. T_ keeps a _scrapbook_ of every _door_ he's kicked in, he's **partial** to the oak ones.
  score: 0.74 (J 6)
- _Mr. T_ is **partial** to the _scrapbook_ by the _door_, he flicks through it every time he leaves.
  score: 0.39 (J 4)
- _Mr. T_ is **partial** to one _door_ in the house, the one with his _scrapbook_ behind it.
  score: 0.39 (J 4)

## 1973 低 lower
primitives: person, calling card
components: Mr. T, calling card
status: candidates
- _Mr. T_ bows **lower** than the butler when handing over his _calling card_.
  score: 0.54 (J 5)
- _Mr. T_ slides his _calling card_ under the door, as **low** as a card can go.
  score: 0.54 (J 5)
- _Mr. T's_ _calling card_ is held **lower** than anyone's, he bows from the waist and keeps going.
  score: 0.57 (J 5)

## 2008 伺 pay respects
primitives: person, director
components: Mr. T, director
status: candidates
- _Mr. T_ **paid his respects** to the _director_ by not breaking anything in the office.
  score: 0.74 (J 6)
- The _director_ came to **pay respects** to _Mr. T_, not the other way round.
  score: 0.54 (J 5)
- When _Mr. T_ **pays his respects** to a _director_, the _director_ checks his wallet afterwards.
  score: 0.54 (J 5)

## 2068 偽 falsehood
primitives: person, do
components: Mr. T, do
status: candidates
- _Mr. T_ doesn't _do_ **falsehood**, if he says he'll hit you he hits you.
  score: 0.67 (J 6)
- A **falsehood** is something _done_ with the mouth, and _Mr. T_ _does_ things with his hands.
  score: 0.57 (J 5)
- _Mr. T_ caught the salesman in a **falsehood** and made him _do_ ten press-ups per lie.
  score: 0.74 (J 6)

## 2105 偶 accidentally
primitives: person, insect, brain, belt
components: Mr. T, insect, brain, belt
status: candidates
- _Mr. T_ **accidentally** squashed Jiminy Cricket, an _insect_ with a _brain_ and a _belt_, under one boot.
  score: 0.55 (J 5)
- _Mr. T_ swallowed an _insect_ **accidentally**, _belt_, _brain_ and all.
  score: 0.67 (J 6)
- _Mr. T_ **accidentally** sat on an _insect_ wearing a _belt_, the clever one with the _brain_, Jiminy Cricket.
  score: 0.55 (J 5)

## 2131 像 statue
primitives: person, elephant
components: Mr. T, elephant
status: candidates
- The town put up a **statue** of _Mr. T_ riding an _elephant_, and the _elephant_ looks tired.
  score: 0.74 (J 6)
- _Mr. T's_ **statue** is life-size and carved from the same block as the _elephant_ beside it.
  score: 0.39 (J 4)
- A **statue** of _Mr. T_ weighs as much as an _elephant_, so they used one to drag it into the square.
  score: 0.43 (J 5)
