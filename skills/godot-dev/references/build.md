# Build, export and driving the build

Contents: a daily build script · trial runs · export presets · reading a failure · drive the build · footage.

## A daily build script

A useful shape for a script that turns the working tree into downloadable Windows and macOS builds each day:

0. Version `0.MILESTONE.BUILD` from a milestone line in your build checklist and a ledger `$DAILY_ROOT/versions.tsv` (a rerun on the same day keeps its number).
1. Test gate: the last line of the test log must be exactly `ALL TESTS PASSED`.
2. Stamp the version into `game/project.godot` (`config/version`, only that line), export the `Windows Desktop` and `macOS` presets into a temp dir, and put the dev value back even on failure (`trap cleanup EXIT`).
3. Check each export by its files and by the version string inside each `.pck`; zip (`ditto` for the app so signature and exec bits survive); write a changelog.
4. Only then move everything into `$DAILY_ROOT/DATE/` and append the ledger.

Print `DAILY BUILD FAILED at step: <step>` on any failure. Whatever runs it on a schedule should read success as exit 0 plus both zips present. Treat that contract as fixed; changing it is a task of its own.

## Trial runs

```sh
BUILD_DATE=2026-01-15 DAILY_ROOT=/tmp/t393/daily ./build/daily_build.sh
```

- Use a past or far date and a `/tmp` root. A trial into the real folder would replace that day's build and bump the real version counter.
- A trial exports the working tree, uncommitted files included. Say in the report whether the tree was clean.
- It runs the whole suite and two exports, so run it once per task after the tests are green, not after every edit.

## Export presets

`game/export_presets.cfg`:

- `exclude_filter` keeps `tests/*`, `tools/*` and dev-only files out of both presets. New dev scenes, probes and drivers go under those folders, so they never ship.
- macOS without an Apple Developer ID: universal binary, built-in ad-hoc signing, no notarization (Godot's documented setup). Players open it once via Privacy & Security → Open Anyway, or right-click → Open. Say so in the changelog.
- Keep `&`, `<` and `>` out of `config/name`: Godot 4.7.2 was seen writing it unescaped into `Info.plist`, and an `&` made an invalid plist, so the app would not start. Show the display title from your own data instead.
- arm64/universal macOS export needs `textures/vram_compression/import_etc2_astc=true`.
- `export_presets.cfg` is safe to commit; secrets (signing passwords, keys) belong in `.godot/export_credentials.cfg`, kept out of Git.
- Pin the Windows rendering driver with a test if you depend on it (Vulkan avoids a reported D3D12 issue on Steam Deck).

## Reading a failure

| Step | First look |
| --- | --- |
| `version` | The checklist lost its milestone line |
| `tests` | The test log's `FAIL` lines; rerun the runner locally on the same tree |
| `version stamp` | `project.godot` must hold exactly one dev `config/version` line; another edit or an earlier failed run left it stamped |
| `export windows` / `export macos` | The export log: missing export templates for this Godot version, a resource that fails to load, or no `.pck` written even though Godot exited 0 |
| `version check` | The stamped string is missing from a `.pck`; check that `project.godot` held the stamp during export |
| `zip` / `publish` | `unzip -t` or the final move failed; check free disk (`df -h`) and the paths in the log |

A build you broke gets fixed the same day.

## Drive the build

People play the exported build, so the proof is the exported build.

- **Run the shipped pack with the editor engine.** Release templates don't accept `--script`, so: `DRIVE_OUT=<dir> godot --main-pack <unzipped>/…/Game.pck --resolution 1920x1080 -s <driver.gd>`. Both zips carry the same pack, so a Mac run of the Windows `.pck` checks its content, not the `.exe`.
- **Drivers** are `SceneTree` scripts that click like a player: real pointer events on buttons and cards, from the title screen through a stage to its end. Contract: `DRIVE_OUT` for frames, quits itself, prints one `RESULT OK|FAIL gaps=N …` line. `gaps` counts clicks that changed nothing (dead buttons).
  - A seed variable restarts the stage with that seed the way a Retry button does; a size variable sets the window.
  - A click dropped because the window lost focus between press and release is the desktop's doing. Count `focus_exited` and click again, and report the retries.
- **Add a check, not a fork.** For a task-specific check, copy the driver into the task's folder with extra `CHECK` log lines instead of editing the shared driver for one task.
- **Frames:** a windowed run off screen (`--position 20000,20000`) or `--write-movie <file>.png` with `--fixed-fps`. Open every frame you cite; one picture per claim.
- **The real app once.** For launch changes (window, menus, version label) also open the unzipped `.app` and click through by hand or with `cliclick`, since only that path runs the release template and Gatekeeper.
- **Windows:** with no Windows machine or Wine, state "exe not launched" and what was checked instead (PE32+ binary, the pack plays).

## Footage

If marketing footage is recorded from each passing build with a showcase driver, whoever owns the driver fixes it in the same task when a screen change breaks it. Have the recorder fall back to the plain stage driver when the showcase doesn't print `RESULT OK`.
