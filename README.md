# MiMo Agent Orchestrator

[![CI](https://github.com/Budisalim55/mimo-agent-orchestrator/actions/workflows/ci.yml/badge.svg)](https://github.com/Budisalim55/mimo-agent-orchestrator/actions/workflows/ci.yml)

A lightweight multi-agent workflow runner for OpenAI-compatible model APIs, designed to test Xiaomi MiMo and other LLM providers inside real developer automation loops.

This project demonstrates how I use agentic workflows for:

- repository triage
- long-context task decomposition
- code review checklists
- structured execution logs
- provider fallback between Claude / GPT / Gemini / MiMo-compatible endpoints

The core idea is simple: define a workflow as YAML, run each step with a chosen model endpoint, persist outputs as audit logs, and produce a final execution report that can be reviewed by humans.

## Why this exists

Most AI coding workflows fail because prompts are not reproducible and the final answer has no trace. This runner keeps every step explicit:

1. load workflow YAML
2. build prompt for each role
3. call an OpenAI-compatible API
4. validate response shape
5. save JSONL traces
6. generate a Markdown report

It is intentionally small so it can be adapted to Claude Code, Hermes Agent, Cursor, OpenClaw, or MiMo API Platform.

## Features

- OpenAI-compatible `/chat/completions` client
- YAML workflow definitions
- multi-step agent roles: planner, builder, reviewer
- streaming-friendly architecture
- JSONL trace output for reproducibility
- offline dry-run mode for demos and CI
- provider config via environment variables
- no vendor lock-in

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .

# dry-run demo, no API key needed
mimo-agent run examples/repo-review.yaml --dry-run

# real provider call
export OPENAI_BASE_URL="https://platform.xiaomimimo.com/v1"
export OPENAI_API_KEY="your_api_key"
export OPENAI_MODEL="mimo-v2.5"
mimo-agent run examples/repo-review.yaml
```

## Example workflow

```yaml
name: repo-review-demo
objective: Review a small repository and produce a prioritized improvement plan.
steps:
  - id: planner
    role: planning agent
    instruction: Break the objective into concrete review areas.
  - id: reviewer
    role: code review agent
    instruction: Identify risks, missing tests, and maintainability issues.
  - id: closer
    role: execution closer
    instruction: Turn findings into a 5-item action plan.
```

## Output

Each run creates:

- `runs/<timestamp>/trace.jsonl`
- `runs/<timestamp>/report.md`
- `examples/sample-report.md` as a static example of the expected output format

Example report excerpt:

```md
# Workflow Report: repo-review-demo

## Objective
Review a small repository and produce a prioritized improvement plan.

## Step planner
- inspect dependency boundaries
- verify test coverage
- identify operational risks

## Step reviewer
- add smoke tests for CLI entrypoint
- validate config errors with readable messages

## Final Action Plan
1. Add typed config validation
2. Add CLI smoke test
3. Add provider timeout + retry policy
```

## Repository structure

```text
mimo_agent/
  cli.py          # command line interface
  client.py       # OpenAI-compatible API client
  runner.py       # workflow execution engine
  schemas.py      # dataclasses and validators
examples/
  repo-review.yaml
  sample-report.md
tests/
  test_runner.py
```

## Grant relevance

This project is built for evaluating AI model APIs inside real builder workflows. Xiaomi MiMo tokens would be used to:

- benchmark MiMo responses against other coding models
- run repo-review workflows on active projects
- test long-chain planning and verification loops
- integrate MiMo into Hermes Agent / Claude Code style automation

## License

MIT
