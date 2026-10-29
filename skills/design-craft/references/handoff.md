# Handing an adopted rule to dev

A handoff carries two things: the spec that states the rule in words, and the `.tres` numbers. Dev builds the rule in the game's own structure and checks it (pinned fight answers, round win rates before and after). The handoff gives dev what that check needs and nothing else.

## Before you send

- [ ] **Adopted.** The human has picked this rule. Unadopted options stay out.
- [ ] **Spec in words.** The design doc states the rule as it is now, one or two sentences per point, with no candidate mark left. Numbers stay in the data; the doc names the `.tres` file and fields.
- [ ] **Numbers in data.** The adopted numbers are in the `.tres`. Where the rule needs a field that doesn't exist yet, the note lists the field, its type, its default (today's game) and the adopted value.
- [ ] **Data and doc agree.** Read both right before sending; the data must not do something the doc doesn't say.
- [ ] **Order of simultaneous events.** If the rule adds something that can happen in the same tick as something else, write the order in the doc (dev copies it into the rule file's header).
- [ ] **Screen words.** New labels and error lines are written in the doc.
- [ ] **Measure line.** Probe command, seeds, N and policies, with today's output saved in the report, so dev can rerun it after wiring and table both.
- [ ] **Pinned fights.** Say whether the rule is meant to move fight answers. If it is, dev re-pins the fixture (`PIN_FIXTURE=1`) and explains each moved line.
- [ ] **Scope.** What the spec says that the current build plan doesn't include, listed as "not for the build". What the plan needs that the spec doesn't settle yet, listed as open.
- [ ] **Bands.** Each policy against its band, with ± SE, or what was read in its place and why.

## The note

Keep it short; the report holds the detail.

```
→ dev: <rule in one line> (adopted).
Spec: <design doc> "<section>".
Data: game/data/<file>.tres <fields> (set) · new fields: <name: type = default, adopted value> or none.
Measure: godot --headless --path game -s <probe> -- <N> <policies> → design/<area>/<topic>/report.md "<table>".
Fights move: <yes, re-pin / no>. Not for the build: <list or none>.
```

## After dev wires it

- Dev's review may find a place where the doc, the data and the build disagree. The doc wins; fix the doc or the data in the same task and tell dev which.
- A rule that measures right but plays wrong in the build is a design finding: write what the build showed and take it back to step 1 of `SKILL.md`.
