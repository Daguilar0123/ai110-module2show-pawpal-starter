# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases. **SEE reflection.md**
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## How it works

PawPal+ helps a busy pet owner keep up with daily care. You tell it who you are and which pets you have, add care tasks such as walks, feedings and medication, and it builds a plan for the day.

The logic lives in `pawpal_system.py`. A `Task` holds one care activity: a description, an "HH:MM" time, the pet it belongs to, a duration, a priority, how often it repeats, a due date, and whether it is done. It can mark itself complete. A `Pet` holds a name, a species and its own list of tasks, and can add, list and remove them. An `Owner` holds a name and a list of pets, refuses two pets with the same name (ignoring case), looks a pet up by name, and can return every pet's tasks as one flat list.

The classes connect in one direction. An Owner has Pets, and a Pet has Tasks. The Scheduler takes an Owner and reads all tasks through `Owner.get_all_tasks()` rather than from any single pet, so a plan always covers every animal in the household.

The project is built CLI-first. `main.py` builds an owner, two pets and a handful of tasks, then prints today's list, so the logic can be checked in a terminal before the Streamlit UI in `app.py` calls the same classes.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
PawPal+ schedule for Danny (Wednesday, October 21, 2026)

=== Today, sorted by time ===
   Time  Task                  Pet     Pri    Repeats Done
🐕 07:30 Morning walk          Mochi   high   daily   ⬜
🍽️ 07:30 Breakfast             Biscuit high   daily   ⬜
💊 12:00 Flea medication       Mochi   medium weekly  ⬜
🐕 18:00 Evening walk          Mochi   high   daily   ⬜
📌 19:15 Brush coat            Biscuit low    weekly  ⬜

=== Mochi's tasks only ===
   Time  Task                  Pet     Pri    Repeats Done
🐕 18:00 Evening walk          Mochi   high   daily   ⬜
🐕 07:30 Morning walk          Mochi   high   daily   ⬜
💊 12:00 Flea medication       Mochi   medium weekly  ⬜

=== By priority (high first) ===
   Time  Task                  Pet     Pri    Repeats Done
🐕 07:30 Morning walk          Mochi   high   daily   ⬜
🍽️ 07:30 Breakfast             Biscuit high   daily   ⬜
🐕 18:00 Evening walk          Mochi   high   daily   ⬜
💊 12:00 Flea medication       Mochi   medium weekly  ⬜
📌 19:15 Brush coat            Biscuit low    weekly  ⬜

=== Conflicts ===
⚠️  Conflict at 07:30 on 2026-10-21: Morning walk (Mochi) and Breakfast (Biscuit)

=== Why this order ===
07:30 Morning walk (Mochi): high priority; earliest slot; conflicts with Breakfast (Biscuit)
07:30 Breakfast (Biscuit): high priority; after Morning walk; conflicts with Morning walk (Mochi)
12:00 Flea medication (Mochi): medium priority; after Breakfast
18:00 Evening walk (Mochi): high priority; after Flea medication
19:15 Brush coat (Biscuit): low priority; after Evening walk

=== Completed 'Morning walk' (daily), next one created ===
   Time  Task                  Pet     Pri    Repeats Done
🐕 07:30 Morning walk          Mochi   high   daily   ✅
🐕 07:30 Morning walk          Mochi   high   daily   ⬜
Next occurrence due 2026-10-22
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time` | Sorts any task list by an `(hour, minute)` key built from "HH:MM", so "9:00" still sorts before "10:00". |
| Filtering | `Scheduler.filter_tasks` | Narrows all of the owner's tasks by pet name (case-insensitive) and/or completed status; both filters are optional. |
| Conflict handling | `Scheduler.detect_conflicts` | Warns when two or more incomplete tasks share the same date and time, for one pet or several; durations are deliberately ignored. |
| Recurring tasks | `Task.next_occurrence`, `Scheduler.mark_task_complete` | Completing a daily or weekly task creates the next copy (+1 or +7 days, not completed) on the same pet; "once" tasks create nothing. |

**Priority scheduling (stretch)**
`Scheduler.sort_by_priority` orders tasks high, then medium, then low (using `PRIORITY_ORDER`), and breaks ties by time of day, so the most important care comes first even when it is later in the day.

**Output formatting (stretch)**
`Scheduler.format_schedule` prints a header and one aligned row per task using plain f-strings and emoji, with no extra dependency. The emoji map is by keyword in the description: walk 🐕, feed/breakfast/dinner 🍽️, med/pill 💊, vet/appointment 🏥, groom/bath 🛁, play/enrichment 🎾, anything else 📌; ✅ marks done tasks and ⬜ open ones.

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
