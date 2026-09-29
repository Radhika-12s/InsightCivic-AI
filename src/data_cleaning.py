# AI_Emergency_Intelligence_System\src\data_cleaning
import pandas as pd
import os

# -----------------------------
# File Paths
# -----------------------------
BASE_PATH = os.path.dirname(os.path.dirname(__file__))

RAW_PATH = os.path.join(BASE_PATH, "data_raw")
PROCESSED_PATH = os.path.join(BASE_PATH, "data_processed")

crime_file = os.path.join(RAW_PATH, "crime_chicago_2026_jan.csv")
traffic_file = os.path.join(RAW_PATH, "traffic_crash_chicago_2026_jan.csv")
weather_file = os.path.join(RAW_PATH, "weather_chicago_2026_jan.csv")
fire_file = os.path.join(RAW_PATH, "fire_stations_chicago.csv")

# -----------------------------
# Create processed folder if not exists
# -----------------------------
os.makedirs(PROCESSED_PATH, exist_ok=True)

# -----------------------------
#Clean Crime Data
# -----------------------------
print("Cleaning Crime Data...")
crime = pd.read_csv(crime_file)

crime = crime[[
    "Date",
    "Primary Type",
    "Arrest",
    "Domestic",
    "District",
    "Community Area",
    "Latitude",
    "Longitude"
]]

crime["Date"] = pd.to_datetime(crime["Date"])
crime = crime.dropna(subset=["Latitude", "Longitude"])

crime.to_csv(os.path.join(PROCESSED_PATH, "crime_cleaned.csv"), index=False)
print("Crime cleaned ✅")

# -----------------------------
#  Clean Traffic Crash Data
# -----------------------------
print("Cleaning Traffic Data...")
traffic = pd.read_csv(traffic_file)

traffic = traffic[[
    "CRASH_DATE",
    "WEATHER_CONDITION",
    "LIGHTING_CONDITION",
    "FIRST_CRASH_TYPE",
    "CRASH_TYPE",
    "INJURIES_TOTAL",
    "INJURIES_FATAL",
    "LATITUDE",
    "LONGITUDE"
]]

traffic["CRASH_DATE"] = pd.to_datetime(traffic["CRASH_DATE"])
traffic = traffic.dropna(subset=["LATITUDE", "LONGITUDE"])

traffic.to_csv(os.path.join(PROCESSED_PATH, "traffic_cleaned.csv"), index=False)
print("Traffic cleaned ✅")

# -----------------------------
#  Clean Weather Data
# -----------------------------
print("Cleaning Weather Data...")
weather = pd.read_csv(weather_file)

weather = weather[[
    "DATE",
    "PRCP",
    "TAVG",
    "TMAX",
    "TMIN"
]]

weather["DATE"] = pd.to_datetime(weather["DATE"])

weather.to_csv(os.path.join(PROCESSED_PATH, "weather_cleaned.csv"), index=False)
print("Weather cleaned ✅")

# -----------------------------
#  Clean Fire Stations Data
# -----------------------------
print("Cleaning Fire Stations Data...")
fire = pd.read_csv(fire_file)

# Extract latitude & longitude from LOCATION column
fire[["Latitude", "Longitude"]] = fire["LOCATION"].str.extract(r"\((.*), (.*)\)")

fire["Latitude"] = fire["Latitude"].astype(float)
fire["Longitude"] = fire["Longitude"].astype(float)

fire = fire[["NAME", "ADDRESS", "Latitude", "Longitude"]]

fire.to_csv(os.path.join(PROCESSED_PATH, "fire_stations_cleaned.csv"), index=False)
print("Fire stations cleaned ✅")

print("\nAll datasets cleaned successfully 🚀")