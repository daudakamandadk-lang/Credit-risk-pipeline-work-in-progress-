# Data Contracts

A pipeline should know what it expects before it starts cleaning data.

The planned data-contract layer describes:

- dataset name and grain;
- primary and foreign keys;
- required and optional fields;
- expected data types;
- allowed categorical values;
- numeric/date boundaries;
- uniqueness expectations;
- Critical Data Elements;
- rule severity;
- quality thresholds and stop conditions.

The validation engine reads this metadata rather than embedding every rule inside procedural code.

## Example concept

```python
schema={
    "applicant_id":{
        "required":True,
        "unique":True
    },
    "requested_amount":{
        "required":True,
        "min":0
    },
    "product_type":{
        "required":True,
        "allowed":["Personal Loan","Mortgage","Asset Finance"]
    }
}
```

This is intentionally simple. The objective is to make data expectations explicit and versionable before introducing a heavier schema or contract framework.
