# Wider Credit-Risk System Roadmap

This pipeline is one layer of a larger system.

## 1. Data foundation and scenarios

- canonical applicant, income, application, loan and repayment structures;
- synthetic/reference data;
- source catalogue and provenance;
- scenario configuration.

## 2. Governed ETL and data quality

- extraction and profiling;
- metadata-driven validation;
- completeness, validity, uniqueness, consistency and timeliness controls;
- cleaning and standardisation;
- quality gates;
- transformation and reconciliation;
- PASS / CORRECTED / QUARANTINE / REJECT handling;
- curated trusted data.

**This public repository currently focuses here.**

## 3. Statistical credit-risk engine

- feature engineering;
- distribution/statistical analysis;
- probability of default (PD);
- loss given default (LGD);
- exposure at default (EAD);
- expected loss;
- risk grades and reason codes;
- stress/scenario analysis;
- separation of risk estimates from lending policy.

## 4. Machine learning and model operations

- logistic-regression baseline and candidate models;
- training/validation/out-of-time testing;
- calibration, discrimination and stability;
- explainability;
- model comparison;
- monitoring and retraining criteria;
- deployment only after the governed data and statistical baseline are stable.

The development principle is:

**build -> break -> understand -> refactor -> test -> commit -> repeat**
