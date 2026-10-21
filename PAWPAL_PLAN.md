# PawPal+ build plan (Tue Oct 20, 2026)

Coordinator-owned. Copied from the plan of record in Danny's study repo (`Show_Project2_PawPal_Plus/PawPal_Plus_Build_Plan.md`).
Hard deadline: Wed Oct 21, 2:59 AM ET. Target submit 11:00 PM ET. Stretch cut line 12:30 AM ET. Hard stop 2:00 AM ET.
Workers read this file for the pinned design and their row. Only the coordinator edits it.

## Sessions and waves

| Wave | # | Course phase | Branch → worktree | Owns (nobody else touches) | Prompt |
|---|---|---|---|---|---|
| 0 | S0 | Coordinator + **Phase 1** design and skeleton | `main`, repo root | `.python-version`, `.venv`, `CLAUDE.md`, `PAWPAL_PLAN.md`, `ai_interactions.md` `## Notes` log, `diagrams/uml_draft.mmd`, `pawpal_system.py` skeleton | `00_Coordinator.md` |
| 1 | S2 | **Phase 2** core | `feat/core-classes` → `../pawpal-core` | `Task` (except `next_occurrence`), `Pet`, `Owner` bodies; `main.py`; `tests/test_pawpal.py` (first two tests); README "How it works" + "Sample Output" | `02_Core.md` |
| 1 | S3 | **Phase 3** UI integration | `feat/ui-integration` → `../pawpal-ui`, port 8521 | `app.py` only | `03_UI_Integration.md` |
| 1 | S4 | **Phase 4** algorithms + stretch 3 and 4 (CLI) | `feat/scheduler-algorithms` → `../pawpal-algorithms` | `Task.next_occurrence`; every `Scheduler` method except `next_available_slot`; README "Smarter Scheduling"; `main.py` additions **only after S2 is merged** | `04_Algorithms.md` |
| merge 1 | Danny | merge S2, then S4, then S3 into `main`; run `main.py` and pytest on `main` | | | coordinator gives the commands |
| 2 | S5 | **Phase 5** tests | `test/suite` → `../pawpal-tests` | `tests/test_pawpal.py`; README "Testing PawPal+" | `05_Tests.md` |
| 2 | S7 | **Stretch 1** third algorithm, agent mode | `feat/next-available-slot` → `../pawpal-agent-algo` | `Scheduler.next_available_slot`; `tests/test_slot.py` | `07_Stretch_AgentMode_NextSlot.md` |
| 2 | S8 | **Stretch 2** persistence | `feat/persistence` → `../pawpal-persist` | `to_dict`/`from_dict` on all three dataclasses, `Owner.save_to_json`/`load_from_json`, `data.json`, `tests/test_persistence.py`, README "Persistence" | `08_Stretch_Persistence.md` |
| 2 | Danny | **Stretch 5** model comparison | none | `ai_interactions.md` SF11 | `09_Danny_Model_Comparison.md` |
| merge 2 | Danny | merge S5, then S8, then S7; full pytest on `main` | | | |
| 3 | S6 | **Phase 6** polish + stretch 4 (UI) + docs | `main`, port 8523 | `app.py` display; `diagrams/uml_final.mmd` + `uml.mmd`; README Features, Demo Walkthrough, Persistence/Formatting notes; `reflection.md` **typed by Danny** | `06_Polish_and_Docs.md` |

## Pinned design (the contract every prompt is written against)

No session may change a signature. If one must, it STOPs and tells Danny; the coordinator relays the change here.

```python
# pawpal_system.py — skeleton signatures. Bodies: raise NotImplementedError until a wave fills them.
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date, timedelta

PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}

@dataclass
class Task:
    description: str
    time: str                      # "HH:MM", 24-hour
    pet_name: str
    duration_minutes: int = 15
    priority: str = "medium"       # "low" | "medium" | "high"
    frequency: str = "once"        # "once" | "daily" | "weekly"
    due_date: date = field(default_factory=date.today)
    completed: bool = False

    def mark_complete(self) -> None: ...            # S2
    def next_occurrence(self) -> Task | None: ...   # S4: copy with due_date +1 day / +7 days, completed=False; None if "once"

@dataclass
class Pet:
    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None: ...     # S2 (also sets task.pet_name = self.name)
    def list_tasks(self) -> list[Task]: ...         # S2
    def remove_task(self, task: Task) -> bool: ...  # S2

@dataclass
class Owner:
    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None: ...                 # S2
    def get_pet(self, name: str) -> Pet | None: ...          # S2
    def get_all_tasks(self) -> list[Task]: ...               # S2 — every pet's tasks, one list (the multi-pet point)

class Scheduler:
    """Reads every task through owner.get_all_tasks(); never from a single pet."""
    def __init__(self, owner: Owner) -> None: ...                                  # S4
    def sort_by_time(self, tasks: list[Task] | None = None) -> list[Task]: ...     # S4 (key: "HH:MM" → (hour, minute))
    def filter_tasks(self, pet_name: str | None = None, completed: bool | None = None) -> list[Task]: ...  # S4
    def detect_conflicts(self) -> list[str]: ...        # S4: warnings for same date+time, incomplete, any pets; never raises
    def mark_task_complete(self, task: Task) -> Task | None: ...   # S4: task.mark_complete(); next = task.next_occurrence(); append to the pet; return next
    def todays_schedule(self, on: date | None = None) -> list[Task]: ...   # S4: incomplete tasks due that day, sorted by time
    def format_schedule(self, tasks: list[Task]) -> str: ...               # S4: emoji per task type + aligned columns
    def explain_schedule(self, tasks: list[Task]) -> str: ...              # S4: one reason line per task (priority, time, conflict)
```

