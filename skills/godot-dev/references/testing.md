# Tests

Contents: how the runner judges · writing a test · scene tests · traps · flaky tests.

## How the runner judges

`res://tests/run_tests.gd` is a `SceneTree` script. On its first frame it loads every `res://tests/**/test_*.gd` (except the base `test_case.gd`), runs each `test_*` method on a fresh instance, and prints `N passed, M failed`, then `ALL TESTS PASSED` only when nothing failed and something passed.

- A method fails on a failed assert **or** on any engine or script error logged while it ran. Register a `Logger` (`OS.add_logger`) that collects errors and script errors and ignores warnings. `_log_error` is called from other threads, so guard it with a `Mutex`.
- A file that doesn't parse prints `FAIL <path>: script did not load` and counts as one failure.
- Set the root to aspect `keep` so screens see your layout canvas (for example 1920×1080). The headless window is tiny and aspect `expand` would otherwise stretch the canvas. Test other window shapes in their own `SubViewport`.
- Exit 1 on failure, 0 on success. On macOS headless the process can still exit 0 when the runner itself breaks, so the gate is the last line, never `$?`.

## Writing a test

```gdscript
## Guards <what>: <why it matters to the player or to another lane>.
extends "res://tests/test_case.gd"

const RULES := preload("res://data/battle_rules.tres")


## A drag cut by Cmd-Tab puts the card back instead of playing it on return.
func test_a_drag_cut_by_focus_loss_goes_back() -> void:
	var view := _view(seed)  # build state from scratch in each test
	…
	assert_eq(view.run.hand.size(), 6, "the card is back in hand")
```

- `assert_eq(actual, expected, msg)` compares type and value; `assert_true(cond, msg)`. The message says what the player would see go wrong.
- Build the starting state inside each test. Shared mutable state between methods makes order matter.
- Seeded scenario tests name their seed and why it was chosen ("seed 8 round 1: an enemy falls last"). When a data change moves that scenario, pick a new seed that shows the same thing and say so in the report.
- Settings the editor may silently rewrite get a pinning test (for example the Windows rendering driver). Add one whenever you rely on a setting.
- Pinned answers live in a JSON fixture read by a small helper. A test loops over the cases, compares each field with a call like `fx.check(self, case, field, got, want, what)` naming the case in `what`, and ends with `fx.save()` so `PIN_FIXTURE=1` can re-pin.

## Scene tests

- Add the scene under `root` inside the test (`root.add_child(view)`); only then do `_ready` and `get_viewport` work. The runner waits one frame before starting for that reason.
- Drive input the way the OS does: build `InputEventMouseButton` / `InputEventMouseMotion` and push them into the viewport (`push_input`), or send the notification Godot sends (`NOTIFICATION_APPLICATION_FOCUS_OUT`, `NOTIFICATION_WM_WINDOW_FOCUS_OUT`). Calling the handler directly skips the code path the player hits.
- Step time explicitly with a fixed delta (a `view.advance(FRAME)` method) instead of waiting on wall-clock timers; a timer test is slow and flaky.
- Free what you add (`free()`, or `queue_free()` and one more frame) so the next test starts clean.

## Traps

| Trap | What happens | Do |
| --- | --- | --- |
| Headless exit code (macOS) | 0 even when scripts fail to parse | Gate on `grep -qx "ALL TESTS PASSED"` |
| Hangs | A headless run can wait forever (a driver that never quits, an await that never resumes) | `perl -e 'alarm 900; exec @ARGV' godot …`; drivers quit themselves, `--quit-after N` is the backstop |
| No pixels | `--headless` renders nothing; viewport textures are empty | Frames come from a windowed run off screen or `--write-movie` |
| Player config | Tests that touch settings write the real `user://` config; a headless run with the title screen in the tree once saved a 64×64 window size | Back the file up and restore it around the test; keep window-owning scenes out of headless trees |
| Hand-written uids | A duplicate `uid` in a `.tscn` loads another scene, no warning | Write no `uid` in hand-written scenes and resources |
| Editor rewrites | Saving in the editor can strip settings equal to defaults | Pin the setting with a test |

Keep this table in your project too and add each new trap the day you find it.

## Flaky tests

A test that sometimes fails tells you nothing when it goes red, and people soon ignore every red. Treat it as a bug:

1. Run it alone ten times with the same seed. If it still flips, the cause is inside the test or the rule (the clock, frame delta, a float compare, a global RNG).
2. If it only flips in the full suite, an earlier test left state behind (a node not freed, a static, the player config). Find it by running the file before it, then halving.
3. Fix the cause. Don't add a retry, a sleep, or a looser assert.
