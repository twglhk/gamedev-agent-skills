# Battle determinism

The rule: same seed and same team give a byte-identical battle log. Pinned fight logs, "this visual change alters nothing" checks, replays by seed and footage that re-shoots a moment all stand on it.

## What the log is

- The sim keeps a text log, one line per thing that happened, in tick order. A `log_hash()` over those lines joined by `\n` (djb2-xor in hex works) is a fast fingerprint, not a tamper checksum. Two equal hashes from the same code path are good enough evidence; when in doubt compare the lines themselves.
- Effects for the view are not part of the log. A view may add, drop or reorder what it shows; it may never feed anything back into the rule object except player inputs.

## What breaks it

| Source | Why | Instead |
| --- | --- | --- |
| `randi()`, `randf()`, `randomize()`, `Array.shuffle()`, `pick_random()` | Global RNG, seeded from time or shared with other code; its algorithm is an implementation detail per the Godot docs | Your own seeded stream passed in; your own shuffle on that stream |
| `RandomNumberGenerator` even when seeded | Same algorithm caveat; an engine update could move every pinned log | A small generator you own (mulberry32 is enough); changing it moves every pin, on purpose |
| `Time.*`, `OS.get_ticks_*`, frame `delta` in a rule | Wall clock differs every run and every machine | Integer ticks; the view maps ticks to seconds |
| Float maths that decides an outcome (distance compares, percentages) | Float results can differ by compiler, CPU and build type | Integers; percent as `x * pct / 100`; distances in cells |
| Iterating a structure whose order depends on how it was built (a `Dictionary` filled from a scene walk, `get_children()` after a reparent) | Order follows insertion, which follows load or scene order | Sort by a stable key (unit `id`) before acting |
| The view calling into the rule (`await`, signals that step the sim) | Game speed, hitstop or a dropped frame changes how many steps run per input | The view only reads; inputs go in with their tick |
| Threads in a rule | Scheduling order varies | Keep rules on one thread |

Turn the first rows into a file scan the test suite runs over your rule folders.

## Checks to run

- **No change intended** (view, effects, UI, refactor): pick the seeds of an existing check, record `log_hash()` per fight before your change, again after, at every game speed, with the view attached and with the bare sim. All equal: write the hash list in the report. Each new visual effect gets a test that copies this pattern.
- **Rule change intended**: run the suite; the pinned fights that fail are the ones the change moved. When the design rule explains every one, re-pin (`PIN_FIXTURE=1 godot --headless --path game -s res://tests/run_tests.gd`) and list each `PIN moved` line with the rule that moves it. A move no rule explains is a bug to find first (below).
- **Fresh process**: run the same check from a second `godot --headless` invocation and compare the printed hashes. A static or cached value can make two runs in one process agree while a fresh one differs.
- **Save and resume**: state written at a round edge and read back must continue to the same log.

## When two runs disagree

Find the first difference before forming a theory.

1. Dump both logs to files (one line per entry) and `diff` them. The first differing line names the tick and the unit.
2. If the logs match but the hashes don't, the inputs differ: compare the specs (team, cells, items, seed, enemy scale) field by field.
3. If the first difference is at tick 0, setup differs (data, spec, stream seed). If later, step into that tick; the tick order in the sim's header says which phase ran first.
4. Fix the cause and add a test that pins the case (the seed and the spec that diverged).

Factorio works the same way at a larger scale: integration tests compare a CRC with a saved value after each test, and a desync is chased by logging a CRC every tick to find the first one that differs.
