"""PawPal+ CLI demo: build an owner with two pets and print today's tasks."""

from datetime import date

from pawpal_system import Owner, Pet, Task


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


def print_schedule(owner: Owner) -> None:
    # S4 replaces this with Scheduler.format_schedule
    print(f"Today's Schedule for {owner.name} ({date.today():%A, %B %d, %Y})")
    for pet in owner.pets:
        print(f"\n{pet.name} the {pet.species}")
        for t in pet.list_tasks():
            print(f"{t.time}  {t.description:<22} {t.pet_name:<8} {t.priority:<6} {t.frequency}")


if __name__ == "__main__":
    print_schedule(build_demo_owner())
