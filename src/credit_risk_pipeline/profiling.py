"""Reusable profiling helpers used before validation and cleaning."""

import pandas as pd

def profile_categorical(series,top_n=5):
    counts=series.value_counts(dropna=False)
    percentages=series.value_counts(dropna=False,normalize=True)*100
    return {
        "mode":series.mode().iloc[0] if not series.mode().empty else None,
        "top_values":counts.head(top_n).to_dict(),
        "top_percentages":percentages.head(top_n).round(2).to_dict()
    }

def profile_numeric(series):
    stats=series.describe()
    q1=stats["25%"]
    q3=stats["75%"]
    iqr=q3-q1
    lower=q1-1.5*iqr
    upper=q3+1.5*iqr
    outlier_mask=(series<lower)|(series>upper)
    return {
        "count":int(stats["count"]),
        "mean":stats["mean"],
        "std":stats["std"],
        "min":stats["min"],
        "q1":q1,
        "median":stats["50%"],
        "q3":q3,
        "max":stats["max"],
        "zeros":int((series==0).sum()),
        "negative":int((series<0).sum()),
        "outliers":int(outlier_mask.sum())
    }

def profile_date(series,reference_date=None):
    valid=series.dropna()
    profile={
        "count":int(valid.count()),
        "earliest":valid.min() if not valid.empty else None,
        "latest":valid.max() if not valid.empty else None,
        "range_days":(valid.max()-valid.min()).days if not valid.empty else None
    }
    if reference_date is not None:
        profile["future_dates"]=int((valid>reference_date).sum())
    return profile

def profile_data(df,top_n=5,reference_date=None):
    profile={
        "rows":len(df),
        "columns":len(df.columns),
        "duplicate_rows":int(df.duplicated().sum()),
        "fields":{}
    }
    for column in df.columns:
        series=df[column]
        field_profile={
            "dtype":str(series.dtype),
            "missing":int(series.isna().sum()),
            "missing_pct":round(series.isna().mean()*100,2),
            "unique":int(series.nunique())
        }
        if pd.api.types.is_datetime64_any_dtype(series):
            field_profile["date"]=profile_date(series,reference_date)
        elif pd.api.types.is_numeric_dtype(series):
            field_profile["numeric"]=profile_numeric(series)
        else:
            field_profile["categorical"]=profile_categorical(series,top_n)
        profile["fields"][column]=field_profile
    return profile
