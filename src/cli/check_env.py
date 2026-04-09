#!/usr/bin/env python3
"""Environment and dataset readiness check."""

from __future__ import annotations

import argparse
import csv
import importlib.util
import platform
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

RAW = ROOT / "data" / "raw" / "epileptic_seizure_recognition" / "epileptic_seizure_data.csv"

from src.runtime.acceleration import configure_acceleration  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--device",
        choices=["auto", "cpu", "gpu"],
        default="auto",
        help="Validate runtime target: auto (prefer GPU), cpu, or gpu.",
    )
    parser.add_argument(
        "--strict-device",
        action="store_true",
        help="Fail if GPU was requested but cannot be enabled.",
    )
    args = parser.parse_args()

    required = [
        "numpy",
        "pandas",
        "sklearn",
        "scipy",
    ]
    optional = ["matplotlib", "seaborn", "cupy", "cuml"]

    print("System check:")
    print(f"- platform: {platform.platform()}")
    print(f"- python: {platform.python_version()}")

    print("\nDependency check:")
    missing = []
    for mod in required:
        ok = importlib.util.find_spec(mod) is not None
        print(f"- {mod}: {'OK' if ok else 'MISSING'}")
        if not ok:
            missing.append(mod)

    print("\nDataset check:")
    if RAW.exists():
        with RAW.open() as f:
            r = csv.reader(f)
            rows = list(r)
        print(f"- CSV found: {RAW}")
        print(f"- columns: {len(rows[0]) if rows else 0}")
        print(f"- rows: {max(0, len(rows)-1)}")
    else:
        print(f"- CSV missing: {RAW}")

    if missing:
        print("\nMissing dependencies detected. Install with:")
        print("python -m pip install --disable-pip-version-check -r requirements.txt")
        raise SystemExit(1)

    print("\nOptional deps:")
    for mod in optional:
        ok = importlib.util.find_spec(mod) is not None
        print(f"- {mod}: {'OK' if ok else 'MISSING'}")

    accel = configure_acceleration(device=args.device, strict=args.strict_device)
    print("\nAcceleration check:")
    print(f"- requested: {accel.requested}")
    print(f"- resolved: {accel.resolved}")
    print(f"- backend: {accel.backend}")
    print(f"- gpu_devices: {accel.gpu_count}")
    print(f"- details: {accel.message}")

    print("\nEnvironment ready.")


if __name__ == "__main__":
    main()
