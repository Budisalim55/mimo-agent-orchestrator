from __future__ import annotations

import argparse
from pathlib import Path

from .runner import WorkflowRunner


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run an agent workflow against an LLM provider.")
    sub = parser.add_subparsers(dest="command", required=True)

    run = sub.add_parser("run", help="Run a YAML workflow")
    run.add_argument("workflow", type=Path)
    run.add_argument("--dry-run", action="store_true", help="Run without calling a provider API")
    run.add_argument("--output-dir", default="runs")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.command == "run":
        runner = WorkflowRunner(output_dir=args.output_dir)
        workflow = runner.load(args.workflow)
        run_dir = runner.run(workflow, dry_run=args.dry_run)
        print(f"workflow completed: {run_dir}")
