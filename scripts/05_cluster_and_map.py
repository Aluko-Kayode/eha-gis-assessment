import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors
import numpy as np

np.random.seed(42)

missed = pd.read_csv("outputs/missed_settlements.csv")
all_settlements = pd.read_csv("data/settlement_masterlist.csv")

missed_gdf = gpd.GeoDataFrame(
    missed, geometry=gpd.points_from_xy(missed["longitude"], missed["latitude"]), crs="EPSG:4326"
).to_crs("EPSG:32632")
all_gdf = gpd.GeoDataFrame(
    all_settlements, geometry=gpd.points_from_xy(all_settlements["longitude"], all_settlements["latitude"]), crs="EPSG:4326"
).to_crs("EPSG:32632")

def mean_nn_distance(coords):
    nn = NearestNeighbors(n_neighbors=2).fit(coords)
    distances, _ = nn.kneighbors(coords)
    return distances[:, 1].mean()

observed = mean_nn_distance(np.column_stack([missed_gdf.geometry.x, missed_gdf.geometry.y]))

all_coords = np.column_stack([all_gdf.geometry.x, all_gdf.geometry.y])
n_missed = len(missed)

# Draw 500 random samples of the SAME size (253) from all settlements, 
# this is the fair, size-matched baseline
random_means = []
for _ in range(500):
    sample_idx = np.random.choice(len(all_coords), size=n_missed, replace=False)
    random_means.append(mean_nn_distance(all_coords[sample_idx]))
random_means = np.array(random_means)

print(f"Observed mean nearest-neighbor distance (missed settlements): {observed:.0f} m")
print(f"Random same-size samples: mean {random_means.mean():.0f} m, range {random_means.min():.0f}-{random_means.max():.0f} m")
percentile = (random_means < observed).mean() * 100
print(f"Observed value sits at the {percentile:.0f}th percentile of random draws")
print("Below 5th percentile = significantly clustered. Above 95th = significantly dispersed. In between = looks like chance.")

print()
print("Missed settlements by LGA (raw counts):")
print(missed["lga_name"].value_counts())
print()
print("Total settlements by LGA (for context, is Idi-Oro just bigger, or disproportionately missed):")
print(all_settlements["lga_name"].value_counts())