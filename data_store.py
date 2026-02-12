import pandas as pd
import os

COLUMNS = [
    "Timestamp",
    "Name",
    "Email",
    "Age",
    "Study_Hours",
    "Sleep_Hours",
    "Screen_Time",
    "Physical_Activity",
    "Academic_Pressure",
    "Sleep_Quality",
    "Stress_Level",
    "Stress_Score"
]

def load_records():
    if not os.path.exists("student_records.csv") or os.path.getsize("student_records.csv") == 0:
        return pd.DataFrame(columns=COLUMNS)

    try:
        df = pd.read_csv("student_records.csv")
    except pd.errors.EmptyDataError:
        return pd.DataFrame(columns=COLUMNS)

    for col in COLUMNS:
        if col not in df.columns:
            df[col] = None

    return df[COLUMNS]

def save_record(record):
    df = load_records()
    df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)
    df.to_csv("student_records.csv", index=False)
