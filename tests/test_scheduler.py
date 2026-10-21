from datetime import date

import pytest
from pawpal_system import Owner, Pet, Task, Scheduler

D = date(2026, 10, 20)


def make_owner(monkeypatch, tasks):
    owner = Owner(name="Danny")
    monkeypatch.setattr(Owner, "get_all_tasks", lambda self: list(tasks))
    return owner


def test_sort_by_time_orders_chronologically(monkeypatch):
    tasks = [Task("Dinner", "18:00", "Mochi", due_date=D), Task("Breakfast", "07:30", "Mochi", due_date=D),
             Task("Walk", "12:00", "Biscuit", due_date=D)]
    s = Scheduler(make_owner(monkeypatch, tasks))
    assert [t.time for t in s.sort_by_time()] == ["07:30", "12:00", "18:00"]


def test_filter_by_pet_and_status(monkeypatch):
    tasks = [Task("Breakfast", "07:30", "Mochi", due_date=D, completed=True),
             Task("Dinner", "18:00", "Mochi", due_date=D),
             Task("Walk", "12:00", "Biscuit", due_date=D)]
    s = Scheduler(make_owner(monkeypatch, tasks))
    assert [t.description for t in s.filter_tasks(pet_name="mochi")] == ["Breakfast", "Dinner"]
    assert [t.description for t in s.filter_tasks(completed=False)] == ["Dinner", "Walk"]
    assert [t.description for t in s.filter_tasks(pet_name="MOCHI", completed=False)] == ["Dinner"]
    assert len(s.filter_tasks()) == 3


def test_detect_conflicts_flags_same_time_across_pets(monkeypatch):
    tasks = [Task("Breakfast", "07:30", "Mochi", due_date=D),
             Task("Morning walk", "07:30", "Biscuit", due_date=D)]
    warnings = Scheduler(make_owner(monkeypatch, tasks)).detect_conflicts()
    assert len(warnings) == 1
    assert "07:30" in warnings[0] and "Breakfast (Mochi)" in warnings[0]
    assert "Morning walk (Biscuit)" in warnings[0]


def test_detect_conflicts_clean_returns_empty(monkeypatch):
    tasks = [Task("Breakfast", "07:30", "Mochi", due_date=D),
             Task("Walk", "07:30", "Biscuit", due_date=date(2026, 10, 21)),  # same time, other day
             Task("Dinner", "18:00", "Mochi", due_date=D),
             Task("Pill", "18:00", "Biscuit", due_date=D, completed=True)]  # completed: ignored
    assert Scheduler(make_owner(monkeypatch, tasks)).detect_conflicts() == []


def test_next_occurrence_daily_weekly_once():
    daily = Task("Walk", "07:00", "Mochi", frequency="daily", due_date=D, completed=True)
    weekly = Task("Bath", "10:00", "Mochi", frequency="weekly", due_date=D, completed=True)
    once = Task("Vet", "09:00", "Mochi", frequency="once", due_date=D)
    assert daily.next_occurrence().due_date == date(2026, 10, 21)
    assert weekly.next_occurrence().due_date == date(2026, 10, 27)
    assert daily.next_occurrence().completed is False
    assert weekly.next_occurrence().completed is False
    assert daily.next_occurrence().description == "Walk"
    assert once.next_occurrence() is None


def test_sort_by_priority_high_first_then_time(monkeypatch):
    tasks = [Task("Play", "08:00", "Mochi", priority="low", due_date=D),
             Task("Meds", "20:00", "Mochi", priority="high", due_date=D),
             Task("Walk", "09:00", "Biscuit", priority="medium", due_date=D),
             Task("Breakfast", "07:30", "Mochi", priority="high", due_date=D)]
    s = Scheduler(make_owner(monkeypatch, tasks))
    assert [t.description for t in s.sort_by_priority()] == ["Breakfast", "Meds", "Walk", "Play"]


def test_explain_schedule_names_priority_and_conflict(monkeypatch):
    tasks = [Task("Breakfast", "07:30", "Mochi", priority="high", due_date=D),
             Task("Morning walk", "07:30", "Biscuit", due_date=D),
             Task("Dinner", "18:00", "Mochi", due_date=D)]
    s = Scheduler(make_owner(monkeypatch, tasks))
    lines = s.explain_schedule(s.sort_by_time()).splitlines()
    assert len(lines) == 3
    assert "high" in lines[0] and "Morning walk" in lines[0]
    assert "earliest slot" in lines[0]
    assert "after" in lines[2] and "conflict" not in lines[2]


def test_todays_schedule_only_incomplete_due_that_day(monkeypatch):
    tasks = [Task("Dinner", "18:00", "Mochi", due_date=D),
             Task("Breakfast", "07:30", "Mochi", due_date=D),
             Task("Done", "08:00", "Mochi", due_date=D, completed=True),
             Task("Tomorrow", "07:00", "Mochi", due_date=date(2026, 10, 21))]
    s = Scheduler(make_owner(monkeypatch, tasks))
    assert [t.description for t in s.todays_schedule(on=D)] == ["Breakfast", "Dinner"]


def test_format_schedule_has_header_row_per_task_and_emoji(monkeypatch):
    tasks = [Task("Morning walk", "07:30", "Biscuit", due_date=D),
             Task("Mystery chore", "09:00", "Mochi", due_date=D, completed=True)]
    out = Scheduler(make_owner(monkeypatch, tasks)).format_schedule(tasks)
    lines = out.splitlines()
    assert len(lines) == 3
    assert "🐕" in lines[1] and "⬜" in lines[1]
    assert "📌" in lines[2] and "✅" in lines[2]
