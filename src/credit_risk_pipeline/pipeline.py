"""Governed pipeline orchestration skeleton.

Business rules live in their own engines; this module defines execution order.
"""

from .gates import GateStatus

PIPELINE_STAGES=[
    "extract",
    "profile",
    "validate",
    "quality_gate",
    "clean",
    "validate_again",
    "quality_gate_again",
    "transform",
    "reconcile",
    "classify",
    "load"
]

RECORD_OUTCOMES=[
    "PASS",
    "CORRECTED",
    "QUARANTINE",
    "REJECT"
]

def stage_plan():
    return PIPELINE_STAGES.copy()

def stop_required(gate_decision):
    return gate_decision.status==GateStatus.STOP
