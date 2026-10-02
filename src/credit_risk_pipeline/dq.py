"""Metadata-driven data-quality checks.

Missingness is owned by completeness. Validity checks evaluate non-null values,
which keeps the dimensions logically separate.
"""

import pandas as pd

def field(required=True,unique=False,min_value=None,max_value=None,allowed=None):
    rules={"required":required,"unique":unique}
    if min_value is not None:
        rules["min"]=min_value
    if max_value is not None:
        rules["max"]=max_value
    if allowed is not None:
        rules["allowed"]=allowed
    return rules

def check_completeness(df,schema):
    results={}
    for column,rules in schema.items():
        if rules.get("required",False):
            missing=int(df[column].isna().sum())
            results[column]={"missing":missing,"passed":missing==0}
    return results

def check_uniqueness(df,schema):
    results={}
    for column,rules in schema.items():
        if rules.get("unique",False):
            duplicates=int(df[column].dropna().duplicated().sum())
            results[column]={"duplicates":duplicates,"passed":duplicates==0}
    return results

def check_validity(df,schema):
    results={}
    for column,rules in schema.items():
        series=df[column]
        present=series.notna()
        invalid=pd.Series(False,index=df.index)

        if "min" in rules:
            invalid|=present&(series<rules["min"])
        if "max" in rules:
            invalid|=present&(series>rules["max"])
        if "allowed" in rules:
            invalid|=present&~series.isin(rules["allowed"])

        invalid_count=int(invalid.sum())
        results[column]={"invalid":invalid_count,"passed":invalid_count==0}
    return results

def run_dq_checks(df,schema):
    return {
        "completeness":check_completeness(df,schema),
        "validity":check_validity(df,schema),
        "uniqueness":check_uniqueness(df,schema)
    }

def dimension_score(results):
    """Return the share of field checks that passed for one DQ dimension."""
    if not results:
        return 1.0
    passed=sum(1 for result in results.values() if result["passed"])
    return passed/len(results)
