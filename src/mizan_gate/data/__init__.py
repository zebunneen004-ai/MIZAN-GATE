"""Read-only dataset adapters and data-contract validation."""

from mizan_gate.data.elliptic import (
    DataContractError,
    EllipticStudy1Data,
    load_elliptic_study1,
)

__all__ = ["DataContractError", "EllipticStudy1Data", "load_elliptic_study1"]
