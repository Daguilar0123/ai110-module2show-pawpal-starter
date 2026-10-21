from datetime import date

import pytest
from pawpal_system import Owner, Pet, Scheduler, Task


def test_mark_complete_changes_status():
    task = Task(description="Morning walk", time="08:00", pet_name="Mochi", due_date=date(2026, 10, 20))
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Mochi", species="dog")
    assert len(pet.list_tasks()) == 0
    pet.add_task(Task(description="Breakfast", time="07:30", pet_name="Mochi"))
    assert len(pet.list_tasks()) == 1


# --- Phase 5: real-object suite (no monkeypatch) ---------------------------------------------

TODAY = date(2026, 10, 20)


@pytest.fixture
def owner():
    """One owner, two pets, six tasks added deliberately out of time order, none clashing."""
    danny = Owner(name="Danny")
    mochi = Pet(name="Mochi", species="dog")
    biscuit = Pet(name="Biscuit", species="cat")
    danny.add_pet(mochi)
    danny.add_pet(biscuit)
    mochi.add_task(Task("Evening walk", "18:00", "Mochi", 30, "high", "daily", TODAY))
    mochi.add_task(Task("Morning walk", "07:30", "Mochi", 30, "high", "daily", TODAY))
    mochi.add_task(Task("Flea medication", "12:00", "Mochi", 5, "medium", "weekly", TODAY))
    biscuit.add_task(Task("Brush coat", "19:15", "Biscuit", 15, "low", "weekly", TODAY))
    biscuit.add_task(Task("Breakfast", "08:15", "Biscuit", 10, "high", "daily", TODAY))
    biscuit.add_task(Task("Vet checkup", "09:00", "Biscuit", 45, "medium", "once", TODAY))
    return danny


@pytest.fixture
def scheduler(owner):
    return Scheduler(owner)


def find(owner, description):
    """Return the one task with this description."""
    return next(t for t in owner.get_all_tasks() if t.description == description)


def test_sort_by_time_returns_chronological_order(scheduler):
    times = [t.time for t in scheduler.sort_by_time()]
    assert times == ["07:30", "08:15", "09:00", "12:00", "18:00", "19:15"]
    assert {t.pet_name for t in scheduler.sort_by_time()} == {"Mochi", "Biscuit"}


def test_sort_by_time_handles_unpadded_hours(owner, scheduler):
    owner.get_pet("Mochi").add_task(Task("Early pill", "9:00", "Mochi", due_date=TODAY))
    order = [t.time for t in scheduler.sort_by_time()]
    assert order.index("9:00") < order.index("12:00")  # a plain string sort would put "9:00" last


def test_marking_daily_task_complete_creates_next_day_task(owner, scheduler):
    mochi = owner.get_pet("Mochi")
    walk = find(owner, "Morning walk")
    before = len(mochi.list_tasks())

    nxt = scheduler.mark_task_complete(walk)

    assert walk.completed is True
    assert nxt is not walk
    assert nxt.due_date == date(2026, 10, 21)
    assert nxt.completed is False
    assert (nxt.time, nxt.pet_name) == ("07:30", "Mochi")
    assert len(mochi.list_tasks()) == before + 1
    assert nxt in mochi.list_tasks()


def test_weekly_recurrence_is_seven_days(owner, scheduler):
    nxt = scheduler.mark_task_complete(find(owner, "Flea medication"))
    assert nxt.due_date == date(2026, 10, 27)
    assert nxt.completed is False


def test_once_task_has_no_next_occurrence(owner, scheduler):
    biscuit = owner.get_pet("Biscuit")
    before = len(biscuit.list_tasks())
    assert scheduler.mark_task_complete(find(owner, "Vet checkup")) is None
    assert len(biscuit.list_tasks()) == before


def test_detect_conflicts_flags_duplicate_times(owner, scheduler):
    assert scheduler.detect_conflicts() == []  # the fixture itself is clash-free
    owner.get_pet("Biscuit").add_task(Task("Early feed", "07:30", "Biscuit", due_date=TODAY))
    warnings = scheduler.detect_conflicts()
    assert len(warnings) == 1
    assert "07:30" in warnings[0]
    assert "Morning walk (Mochi)" in warnings[0] and "Early feed (Biscuit)" in warnings[0]


def test_detect_conflicts_ignores_completed_tasks(owner, scheduler):
    clash = Task("Early feed", "07:30", "Biscuit", due_date=TODAY)
    owner.get_pet("Biscuit").add_task(clash)
    assert len(scheduler.detect_conflicts()) == 1
    clash.mark_complete()
    assert scheduler.detect_conflicts() == []


def test_detect_conflicts_same_pet_same_time(owner, scheduler):
    owner.get_pet("Mochi").add_task(Task("Brush teeth", "07:30", "Mochi", due_date=TODAY))
    warnings = scheduler.detect_conflicts()
    assert len(warnings) == 1
    assert "Morning walk (Mochi)" in warnings[0] and "Brush teeth (Mochi)" in warnings[0]


def test_filter_tasks_by_pet_is_case_insensitive(scheduler):
    assert len(scheduler.filter_tasks(pet_name="MoChI")) == 3
    assert {t.pet_name for t in scheduler.filter_tasks(pet_name="biscuit")} == {"Biscuit"}
    assert scheduler.filter_tasks(pet_name="Nobody") == []


def test_filter_tasks_by_completed(owner, scheduler):
    find(owner, "Breakfast").mark_complete()
    done = scheduler.filter_tasks(completed=True)
    assert [t.description for t in done] == ["Breakfast"]
    assert len(scheduler.filter_tasks(completed=False)) == 5


def test_todays_schedule_excludes_other_dates_and_completed(owner, scheduler):
    owner.get_pet("Mochi").add_task(Task("Tomorrow walk", "06:00", "Mochi", due_date=date(2026, 10, 21)))
    find(owner, "Breakfast").mark_complete()
    names = [t.description for t in scheduler.todays_schedule(on=TODAY)]
    assert names == ["Morning walk", "Vet checkup", "Flea medication", "Evening walk", "Brush coat"]


def test_pet_with_no_tasks(owner, scheduler):
    pip = Pet(name="Pip", species="hamster")
    owner.add_pet(pip)
    assert pip.list_tasks() == []
    assert len(owner.get_all_tasks()) == 6
    assert len(scheduler.todays_schedule(on=TODAY)) == 6
    assert scheduler.filter_tasks(pet_name="Pip") == []


def test_sort_by_priority_high_before_low_then_time(scheduler):
    order = [t.description for t in scheduler.sort_by_priority()]
    assert order == ["Morning walk", "Breakfast", "Evening walk", "Vet checkup", "Flea medication", "Brush coat"]


def test_get_all_tasks_spans_multiple_pets(owner):
    expected = sum(len(pet.list_tasks()) for pet in owner.pets)
    tasks = owner.get_all_tasks()
    assert len(tasks) == expected == 6
    assert [t.pet_name for t in tasks] == ["Mochi"] * 3 + ["Biscuit"] * 3  # ordered by pet


def test_add_pet_rejects_duplicate_name_ignoring_case(owner):
    with pytest.raises(ValueError):
        owner.add_pet(Pet(name="MOCHI", species="dog"))
    assert len(owner.pets) == 2


def test_mark_task_complete_twice_does_not_duplicate(owner, scheduler):
    mochi = owner.get_pet("Mochi")
    walk = find(owner, "Morning walk")
    scheduler.mark_task_complete(walk)
    scheduler.mark_task_complete(walk)  # a double click in the UI
    assert len(mochi.list_tasks()) == 4  # 3 original + exactly one next occurrence