## Added in wave 2 (stretch), not in the skeleton

These are added by their sessions with exactly these signatures; adding a method is not a signature change.

```python
# Task (S8)
    def to_dict(self) -> dict: ...                  # S8
    @classmethod
    def from_dict(cls, data: dict) -> Task: ...     # S8

# Pet (S8)
    def to_dict(self) -> dict: ...                  # S8
    @classmethod
    def from_dict(cls, data: dict) -> Pet: ...      # S8

# Owner (S8)
    def to_dict(self) -> dict: ...                           # S8
    @classmethod
    def from_dict(cls, data: dict) -> Owner: ...             # S8
    def save_to_json(self, path: str = "data.json") -> None: ...        # S8
    @classmethod
    def load_from_json(cls, path: str = "data.json") -> Owner: ...      # S8

# Scheduler
    def sort_by_priority(self, tasks: list[Task] | None = None) -> list[Task]: ... # S4 (PRIORITY_ORDER, then time)
    def next_available_slot(self, duration_minutes: int, on: date | None = None,
                            day_start: str = "07:00", day_end: str = "21:00") -> str | None: ...  # S7
```

Other pinned choices: conflict = exact same `due_date` and `time` among incomplete tasks, same pet or different pets
(durations are not checked; that is the tradeoff for reflection §2b). `Pet.add_task` stamps `task.pet_name`.
`main.py` prints with `Scheduler.format_schedule`. UML files: `diagrams/uml_draft.mmd` (Phase 1),
`diagrams/uml_final.mmd` (Phase 6), `diagrams/uml.mmd` overwritten with the final. Ports: 8521 (S3), 8523 (S6).

## Merge commands (Danny runs them from the repo root, after the coordinator's go-ahead)

```
git checkout main
git merge --no-ff feat/core-classes -m "Merge feat/core-classes: Task, Pet, Owner bodies, main.py demo, first tests"
git merge --no-ff feat/scheduler-algorithms -m "Merge feat/scheduler-algorithms: sorting, filtering, conflicts, recurrence, priority, formatting"
git merge --no-ff feat/ui-integration -m "Merge feat/ui-integration: app.py wired to Owner/Pet/Task via session_state"
.venv/bin/python main.py
.venv/bin/python -m pytest -v
```

Wave 2 the same way, in this order: `test/suite`, then `feat/persistence`, then `feat/next-available-slot`.
Worktrees come off at the end: `git worktree remove ../pawpal-core` etc. (six of them).

## Status

Stages per session: started / STOP 1 reached / tests green / live check done / committed / merged.

### S0 — coordinator + Phase 1
started (env pinned to 3.13.13; setup commit 3e3b11d); Phase 1 files written 10:30 PM ET (uml_draft.mmd, pawpal_system.py skeleton, required work only), skeleton commit pending
Gates (Danny, Oct 20): wave 1 merged 11:35 PM, wave 2 merged 12:45 AM (only what is green), polish 12:45–1:30, submit 1:45 AM, hard stop 2:15 AM.
Contract change, Oct 20 2026: Danny chose to add `Scheduler.explain_schedule(tasks) -> str` (S4's region) so his
third core action, "explain why it chose that plan", has code behind it. Task types stay description keywords;
time available = `next_available_slot` window; owner preferences are out of scope (reflection 2b, Danny's words).
Prompt patches Danny applies in the study repo: 04_Algorithms.md (add the method and one test) and
06_Polish_and_Docs.md (show the explanation in the UI).

### S2 — core classes (`feat/core-classes`)
not started

### S3 — UI integration (`feat/ui-integration`)
not started

### S4 — scheduler algorithms (`feat/scheduler-algorithms`)
not started

### S5 — tests (`test/suite`)
not started

### S6 — polish and docs (`main`)
not started

### S7 — next available slot (`feat/next-available-slot`)
not started

### S8 — persistence (`feat/persistence`)
not started
