"""PawPal+ logic layer: Task, Pet, Owner and Scheduler (Phase 1 skeleton, no logic yet)."""

from __future__ import annotations

from dataclasses import dataclass, field, replace
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
        self.completed = True

    def next_occurrence(self) -> Task | None:  # S4
        """Return the next copy of a daily or weekly task. Returns None for a 'once' task.

        The copy is due 1 day (daily) or 7 days (weekly) after this task and is not completed.
        """
        step = {"daily": 1, "weekly": 7}.get(self.frequency)
        if step is None:
            return None
        return replace(self, due_date=self.due_date + timedelta(days=step), completed=False)


@dataclass
class Pet:
    """A pet and the tasks that belong to it."""

    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:  # S2
        """Add a task to this pet and stamp the pet's name on it."""
        task.pet_name = self.name
        self.tasks.append(task)

    def list_tasks(self) -> list[Task]:  # S2
        """Return this pet's tasks."""
        return list(self.tasks)

    def remove_task(self, task: Task) -> bool:  # S2
        """Remove a task from this pet; return whether it was there."""
        for i, existing in enumerate(self.tasks):
            if existing is task:
                del self.tasks[i]
                return True
        return False


@dataclass
class Owner:
    """A person who owns one or more pets."""

    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:  # S2
        """Add a pet to this owner."""
        if self.get_pet(pet.name) is not None:
            raise ValueError(f"{self.name} already has a pet named {pet.name!r}")
        self.pets.append(pet)

    def get_pet(self, name: str) -> Pet | None:  # S2
        """Find a pet by name, ignoring case. Returns None if there is no match."""
        for pet in self.pets:
            if pet.name.casefold() == name.casefold():
                return pet
        return None

    def get_all_tasks(self) -> list[Task]:  # S2
        """Return every pet's tasks as one list."""
        return [task for pet in self.pets for task in pet.list_tasks()]


def _time_key(task: Task) -> tuple[int, ...]:
    """Turn a task's "HH:MM" into (hour, minute) so "9:00" sorts before "10:00"."""
    return tuple(int(part) for part in task.time.split(":"))


class Scheduler:
    """Reads every task through owner.get_all_tasks(); never from a single pet."""

    def __init__(self, owner: Owner) -> None:  # S4
        """Store the owner whose pets' tasks this scheduler organizes."""
        self.owner = owner

    def sort_by_time(self, tasks: list[Task] | None = None) -> list[Task]:  # S4
        """Return tasks in chronological order by their HH:MM time (all owner tasks if none given)."""
        if tasks is None:
            tasks = self.owner.get_all_tasks()
        return sorted(tasks, key=lambda t: tuple(int(x) for x in t.time.split(":")))

    def sort_by_priority(self, tasks: list[Task] | None = None) -> list[Task]:  # S4
        """Return tasks ordered high, then medium, then low priority, ties broken by time."""
        if tasks is None:
            tasks = self.owner.get_all_tasks()
        return sorted(tasks, key=lambda t: (PRIORITY_ORDER[t.priority], _time_key(t)))

    def filter_tasks(
        self, pet_name: str | None = None, completed: bool | None = None
    ) -> list[Task]:  # S4
        """Return tasks matching an optional pet name (case-insensitive) and an optional completed status."""
        result = self.owner.get_all_tasks()
        if pet_name is not None:
            result = [t for t in result if t.pet_name.lower() == pet_name.lower()]
        if completed is not None:
            result = [t for t in result if t.completed == completed]
        return result

    def detect_conflicts(self) -> list[str]:  # S4
        """Return warnings for incomplete tasks sharing the same date and time; never raises.

        Lightweight strategy: only an exact date+time match counts, durations are ignored.
        Same-pet and different-pet clashes are both reported, one warning per clashing slot.
        """
        slots: dict[tuple[date, str], list[Task]] = {}
        for task in self.owner.get_all_tasks():
            if not task.completed:
                slots.setdefault((task.due_date, task.time), []).append(task)
        warnings = []
        for (due, time), group in slots.items():
            if len(group) >= 2:
                names = " and ".join(f"{t.description} ({t.pet_name})" for t in group)
                warnings.append(f"Conflict at {time} on {due}: {names}")
        return warnings

    def mark_task_complete(self, task: Task) -> Task | None:  # S4
        """Complete a task and add its next occurrence to its pet. Returns None for a 'once' task."""
        if task.completed:
            return None
        task.mark_complete()
        nxt = task.next_occurrence()
        if nxt:
            self.owner.get_pet(task.pet_name).add_task(nxt)
        return nxt

    def todays_schedule(self, on: date | None = None) -> list[Task]:  # S4
        """Return the incomplete tasks due on a day (default today), sorted by time."""
        on = on or date.today()
        due = [t for t in self.owner.get_all_tasks() if t.due_date == on and not t.completed]
        return self.sort_by_time(due)

    def format_schedule(self, tasks: list[Task]) -> str:  # S4
        """Return the tasks as aligned text: a header, then one emoji-tagged row per task."""
        emoji_by_keyword = [
            (("walk",), "🐕"),
            (("feed", "breakfast", "dinner"), "🍽️"),
            (("med", "pill"), "💊"),
            (("vet", "appointment"), "🏥"),
            (("groom", "bath"), "🛁"),
            (("play", "enrichment"), "🎾"),
        ]

        def emoji_for(description: str) -> str:
            lowered = description.lower()
            for keywords, emoji in emoji_by_keyword:
                if any(word in lowered for word in keywords):
                    return emoji
            return "📌"

        lines = [f"   {'Time':<6}{'Task':<22}{'Pet':<8}{'Pri':<7}{'Repeats':<8}Done"]
        for t in tasks:
            done = "✅" if t.completed else "⬜"
            lines.append(
                f"{emoji_for(t.description)} {t.time:<6}{t.description:<22}{t.pet_name:<8}"
                f"{t.priority:<7}{t.frequency:<8}{done}"
            )
        return "\n".join(lines)

    def explain_schedule(self, tasks: list[Task]) -> str:  # S4
        """Return one line per task, in the given order, saying why it sits where it does.

        Reasons: the priority word, its position ("earliest slot" or "after <previous task>"),
        and any conflict from detect_conflicts() that names the task.
        """
        warnings = self.detect_conflicts()
        lines = []
        for i, t in enumerate(tasks):
            reasons = [f"{t.priority} priority", "earliest slot" if i == 0 else f"after {tasks[i - 1].description}"]
            if any(f"{t.description} ({t.pet_name})" in w for w in warnings):
                others = [
                    f"{o.description} ({o.pet_name})"
                    for o in tasks
                    if o is not t and not o.completed
                    and (o.due_date, o.time) == (t.due_date, t.time)
                ]
                if others:
                    reasons.append("conflicts with " + ", ".join(others))
            lines.append(f"{t.time} {t.description} ({t.pet_name}): " + "; ".join(reasons))
        return "\n".join(lines)
