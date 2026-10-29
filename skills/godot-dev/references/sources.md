# Sources

**Strength** as used in `SKILL.md`: **rule** = two independent sources, an official doc, or a repeated field measurement; **proposal** = one source. Pages read 2026-10.

## Godot official docs (4.x)

| Source | URL | Claim it supports |
| --- | --- | --- |
| Command line tutorial | https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html | `-s/--script` and `--main-pack` are "extended" options (editor builds, or templates built with `disable_path_overrides=false`); `--headless` = headless display and dummy audio; `--write-movie` forces `--fixed-fps`, `--quit-after` sets frames; `--export-release` needs the editor binary and installed templates; unknown arguments give no warning |
| Exporting projects | https://docs.godotengine.org/en/stable/tutorials/export/exporting_projects.html | `export_presets.cfg` is safe to commit; secrets go in `.godot/export_credentials.cfg`, kept out of version control; command-line export from a preset |
| Exporting for macOS | https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_macos.html | Without a Developer ID: built-in ad-hoc signing, notarization off; unsigned or un-notarized apps are blocked by Gatekeeper |
| Running Godot apps on macOS | https://docs.godotengine.org/en/stable/tutorials/export/running_on_macos.html | Ad-hoc signed app: Open Anyway in Privacy & Security, or right-click → Open |
| Creating movies | https://docs.godotengine.org/en/stable/tutorials/animation/creating_movies.html | Movie Maker is non-real-time with perfect frame pacing, "not designed for capturing real-time footage"; end with `quit()` or `--quit-after`, not Ctrl-C (broken AVI/WAV) |
| RandomNumberGenerator | https://docs.godotengine.org/en/stable/classes/class_randomnumbergenerator.html | "The underlying algorithm is an implementation detail and should not be depended upon." |
| Logger | https://docs.godotengine.org/en/stable/classes/class_logger.html | `_log_error` receives errors, script and shader errors and is called from other threads, so the implementation needs a `Mutex` |
| General optimization tips | https://docs.godotengine.org/en/stable/tutorials/performance/general_optimization.html | Measure first; hypothesis testing and binary search; profile → optimize → profile again; frame time is the slower of CPU and GPU |

## Determinism

| Source | Author | URL / ISBN | Claim it supports |
| --- | --- | --- | --- |
| Floating Point Determinism (2010) | Glenn Fiedler | https://gafferongames.com/post/floating_point_determinism/ | Float results are not reproducible across compilers, architectures or debug/release builds without heavy work; input replays work on the same machine and build |
| Game Programming Patterns, "Game Loop" (2014) | Robert Nystrom | https://gameprogrammingpatterns.com/game-loop.html ; ISBN 978-0-9905829-0-8 | A variable time step makes the game non-deterministic; update on a fixed step, render on its own |
| Friday Facts #60 "Tests all around" (2014) | Wube Software | https://www.factorio.com/blog/post/fff-60 | Fast unit tests plus integration tests; after each integration test a CRC is compared with saved values to catch determinism regressions |
| Friday Facts #188 (2017) | Wube Software | https://www.factorio.com/blog/post/fff-188 | Lockstep needs bit-identical simulation; desyncs are found by comparing per-tick state |
| Correlated Randomness in Slay the Spire | forgottenarbiter | https://forgottenarbiter.github.io/Correlated-Randomness/ | Streams seeded with the same number roll in lockstep; hash the run seed with the stream name |

## Tests

| Source | Author | URL / ISBN | Claim it supports |
| --- | --- | --- | --- |
| Eradicating Non-Determinism in Tests (2011) | Martin Fowler | https://martinfowler.com/articles/nonDeterminism.html | Flaky tests make the whole suite ignored; keep tests isolated; wrap the clock; no bare sleeps; fix quarantined tests fast |
| Test Pyramid (2012) | Martin Fowler, after Mike Cohn | https://martinfowler.com/bliki/TestPyramid.html | Many fast low-level tests, few broad UI tests; reproduce a bug a broad test found with a unit test first |
| Characterization test (golden master) | Wikipedia, after Michael Feathers, *Working Effectively with Legacy Code* | https://en.wikipedia.org/wiki/Characterization_test ; ISBN 0-13-117705-2 | Record what the reference does for given inputs and assert the new code matches; it detects change, not correctness, and needs repeatable output |

## Field findings (Godot 4.7, macOS, measured in a production project)

- macOS headless Godot exits 0 when scripts fail to parse; judge by the last line.
- Release templates take no `--script`; the editor engine runs the shipped `.pck`.
- `--headless` draws no pixels; frames need a window off screen or `--write-movie`.
- Metal reports GPU time 0; use Vulkan for GPU numbers.
- A click is dropped when the window loses focus between press and release.
- A duplicate `uid` in a hand-written `.tscn` loads the wrong scene silently.
- A headless run with the title screen in the tree saved a 64×64 window size to the user config.
- `&` in `config/name` broke the macOS `Info.plist`.
- A first-draw shader compile caused a single 479 ms hitch in an otherwise steady run.

## Strength per claim in SKILL.md

- Gate tests on the last line, not the exit code = **rule** (field measurement).
- Rules in plain objects, the view reads events = **rule** (Nystrom + field practice).
- No global RNG, clock or float decisions in rules = **rule** (Godot RNG doc + Fiedler + Fowler on clocks).
- Pinned answers as a characterization test, re-pinned when a change is meant to move them = **rule** (Feathers + Factorio saved CRCs).
- Log hash unchanged before and after a view change = **rule** (Factorio + field practice).
- Test pyramid, one broad drive = **rule** (Fowler/Cohn + Factorio).
- Fix flaky tests, never rerun until green = **rule** (Fowler).
- Drive the shipped `.pck` with the editor engine = **rule** (Godot command line doc + field measurement).
- Judge exports by their files = **proposal** (a guard; no failing export that exited 0 seen yet).
- Profile → change one thing → profile again; CPU vs GPU = **rule** (Godot docs + field practice).
- Vulkan for GPU timing on macOS = **rule** (field measurement).

## Not yet read

Sea of Thieves' automated-testing talk (Rare, GDC 2019) and Retro City Rampage's replay-testing talk (GDC 2015) on GDC Vault are worth adding if they change a step.
