"""PawPal+ logic layer: Task, Pet, Owner and Scheduler (Phase 1 skeleton, no logic yet)."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta

PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


@dataclass
class Task:
    """One care activity for one pet."""

    description: str
    time: str  # "HH:MM", 24-hour
    pet_name: str
    duration_minutes: int = 15
    priority: str = "medium"  # "low" | "medium" | "high"
    frequency: str = "once"  # "once" | "daily" | "weekly"
    due_date: date = field(default_factory=date.today)
    completed: bool = False

    def mark_complete(self) -> None:  # S2
        """Mark this task as done."""
        raise NotImplementedError

    def next_occurrence(self) -> Task | None:  # S4
        """Return the next copy of a daily or weekly task. Returns None for a 'once' task."""
        raise NotImplementedError


@dataclass
class Pet:
    """A pet and the tasks that belong to it."""

    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:  # S2
        """Add a task to this pet and stamp the pet's name on it."""
        raise NotImplementedError

    def list_tasks(self) -> list[Task]:  # S2
        """Return this pet's tasks."""
        raise NotImplementedError

    def remove_task(self, task: Task) -> bool:  # S2
        """Remove a task from this pet; return whether it was there."""
        raise NotImplementedError


@dataclass
class Owner:
    """A person who owns one or more pets."""

    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:  # S2
        """Add a pet to this owner."""
        raise NotImplementedError

    def get_pet(self, name: str) -> Pet | None:  # S2
        """Find a pet by name, ignoring case. Returns None if there is no match."""
        raise NotImplementedError

    def get_all_tasks(self) -> list[Task]:  # S2
        """Return every pet's tasks as one list."""
        raise NotImplementedError


class Scheduler:
    """Reads every task through owner.get_all_tasks(); never from a single pet."""

    def __init__(self, owner: Owner) -> None:  # S4
        """Store the owner whose pets' tasks this scheduler organizes."""
        raise NotImplementedError

    def sort_by_time(self, tasks: list[Task] | None = None) -> list[Task]:  # S4
        """Return tasks in chronological order by their HH:MM time."""
        raise NotImplementedError

    def filter_tasks(
        self, pet_name: str | None = None, completed: bool | None = None
    ) -> list[Task]:  # S4
        """Return tasks matching an optional pet name and an optional completed status."""
        raise NotImplementedError

    def detect_conflicts(self) -> list[str]:  # S4
        """Return warnings for incomplete tasks sharing the same date and time; never raises."""
        raise NotImplementedError

    def mark_task_complete(self, task: Task) -> Task | None:  # S4
        """Complete a task and add its next occurrence to the pet. Returns None for a 'once' task."""
        raise NotImplementedError

    def todays_schedule(self, on: date | None = None) -> list[Task]:  # S4
        """Return the incomplete tasks due on a day (default today), sorted by time."""
        raise NotImplementedError

    def format_schedule(self, tasks: list[Task]) -> str:  # S4
        """Return the tasks as aligned text with an emoji per task type."""
        raise NotImplementedError

    def explain_schedule(self, tasks: list[Task]) -> str:  # S4
        """Return one line per task explaining why it is placed where it is."""
        raise NotImplementedError
