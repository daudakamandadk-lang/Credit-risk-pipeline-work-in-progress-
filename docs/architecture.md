# Architecture

## Purpose

This repository represents the **governed data-pipeline layer** of a larger credit-risk system.

The design assumes that a statistical or machine-learning risk model should not consume source data directly. Data first passes through controlled ingestion, profiling, validation, data-quality gates, cleaning, transformation and reconciliation.

```text
Source / Scenario
      |
      v
Extraction
      |
      v
Profiling
      |
      v
Validation ---------> DQ evidence
      |
      v
Quality Gate --STOP--> quarantine / investigation
      |
      v
Cleaning
      |
      v
Revalidation
      |
      v
Transformation
      |
      v
Reconciliation
      |
      v
Classification
      |
      v
Load / Curated Layer
      |
      v
Feature Engineering
      |
      v
Statistical Credit-Risk Engine
      |
      v
PD / LGD / EAD / Expected Loss / Risk Grades
      |
      v
Policy / Decisions / Reporting
```

## Component boundaries

**Extraction** gets the data and records structural metadata.

**Profiling** describes what actually arrived before assumptions are imposed.

**Validation** evaluates data against explicit schema and rule metadata.

**Data-quality gates** decide whether the pipeline can continue, continue with a warning, or stop.

**Cleaning** standardises or repairs only where an approved correction exists.

**Revalidation** proves that cleaning did not introduce or leave unresolved defects.

**Transformation** derives business-ready structures and fields.

**Reconciliation** proves that records and important totals remain explainable across processing.

**Classification** assigns controlled outcomes such as PASS, CORRECTED, QUARANTINE or REJECT.

**Loading** persists only the intended outputs into the next governed layer.

## Downstream system

The curated output is intended to become the input to feature engineering and a statistical credit-risk engine. That later engine will estimate quantities such as PD, LGD, EAD and expected loss, with risk estimates kept separate from lending-policy decisions.

Machine learning is a later layer, not a substitute for governed data engineering.
