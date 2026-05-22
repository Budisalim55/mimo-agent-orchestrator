from pathlib import Path

from mimo_agent.runner import WorkflowRunner


def test_dry_run_creates_trace_and_report(tmp_path: Path) -> None:
    workflow_file = tmp_path / "workflow.yaml"
    workflow_file.write_text(
        """
name: smoke
objective: Validate the runner.
steps:
  - id: plan
    role: planner
    instruction: Create a plan.
  - id: review
    role: reviewer
    instruction: Review the plan.
""".strip(),
        encoding="utf-8",
    )

    runner = WorkflowRunner(output_dir=tmp_path / "runs")
    workflow = runner.load(workflow_file)
    run_dir = runner.run(workflow, dry_run=True)

    assert (run_dir / "trace.jsonl").exists()
    assert (run_dir / "report.md").exists()
    assert "Workflow Report: smoke" in (run_dir / "report.md").read_text(encoding="utf-8")
