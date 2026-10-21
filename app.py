from datetime import date, time

import streamlit as st

from pawpal_system import Owner, Pet, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=False):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

# Streamlit reruns this whole script on every click, so a plain variable is reborn empty
# each time. st.session_state is the vault that survives reruns: the Owner goes in once
# and every later rerun finds the same object (with its pets and tasks) still there.
if "owner" not in st.session_state:
    st.session_state.owner = None

st.subheader("Owner")
if st.session_state.owner is None:
    with st.form("owner_form"):
        owner_name = st.text_input("Owner name", value="Jordan")
        start = st.form_submit_button("Start")
    if start:
        if owner_name.strip():
            st.session_state.owner = Owner(name=owner_name.strip())
            st.rerun()
        else:
            st.error("Owner name can't be empty.")
    st.info("Enter your name and press Start to begin.")
    st.stop()

owner: Owner = st.session_state.owner
st.write(f"Owner: **{owner.name}**")

st.divider()

st.subheader("Pets")
with st.form("pet_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        pet_name = st.text_input("Pet name", value="Mochi")
    with col2:
        species = st.selectbox("Species", ["dog", "cat", "other"])
    add_pet = st.form_submit_button("Add pet")

if add_pet:
    if not pet_name.strip():
        st.error("Pet name can't be empty.")
    else:
        try:
            owner.add_pet(Pet(name=pet_name.strip(), species=species))
            st.success(f"Added {pet_name.strip()} the {species}.")
        except ValueError as err:
            st.error(str(err))

if owner.pets:
    st.write("Your pets: " + ", ".join(f"{p.name} ({p.species})" for p in owner.pets))
else:
    st.info("No pets yet. Add one above.")

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

if owner.pets:
    with st.form("task_form"):
        task_pet = st.selectbox("Pet", [p.name for p in owner.pets])
        description = st.text_input("Task description", value="Morning walk")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            task_time = st.time_input("Time", value=time(8, 0))
        with col2:
            duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
        with col3:
            priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
        with col4:
            frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])
        add_task = st.form_submit_button("Add task")

    if add_task:
        pet = owner.get_pet(task_pet)
        if pet is None:
            st.error(f"No pet named {task_pet}.")
        elif not description.strip():
            st.error("Task description can't be empty.")
        else:
            pet.add_task(
                Task(
                    description=description.strip(),
                    time=task_time.strftime("%H:%M"),
                    pet_name=pet.name,
                    duration_minutes=int(duration),
                    priority=priority,
                    frequency=frequency,
                    due_date=date.today(),
                )
            )
            st.success(f"Added '{description.strip()}' for {pet.name}.")
else:
    st.info("Add a pet before adding tasks.")

all_tasks = owner.get_all_tasks()
if all_tasks:
    st.write("Current tasks:")
    st.table(
        [
            {
                "Pet": t.pet_name,
                "Time": t.time,
                "Description": t.description,
                "Duration (min)": t.duration_minutes,
                "Priority": t.priority,
                "Frequency": t.frequency,
                "Done": "✅" if t.completed else "—",
            }
            for t in all_tasks
        ]
    )
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    st.warning("Scheduler arrives in Phase 6")
