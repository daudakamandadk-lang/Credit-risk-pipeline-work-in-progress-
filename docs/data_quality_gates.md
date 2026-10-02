# Data Quality Gates

## Why gates exist

A validation report by itself does not control a pipeline. A **data-quality gate** converts quality evidence into an execution decision.

This project uses three gate states:

- **PASS** — quality meets the configured acceptance threshold.
- **WARN** — quality is below the preferred threshold but above the configured stop threshold; continuation must be explicitly allowed.
- **STOP** — quality is below the minimum threshold and the pipeline should not continue automatically.

The public prototype intentionally does not hard-code business thresholds. Thresholds belong to configuration/policy because the acceptable level depends on the dataset, Critical Data Element and use case.

## Current dimensions

Implemented prototype dimensions:

- completeness;
- validity;
- uniqueness.

Planned hardening includes:

- consistency;
- timeliness;
- referential integrity;
- business-rule validation;
- reconciliation checks.

## Gate placement

The first gate sits after initial validation:

```text
extract -> profile -> validate -> GATE
```

The second gate sits after cleaning/revalidation:

```text
clean -> validate again -> GATE AGAIN
```

This prevents a pipeline from assuming that a cleaning step automatically produced trustworthy data.

## Record handling

Dataset-level gates and record-level classification solve different problems.

A dataset can have an overall gate decision while individual records are classified as:

- **PASS** — accepted without correction;
- **CORRECTED** — accepted after an approved deterministic correction;
- **QUARANTINE** — isolated for investigation or manual review;
- **REJECT** — cannot be accepted under the defined rules.

Bad records should not simply disappear. Reason codes, keys and lineage should be preserved so processing remains auditable.

## Scoring

The current helper can calculate the share of field checks passed within one quality dimension. A later implementation can combine dimensions, Critical Data Element weighting and severity rules once those policies are explicitly defined and tested.
