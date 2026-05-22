from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class WorkflowStep:
    id: str
    role: str
    instruction: str


@dataclass(slots=True)
class Workflow:
    name: str
    objective: str
    steps: list[WorkflowStep] = field(default_factory=list)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "Workflow":
        missing = [key for key in ("name", "objective", "steps") if key not in payload]
        if missing:
            raise ValueError(f"workflow missing required keys: {', '.join(missing)}")

        steps = []
        for raw in payload["steps"]:
            for key in ("id", "role", "instruction"):
                if key not in raw:
                    raise ValueError(f"workflow step missing key: {key}")
            steps.append(
                WorkflowStep(
                    id=str(raw["id"]),
                    role=str(raw["role"]),
                    instruction=str(raw["instruction"]),
                )
            )

        if not steps:
            raise ValueError("workflow must contain at least one step")

        return cls(name=str(payload["name"]), objective=str(payload["objective"]), steps=steps)


@dataclass(slots=True)
class StepResult:
    step_id: str
    role: str
    prompt: str
    output: str
    provider: str
