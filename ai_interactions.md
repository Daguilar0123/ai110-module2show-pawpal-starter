# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF7)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

<!-- Describe the goal you asked the agent to accomplish -->

**What did the agent do?**

<!-- List the steps the agent took (files edited, commands run, etc.) -->

**What did you have to verify or fix manually?**

<!-- Describe anything the agent got wrong or that required human review -->

---

## Prompt Comparison (SF11)

> Compare two different prompts (or two different models) on the same task.

| | Option A | Option B |
|-|----------|----------|
| **Model / tool used** | | |
| **Prompt** | | |
| **Response summary** | | |
| **What was useful** | | |
| **Problems noticed** | | |
| **Decision** | | |

**Which approach did you use in your final implementation and why?**

<!-- Your conclusion -->

---

## Notes

#note 2026-10-20 21:41 ET — coordinator started; env pinned to 3.13 (uv 0.12.7, `.venv/bin/python --version` printed 3.13.13, verified from Danny's pasted output).
#note 2026-10-20 21:41 ET — S0: coordinator suggested a default set of three core actions; Danny wrote his own in reflection.md 1a (Track, Consider constraints, Produce a daily plan + explain why). Compared against the pinned design; gaps found: no explanation code, no owner preferences, no time budget, no task-type field.
#note 2026-10-20 21:41 ET — S0: coordinator suggested adding only `Scheduler.explain_schedule(tasks) -> str` (S4). Danny accepted. Rejected for tonight: Task.category and Owner.preferences (cost: dataclass changes across S2/S3/S4/S8/S6 prompts and the UML). Danny: owner preferences stay out tonight; written up in reflection 2b, possible resubmission feature later this week. Verified by reading reflection.md 1a and PAWPAL_PLAN.md pinned block.
#note 2026-10-20 21:41 ET — S0: Danny reviewed the four-object breakdown (Task, Pet, Owner, Scheduler with attributes and methods) and said "no changes"; pinned design plus explain_schedule is the contract.
#note 2026-10-20 22:30 ET — S0: Danny decided the UML draft and the skeleton show required work only: removed to_dict/from_dict, save_to_json/load_from_json, sort_by_priority and next_available_slot; kept the `priority` attribute, format_schedule and explain_schedule; next_occurrence and mark_task_complete typed Optional~Task~ in the diagram. Reason: the draft shows required work only, so Phase 6's final diagram shows what the build actually added. Stretch signatures moved unchanged to PAWPAL_PLAN.md under "Added in wave 2 (stretch), not in the skeleton"; prompts 04/07/08 patched by Danny in the study repo (commit 5c61ca2). Verified: `import pawpal_system` prints ok; skeleton methods match the draft; PAWPAL_PLAN.md blocks read by Danny.
#note 2026-10-20 22:30 ET — S0: new time gates from Danny: skeleton commit by 10:05 (slipped; committing 10:30), wave 1 merged by 11:35, wave 2 merged by 12:45 (only what is green), polish 12:45–1:30, submit by 1:45 AM, hard stop 2:15 AM.
