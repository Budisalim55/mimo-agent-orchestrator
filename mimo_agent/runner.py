from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import yaml

from .client import ChatClient
from .schemas import StepResult, Workflow


class WorkflowRunner:
    def __init__(self, client: ChatClient | None = None, output_dir: Path | str = "runs") -> None:
        self.client = client or ChatClient.from_env()
        self.output_dir = Path(output_dir)

    def load(self, workflow_path: Path | str) -> Workflow:
        path = Path(workflow_path)
        with path.open("r", encoding="utf-8") as handle:
            payload = yaml.safe_load(handle)
        return Workflow.from_dict(payload)

    def run(self, workflow: Workflow, dry_run: bool = False) -> Path:
        run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        run_dir = self.output_dir / run_id
        run_dir.mkdir(parents=True, exist_ok=True)

        results: list[StepResult] = []
        context = ""
        for step in workflow.steps:
            prompt = self._build_prompt(workflow.objective, step.instruction, context)
            if dry_run:
                output = self._dry_output(step.id, step.role, workflow.objective)
                provider = "dry-run"
            else:
                output = self.client.complete(system=f"You are a {step.role}.", user=prompt)
                provider = self.client.model

            result = StepResult(
                step_id=step.id,
                role=step.role,
                prompt=prompt,
                output=output,
                provider=provider,
            )
            results.append(result)
            context += f"\n\n## {step.id}\n{output}"
            self._append_trace(run_dir, result)

        self._write_report(run_dir, workflow, results)
        return run_dir

    def _build_prompt(self, objective: str, instruction: str, context: str) -> str:
        return (
            f"Objective:\n{objective}\n\n"
            f"Instruction:\n{instruction}\n\n"
            f"Prior context:\n{context or 'No prior context yet.'}\n\n"
            "Return concise, actionable bullets."
        )

    def _dry_output(self, step_id: str, role: str, objective: str) -> str:
        return (
            f"Dry-run output for `{step_id}` ({role}).\n"
            f"- Objective understood: {objective}\n"
            "- Proposed action: inspect inputs, identify risks, and produce prioritized next steps.\n"
            "- Verification: keep trace logs and generate a final report."
        )

    def _append_trace(self, run_dir: Path, result: StepResult) -> None:
        trace_path = run_dir / "trace.jsonl"
        with trace_path.open("a", encoding="utf-8") as handle:
            handle.write(
                json.dumps(
                    {
                        "step_id": result.step_id,
                        "role": result.role,
                        "provider": result.provider,
                        "prompt": result.prompt,
                        "output": result.output,
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )

    def _write_report(self, run_dir: Path, workflow: Workflow, results: list[StepResult]) -> None:
        lines = [f"# Workflow Report: {workflow.name}", "", "## Objective", workflow.objective, ""]
        for result in results:
            lines.extend(
                [
                    f"## Step: {result.step_id}",
                    f"Role: {result.role}",
                    f"Provider: {result.provider}",
                    "",
                    result.output,
                    "",
                ]
            )
        (run_dir / "report.md").write_text("\n".join(lines), encoding="utf-8")
