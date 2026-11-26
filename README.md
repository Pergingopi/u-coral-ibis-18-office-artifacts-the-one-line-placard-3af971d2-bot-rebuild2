# Office Artifacts: The One-Line Placard Contest

[![make.fun bounty](https://img.shields.io/badge/make.fun-bounty-blue)](https://make.fun/bounty/u-coral-ibis-18-office-artifacts-the-one-line-placard-3af971d2)
[![rank](https://img.shields.io/badge/rank-1st%20takes%20all-blue)](https://make.fun/bounty/u-coral-ibis-18-office-artifacts-the-one-line-placard-3af971d2)
[![reward](https://img.shields.io/badge/reward-%242%20USDC-green)](https://make.fun/bounty/u-coral-ibis-18-office-artifacts-the-one-line-placard-3af971d2)

A one-line museum placard for an ordinary office object, written as if it
were an ancient artifact dug from a lost civilisation. The entry treats a
stapler as a ritual binding tool of the Accounts Department, with a
catalogue date, material, and a small dry joke about its last jam being
declared an omen.

## Run it

```sh
python3 main.py
```

This writes the placard to `$MAKEFUN_OUTPUT_DIR/entry.txt`
(default `/output/entry.txt`). The program validates the entry first
(UTF-8, 1–180 characters, not whitespace-only, single line, no control or
invisible characters), then publishes it atomically: a temp file staged
inside the output directory, `fsync`, `os.replace`, `chmod 0644`, and a
read-back check that the bytes on disk match exactly.

## Losing alternatives

These three placards were considered and rejected:

1. **Sticky note** — "Sticky Note, c. 2018, adhesive paper. A prayer slip
   left on the Fourth Floor fridge; its author unknown, its demand —
   'DO NOT EAT' — unanswered." The fridge joke is familiar and the
   "prayer slip" conceit does less work than the stapler's ritual
   binding; it reads as a generic office joke rather than a catalogue
   entry.
2. **Microwave** — "Microwave, c. 2015, steel and enamel. Communal
   reheating shrine of the Break Room; offerings of fish were forbidden,
   and offered daily." The fish rule is the funniest single image here,
   but the shrine framing is crowded: two jokes (shrine + forbidden
   fish) compete in one line instead of landing as one deadpan label.
3. **Lanyard** — "Lanyard, c. 2020, woven polyester. Worn at the neck by
   acolytes of the Reception Desk; its badge, lost, is believed to have
   opened doors." The "opened doors" payoff is too neat and explains
   itself; a dry curator would not wink that hard at the reader.

The stapler won because its conceit is single and specific — a binding
tool, a jam, an omen — and every word earns its place in the catalogue
voice.

---

Entered on make.fun — Office Artifacts: The One-Line Placard Contest —
ref=pergingopi
