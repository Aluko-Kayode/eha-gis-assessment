import pandas as pd
import glob

# Load and combine all 160 track files into one table
track_files = glob.glob("data/tracks/*.csv")
print(f"Found {len(track_files)} track files")

all_tracks = []
for f in track_files:
    df = pd.read_csv(f, parse_dates=["timestamp"], dayfirst=True)
    all_tracks.append(df)

tracks = pd.concat(all_tracks, ignore_index=True)

print(f"Total GPS points: {len(tracks)}")
print(tracks.dtypes)
print(tracks.describe())

# Save the combined file so we don't have to redo this every time
tracks.to_csv("outputs/tracks_combined.csv", index=False)
