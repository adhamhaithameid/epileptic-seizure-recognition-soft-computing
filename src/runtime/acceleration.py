from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AccelerationResult:
    requested: str
    resolved: str
    backend: str
    gpu_count: int
    message: str


def _normalize_device(device: str) -> str:
    value = (device or "auto").strip().lower()
    if value not in {"auto", "cpu", "gpu"}:
        raise ValueError(f"Unsupported device value: {device}")
    return value


def _detect_cuda_devices() -> int:
    try:
        import cupy as cp

        return int(cp.cuda.runtime.getDeviceCount())
    except Exception:
        return 0


def configure_acceleration(device: str = "auto", strict: bool = False) -> AccelerationResult:
    requested = _normalize_device(device)

    if requested == "cpu":
        return AccelerationResult(
            requested=requested,
            resolved="cpu",
            backend="none",
            gpu_count=0,
            message="CPU mode selected.",
        )

    try:
        from cuml import accel as cuml_accel

        cuml_accel.install()
        gpu_count = _detect_cuda_devices()

        if gpu_count > 0:
            return AccelerationResult(
                requested=requested,
                resolved="gpu",
                backend="rapids-cuml-accel",
                gpu_count=gpu_count,
                message="RAPIDS sklearn accelerator enabled.",
            )

        msg = (
            "RAPIDS accelerator is installed but no CUDA GPU was detected. "
            "Falling back to CPU."
        )
        if requested == "gpu" and strict:
            raise RuntimeError(msg)
        return AccelerationResult(
            requested=requested,
            resolved="cpu",
            backend="none",
            gpu_count=gpu_count,
            message=msg,
        )
    except Exception as exc:
        msg = (
            "GPU acceleration is unavailable "
            f"({exc.__class__.__name__}: {exc}). Falling back to CPU."
        )
        if requested == "gpu" and strict:
            raise RuntimeError(msg) from exc
        return AccelerationResult(
            requested=requested,
            resolved="cpu",
            backend="none",
            gpu_count=0,
            message=msg,
        )

