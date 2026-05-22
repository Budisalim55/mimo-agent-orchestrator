# Workflow Report: repo-review-demo

## Objective
Review a small repository and produce a prioritized improvement plan.

## Step: planner
Role: planning agent
Provider: dry-run

- inspect dependency boundaries
- verify test coverage
- identify operational risks

## Step: reviewer
Role: code review agent
Provider: dry-run

- add smoke tests for CLI entrypoint
- validate config errors with readable messages

## Final Action Plan
1. Add typed config validation
2. Add CLI smoke test
3. Add provider timeout + retry policy
