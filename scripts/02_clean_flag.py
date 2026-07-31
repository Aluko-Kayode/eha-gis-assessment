import pandas as pd
import glob

track_files = glob.glob("data/tracks/*.csv")

all_tracks = []
for f in track_files:
    df = pd.read_csv(f)
    all_tracks.append(df)

tracks = pd.concat(all_tracks, ignore_index=True)

# format='mixed' tells pandas: don't assume every row uses the same 
# date format, work it out row by row. dayfirst=True breaks ties in 
# favor of day/month/year when a date could be read either way.
tracks["timestamp"] = pd.to_datetime(
    tracks["timestamp"], format="mixed", dayfirst=True
)

print("Timestamp column type after fix:", tracks["timestamp"].dtype)
print()

# Flag 1: null island, a point sitting exactly at 0,0
tracks["flag_null_island"] = (tracks["longitude"] == 0) & (tracks["latitude"] == 0)
print("Null island points:", tracks["flag_null_island"].sum())

# Flag 2: missing accuracy reading
tracks["flag_missing_accuracy"] = tracks["accuracy_m"].isna()
print("Missing accuracy_m:", tracks["flag_missing_accuracy"].sum())

# Flag 3: implausible speed. 60 km/h is generous for a foot or 
# motorbike based house to house team, anything above that gets flagged
tracks["flag_speed_outlier"] = tracks["speed_kmh"] > 60
print("Speed outliers (>60 km/h):", tracks["flag_speed_outlier"].sum())

print()
print("Total rows with at least one flag:", 
      tracks[["flag_null_island", "flag_missing_accuracy", "flag_speed_outlier"]].any(axis=1).sum())

tracks.to_csv("outputs/tracks_flagged.csv", index=False)
print("Saved to outputs/tracks_flagged.csv")