"""Configurable data-quality gate evaluation."""

from dataclasses import dataclass
from enum import Enum

class GateStatus(str,Enum):
    PASS="PASS"
    WARN="WARN"
    STOP="STOP"

@dataclass(frozen=True)
class GateDecision:
    score:float
    status:GateStatus
    pass_threshold:float
    warn_threshold:float

def evaluate_gate(score,pass_threshold,warn_threshold):
    """Convert a quality score into PASS, WARN or STOP.

    Thresholds are supplied by configuration/business policy rather than
    hard-coded into the engine.
    """
    if not 0<=score<=1:
        raise ValueError("score must be between 0 and 1")
    if not 0<=warn_threshold<=pass_threshold<=1:
        raise ValueError("require 0 <= warn_threshold <= pass_threshold <= 1")

    if score>=pass_threshold:
        status=GateStatus.PASS
    elif score>=warn_threshold:
        status=GateStatus.WARN
    else:
        status=GateStatus.STOP

    return GateDecision(
        score=score,
        status=status,
        pass_threshold=pass_threshold,
        warn_threshold=warn_threshold
    )

def can_continue(decision,allow_warning=True):
    if decision.status==GateStatus.STOP:
        return False
    if decision.status==GateStatus.WARN and not allow_warning:
        return False
    return True
