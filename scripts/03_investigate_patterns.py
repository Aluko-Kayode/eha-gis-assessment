import pandas as pd

tracks = pd.read_csv("outputs/tracks_flagged.csv", parse_dates=["timestamp"])

print("=== Null island points by logger ===")
print(tracks[tracks["flag_null_island"]]["logger_id"].value_counts())
print()

print("=== Missing accuracy by logger ===")
print(tracks[tracks["flag_missing_accuracy"]]["logger_id"].value_counts().head(10))
print()

print("=== Speed outliers by team ===")
print(tracks[tracks["flag_speed_outlier"]]["team_id"].value_counts().head(10))
print()

print("=== A closer look at ten speed outlier rows ===")
print(tracks[tracks["flag_speed_outlier"]][
    ["team_id", "logger_id", "timestamp", "speed_kmh"]
].head(10))