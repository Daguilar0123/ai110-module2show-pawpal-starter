from datetime import date
from pawpal_system import Owner, Pet, Task


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
