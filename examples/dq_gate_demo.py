"""Small synthetic demonstration of DQ checks and a quality gate.

The thresholds below are illustrative only; they are not lending policy.
"""

import pandas as pd
from credit_risk_pipeline.dq import field,run_dq_checks,dimension_score
from credit_risk_pipeline.gates import evaluate_gate

data=pd.DataFrame({
    "application_id":["A001","A002","A003"],
    "requested_amount":[1200,-50,800],
    "product_type":["Personal Loan","Mortgage","Personal Loan"]
})

schema={
    "application_id":field(required=True,unique=True),
    "requested_amount":field(required=True,min_value=0),
    "product_type":field(
        required=True,
        allowed=["Personal Loan","Mortgage","Asset Finance"]
    )
}

results=run_dq_checks(data,schema)
validity_score=dimension_score(results["validity"])

decision=evaluate_gate(
    score=validity_score,
    pass_threshold=1.00,
    warn_threshold=0.60
)

print("DQ results:",results)
print("Validity score:",round(validity_score,3))
print("Gate decision:",decision.status.value)
