#!/usr/bin/env python3
"""Cross-platform runner for the full soft-computing pipeline."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def _run_step(label: str, cmd: list[str]) -> None:
    print(f"\n==> {label}")
    print(" ".join(cmd))
    subprocess.run(cmd, cwd=ROOT, check=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fresh", action="store_true", help="Start benchmark from scratch.")
    parser.add_argument("--max-rows", type=int, default=None, help="Optional smoke-test row cap.")
    parser.add_argument("--checkpoint-every", type=int, default=120)
    parser.add_argument("--jobs", type=int, default=1, help="Parallel model workers.")
    parser.add_argument("--selection-jobs", type=int, default=1, help="Parallel SFS workers.")
    parser.add_argument("--allow-partial", action="store_true", help="Allow partial validation mode.")
    parser.add_argument(
        "--device",
        choices=["auto", "cpu", "gpu"],
        default="auto",
        help="Execution target for check/run stages.",
    )
    parser.add_argument(
        "--strict-device",
        action="store_true",
        help="Fail when --device gpu is requested but acceleration cannot be enabled.",
    )
    args = parser.parse_args()

    py = sys.executable

    _run_step("Fetch dataset", [py, "src/cli/fetch_data.py"])

    check_cmd = [py, "src/cli/check_env.py", "--device", args.device]
    if args.strict_device:
        check_cmd.append("--strict-device")
    _run_step("Check environment", check_cmd)

    run_cmd = [
        py,
        "src/cli/run_experiments.py",
        "--checkpoint-every",
        str(max(1, args.checkpoint_every)),
        "--jobs",
        str(max(1, args.jobs)),
        "--selection-jobs",
        str(max(1, args.selection_jobs)),
        "--device",
        args.device,
    ]
    if args.strict_device:
        run_cmd.append("--strict-device")
    if args.fresh:
        run_cmd.append("--fresh")
    if args.max_rows is not None:
        run_cmd.extend(["--max-rows", str(args.max_rows)])
    _run_step("Run benchmark", run_cmd)

    validate_cmd = [py, "src/cli/validate_cartesian_outputs.py"]
    if args.allow_partial:
        validate_cmd.append("--allow-partial")
    _run_step("Validate outputs", validate_cmd)

    _run_step("Generate paper drafts", [py, "src/cli/generate_paper_drafts.py"])
    print("\nAll steps completed.")


if __name__ == "__main__":
    main()

