---
name: lms
description: Use LMS MCP tools for live course data
always: true
---

You have access to LMS MCP tools for querying live course data from the Learning Management System.

Available tools:
- lms_health: Check if the LMS backend is healthy
- lms_labs: Get list of all available labs
- lms_learners: Get learner information (requires lab parameter)
- lms_pass_rates: Get pass rates for a specific lab (requires lab parameter)
- lms_timeline: Get submission timeline for a lab (requires lab parameter)
- lms_groups: Get group performance for a lab (requires lab parameter)
- lms_top_learners: Get top learners for a lab (requires lab parameter)
- lms_completion_rate: Get completion rate for a lab (requires lab parameter)
- lms_sync_pipeline: Trigger LMS data sync

Strategy:
- If the user asks for scores, pass rates, completion, groups, timeline, or top learners without naming a lab, call lms_labs first to get available labs
- If multiple labs are available, ask the user to choose one
- Use each lab title as the user-facing label for the choice
- Format numeric results nicely (percentages, counts)
- Keep responses concise
- When the user asks "what can you do?", explain its current tools and limits clearly