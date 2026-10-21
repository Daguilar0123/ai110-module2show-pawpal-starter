"""PawPal+ CLI demo: build an owner with two pets and show what the Scheduler can do."""

from datetime import date

from pawpal_system import Owner, Pet, Scheduler, Task


def build_demo_owner() -> Owner:
    """Create Danny, Mochi and Biscuit with tasks added deliberately out of time order."""
    today = date.today()
    owner = Owner(name="Danny")
    mochi = Pet(name="Mochi", species="dog")
    biscuit = Pet(name="Biscuit", species="cat")
    owner.add_pet(mochi)
    owner.add_pet(biscuit)

    mochi.add_task(Task("Evening walk", "18:00", "Mochi", 30, "high", "daily", today))
    mochi.add_task(Task("Morning walk", "07:30", "Mochi", 30, "high", "daily", today))
    biscuit.add_task(Task("Breakfast", "07:30", "Biscuit", 10, "high", "daily", today))
    mochi.add_task(Task("Flea medication", "12:00", "Mochi", 5, "medium", "weekly", today))
    biscuit.add_task(Task("Brush coat", "19:15", "Biscuit", 15, "low", "weekly", today))
    return owner


def show(title: str, body: str) -> None:
    """Print a section header followed by its body."""
    print(f"\n=== {title} ===")
    print(body)


def run_demo(owner: Owner) -> None:
    """Walk through every Scheduler feature in order."""
    scheduler = Scheduler(owner)
    print(f"PawPal+ schedule for {owner.name} ({date.today():%A, %B %d, %Y})")

    show("Today, sorted by time", scheduler.format_schedule(scheduler.sort_by_time()))
    show("Mochi's tasks only", scheduler.format_schedule(scheduler.filter_tasks(pet_name="Mochi")))
    show("By priority (high first)", scheduler.format_schedule(scheduler.sort_by_priority()))

    conflicts = scheduler.detect_conflicts()
    show("Conflicts", "\n".join(f"⚠️  {w}" for w in conflicts) or "None")

    show("Why this order", scheduler.explain_schedule(scheduler.sort_by_time()))

    walk = next(t for t in scheduler.sort_by_time() if t.description == "Morning walk")
    nxt = scheduler.mark_task_complete(walk)
    show("Completed 'Morning walk' (daily), next one created",
         scheduler.format_schedule([walk, nxt]) + f"\nNext occurrence due {nxt.due_date}" if nxt
         else "No next occurrence")


if __name__ == "__main__":
    run_demo(build_demo_owner())
