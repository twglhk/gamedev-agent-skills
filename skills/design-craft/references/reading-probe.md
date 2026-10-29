# Reading the auto-play

How to turn probe output into a claim the human can trust. The policies, what the game plays and what each output field counts are defined in the probe's own header and code; read them each time, because they change with the game.

## What a policy is for

- Each policy stands in for a kind of player, not a player. Its numbers say what the rules let a player who plays that way reach.
- The spread between policies is the signal that decisions matter. If a change moves the careful policy and the careless one by the same amount, it changed difficulty, not depth.
- When a policy can't use a new card, choice or placement, its number says nothing about the design. Teach your lane probe to use it (override the scoring or targeting function it inherits), measure both, and say which you report.

## Lane probes

- One per task, in the task's folder: `design/<area>/<topic>/probe.gd`, extending the main probe, run with `godot --headless --path game -s "$PWD/design/<area>/<topic>/probe.gd" -- <N> <policies>`.
- Header: the run command, every `TRY=` key it accepts, what `OUT=` writes, and what each printed count means. A small script that turns two `OUT` files into tables and paired differences pays for itself.
- `TRY="k=v;…"` changes numbers in memory only. The `.tres` stays as it is until the human adopts.
- Check it against the original: with no `TRY`, the lane probe prints the same per-round rates as the main probe on the same seeds. Say so in the report.
- If the question needs a part of the run the game can't play yet, or a rule that needs code, the probe can't fake it. Ask dev and measure once it lands.

## Error bars

- One rate from N runs: standard error = √(p(1−p)/N). At p = 50%: N = 200 → ±3.5 points, N = 500 → ±2.2, N = 1,000 → ±1.6.
- To halve the error, run four times as many seeds.
- Two conditions on the **same seeds**: compute the difference run by run and take its standard error (standard deviation of the per-seed differences ÷ √N). This is smaller than comparing two separate rates, because both sides share each seed's luck (common random numbers).
- Report: rate (± SE) for each condition, Δ (± SE) against today. Read |Δ| < 2 SE as no difference.
- Rates counted per fight or per round are clustered by run: rounds in one run share a team. Their real error is wider than the count suggests; quote them to the nearest couple of points.
- If the seed also picks the route or map, a rate for one route comes from only part of the seeds. Give N per route.
- Use the same seed set 1..N in every report, so a later task can rerun an old table and see whether the game drifted. If it drifted, say so and rerun the baseline column.

## Choosing N

| Purpose | Runs per policy |
| --- | --- |
| Does it run, does anything move | 50–100 |
| First look, a number for the report | 1000 |
| One route only, or an effect of 2 points or less | 2000 or more, so each route gets 1000 |
| A check after dev wires a rule | whatever your build guide sets |

## Matching difficulty

Options that give the team more (rounds, cards, slots) make every policy win more, which hides what else changed.

1. Pick one knob that sits after the change in the run (enemy or boss strength are the usual ones, because they touch no earlier choice).
2. Move it in memory (`TRY=`) until smart is within one SE of today.
3. Compare the other metrics at that point and list the knob value in the table.
4. If no single knob gets there without breaking another policy's band, that is the finding; report it.

## Pick metrics before running

Write the question's metrics first (`SKILL.md` §1). Typical ones: per-round win rate per policy, stage clear, wiped runs, rounds and units lost per run, upgrades and synergy tiers at the boss, boss casts and when it falls, minutes (agent estimate). Other numbers in the output are context, not findings, unless they change the reading.

## Bands on a partial game

Bands are usually written per run. While the game plays less than a whole run, a band can't be read directly. Write what you read in its place (for example stage clear as a share of runs), why it stands in, and how far it is from the real thing.

## Finding causes

- Averages show that something moved; single runs show why. Pick three seeds where the outcome flipped between conditions and read them through.
- Counterfactual: rerun the same seed with one thing swapped at one point (one encounter, one card), so everything before is byte-identical, and compare that round.
- A distribution beats a mean when the tail matters (units lost, wiped runs): print the histogram.

## Checks before a number leaves the lane

- Same command twice gives the same numbers (determinism).
- Default output unchanged when your switch is off.
- Every number has its unit, N, seeds, policy and what ± means.
- The table states "agent auto-play, not a playtest".
- The command that reproduces each table is in the report's files list.
