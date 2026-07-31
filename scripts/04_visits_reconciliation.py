import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# --- Load and clean tracks ---
tracks = pd.read_csv("outputs/tracks_flagged.csv", parse_dates=["timestamp"])
# Drop null island points entirely, they are not real locations, unlike 
# other flags we are not analyzing movement from these
tracks = tracks[~tracks["flag_null_island"]].copy()

tracks_gdf = gpd.GeoDataFrame(
    tracks,
    geometry=gpd.points_from_xy(tracks["longitude"], tracks["latitude"]),
    crs="EPSG:4326"
)
# Project to UTM zone 32N, the correct projected CRS for this longitude 
# range in Nigeria, needed for any real distance measurement
tracks_gdf = tracks_gdf.to_crs("EPSG:32632")

# --- Load settlements ---
settlements = pd.read_csv("data/settlement_masterlist.csv")
settlements_gdf = gpd.GeoDataFrame(
    settlements,
    geometry=gpd.points_from_xy(settlements["longitude"], settlements["latitude"]),
    crs="EPSG:4326"
).to_crs("EPSG:32632")

# Buffer each settlement point by 150m. This accounts for GPS accuracy 
# (up to ~58m in this data) plus a team moving around within a settlement 
# rather than standing on one exact point
settlements_gdf["buffer"] = settlements_gdf.geometry.buffer(150)
buffers_gdf = settlements_gdf.set_geometry("buffer")[["settlement_id", "settlement_name", "lga_name", "buffer"]]

# Spatial join: for every GPS point, find which settlement buffer it falls inside
joined = gpd.sjoin(tracks_gdf, buffers_gdf.set_geometry("buffer"), how="inner", predicate="within")

# A settlement counts as GPS-visited if it has at least 5 points inside 
# its buffer, a single stray point passing through is not a visit
visit_counts = joined.groupby("settlement_id").size()
gps_visited = set(visit_counts[visit_counts >= 5].index)

print(f"Settlements with GPS-confirmed visit: {len(gps_visited)}")

# --- Compare against e-tally ---
etally = pd.read_csv("data/etally_daily.csv")
etally_settlements = set(etally["settlement_id"].unique())
print(f"Settlements with an e-tally record: {len(etally_settlements)}")

# --- Inaccessible settlements, excluded from "missed" analysis ---
inaccessible = pd.read_csv("data/inaccessible_settlements.csv")
inaccessible_ids = set(inaccessible["settlement_id"])

all_settlements = set(settlements["settlement_id"])
accessible_settlements = all_settlements - inaccessible_ids

# The real finding: planned, accessible settlements with NO gps visit 
# and NO etally record at all
missed = accessible_settlements - gps_visited - etally_settlements
print(f"Planned, accessible settlements with no GPS visit and no e-tally record: {len(missed)}")

# Settlements reported in e-tally but GPS never confirms a visit, 
# worth flagging as a possible data entry or fabrication concern
reported_not_visited = (etally_settlements - gps_visited) - inaccessible_ids
print(f"Reported in e-tally but no GPS confirmation: {len(reported_not_visited)}")

# Save the missed list with coordinates, we need this for the map and clustering
missed_gdf = settlements[settlements["settlement_id"].isin(missed)]
missed_gdf.to_csv("outputs/missed_settlements.csv", index=False)

reported_not_visited_df = settlements[settlements["settlement_id"].isin(reported_not_visited)]
reported_not_visited_df.to_csv("outputs/reported_not_visited.csv", index=False)

print("Saved outputs/missed_settlements.csv and outputs/reported_not_visited.csv")
