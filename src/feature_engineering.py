# AI_Emergency_Intelligence_System\src\feature_engineering
import pandas as pd
import os
import numpy as np

# -----------------------------
# File Paths
# -----------------------------
BASE_PATH = os.path.dirname(os.path.dirname(__file__))
PROCESSED_PATH = os.path.join(BASE_PATH, "data_processed")

crime_file = os.path.join(PROCESSED_PATH, "crime_cleaned.csv")
traffic_file = os.path.join(PROCESSED_PATH, "traffic_cleaned.csv")
weather_file = os.path.join(PROCESSED_PATH, "weather_cleaned.csv")

print("Loading cleaned datasets...")

crime = pd.read_csv(crime_file, parse_dates=["Date"])
traffic = pd.read_csv(traffic_file, parse_dates=["CRASH_DATE"])
weather = pd.read_csv(weather_file, parse_dates=["DATE"])

# -----------------------------
#  Extract Date & Hour
# -----------------------------
crime["date"] = crime["Date"].dt.date
crime["hour"] = crime["Date"].dt.hour

traffic["date"] = traffic["CRASH_DATE"].dt.date
traffic["hour"] = traffic["CRASH_DATE"].dt.hour

# -----------------------------
#  Hourly Aggregation
# -----------------------------
crime_hourly = (
    crime.groupby(["date", "hour"])
    .size()
    .reset_index(name="crime_count")
)

crash_hourly = (
    traffic.groupby(["date", "hour"])
    .size()
    .reset_index(name="crash_count")
)

# -----------------------------
#  Merge Crime + Crash
# -----------------------------
merged = pd.merge(
    crime_hourly,
    crash_hourly,
    on=["date", "hour"],
    how="outer"
).fillna(0)

# -----------------------------
#  Merge Weather (Daily → Hourly)
# -----------------------------
weather["date"] = weather["DATE"].dt.date

merged = pd.merge(
    merged,
    weather[["date", "PRCP", "TAVG", "TMAX", "TMIN"]],
    on="date",
    how="left"
)

# Fill missing weather safely
merged[["PRCP", "TAVG", "TMAX", "TMIN"]] = merged[
    ["PRCP", "TAVG", "TMAX", "TMIN"]
].fillna(0)

# -----------------------------
#  Advanced Feature Engineering
# -----------------------------

# Normalize safely
merged["crime_score"] = merged["crime_count"] / (
    merged["crime_count"].max() + 1e-6
)

merged["crash_score"] = merged["crash_count"] / (
    merged["crash_count"].max() + 1e-6
)

# Weather severity indicators
merged["is_rain"] = (merged["PRCP"] > 0).astype(int)
merged["is_cold"] = (merged["TAVG"] < 32).astype(int)

merged["weather_factor"] = (
    merged["is_rain"] * 0.2 +
    merged["is_cold"] * 0.1
)

# Peak hour indicator
merged["is_peak_hour"] = merged["hour"].apply(
    lambda x: 1 if (7 <= x <= 10) or (17 <= x <= 20) else 0
)

# Final Risk Score
merged["emergency_risk_score"] = (
    0.45 * merged["crime_score"] +
    0.30 * merged["crash_score"] +
    0.15 * merged["weather_factor"] +
    0.10 * merged["is_peak_hour"]
)

# -----------------------------
# Save Dataset
# -----------------------------
output_path = os.path.join(
    PROCESSED_PATH,
    "final_emergency_hourly_dataset.csv"
)

merged.to_csv(output_path, index=False)

print("Feature engineering completed 🚀")
print("Saved as final_emergency_hourly_dataset.csv")