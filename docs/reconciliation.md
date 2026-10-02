# Reconciliation

Data quality checks whether individual values conform to rules. **Reconciliation** checks whether the pipeline can account for what happened to the dataset as a whole.

Planned reconciliation evidence includes:

- input and output row counts;
- duplicate and dropped-record counts;
- primary-key preservation;
- records corrected, quarantined and rejected;
- referential-integrity outcomes;
- important numeric totals before and after transformation where meaningful;
- post-load counts against curated targets;
- run identifiers, timestamps and reason codes.

## Core principle

```text
input records
    =
passed
+ corrected
+ quarantined
+ rejected
```

Where transformations change grain, the reconciliation rule must change with the grain rather than forcing a misleading row-count equality.

The objective is that no record silently disappears and every controlled change remains explainable.
