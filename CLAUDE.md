# PawPal+ (CodePath AI110 Project 2) — rules for every session

## For credit
This course is for credit. You explain, scaffold, propose, review and test. Danny decides, runs
every git command, and writes `reflection.md` in his own words. Deadline: Wed Oct 21, 2:59 AM ET
(Tue Oct 20, 11:59 PM PT). Missing it moves him to observer status. Required work ships tonight.
Stretch cut line: 12:30 AM ET. Resubmission is unlimited; only the highest score shows.

## Environment (Python 3.13 via uv)
```
uv python pin 3.13
uv venv
uv pip install -r requirements.txt
.venv/bin/python --version      # must print Python 3.13.x; if 3.12 or 3.14, STOP and tell Danny
```
Never `python3 -m venv`, never plain `pip`: on this Mac they build a 3.12 venv or install into
the wrong interpreter. `.python-version` is committed; `.venv/` and `__pycache__/` are ignored.
`__pycache__/pawpal_system.cpython-314.pyc` is tracked by CodePath's starter commit: leave it
alone and never add new bytecode.

## Run commands
```
.venv/bin/python main.py
.venv/bin/python -m pytest -v
.venv/bin/python -m streamlit run app.py --server.port 8523
```
Worker ports: 8521 (UI session), 8523 (polish session).

## File map
- `pawpal_system.py` — logic layer: Task, Pet, Owner (dataclasses), Scheduler
- `main.py` — CLI demo
- `app.py` — Streamlit UI
- `tests/` — pytest suites
- `diagrams/` — `uml_draft.mmd` (Phase 1), `uml_final.mmd` and `uml.mmd` (Phase 6)
- `PAWPAL_PLAN.md` — wave/session table, merge commands, status blocks
- `ai_interactions.md` — SF7/SF11 templates (Danny fills) and the `## Notes` #note log

## Worktree workflow
One fresh session per phase, each in its own worktree on its own branch
(`git worktree add ../pawpal-<name> -b <branch>`). Never share a working tree between sessions.
Sessions cannot see each other; Danny relays messages by hand. Worktrees are removed at the end.

## Git rule
Never commit, merge or push. Present the exact commands; Danny runs them. Commit messages are
memory entries for a future agent: what changed, why, what was decided. No Co-Authored-By trailers.

## STOP rule
At every named checkpoint, show the diff and wait for Danny's explicit go-ahead before going on.
One next step at a time for Danny.

## Scope
- Workers never edit `reflection.md` or `ai_interactions.md`.
- No signature changes to the skeleton. If one must change, STOP and report; the coordinator decides.
- Note side issues, don't fix them.
- Stay inside your session's region (see the table in `PAWPAL_PLAN.md`).
