import logging
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import osmnx as ox
from shapely.geometry import box


richness = pd.read_csv("data/species_richness.csv")

def interval_to_midpoint(s):
    left, right = s.strip("()[]").split(",")
    return (float(left) + float(right)) / 2

richness["lat_bin"] = richness["lat_bin"].apply(interval_to_midpoint)
richness["lon_bin"] = richness["lon_bin"].apply(interval_to_midpoint)

austin = ox.geocode_to_gdf("Austin, Texas, USA")
austin = austin.to_crs(epsg=4326)

GRID_SIZE = 0.03

richness["geometry"] = richness.apply(
    lambda row: box(
        row["lon_bin"] - GRID_SIZE / 2,
        row["lat_bin"] - GRID_SIZE / 2,
        row["lon_bin"] + GRID_SIZE / 2,
        row["lat_bin"] + GRID_SIZE / 2,
    ),
    axis=1,
)

grid_gdf = gpd.GeoDataFrame(richness, geometry="geometry", crs="EPSG:4326")
grid_gdf = gpd.clip(grid_gdf, austin)

# top_cells = grid_gdf[grid_gdf["richness_rank"] <= 10]

fig, ax = plt.subplots(1, 1)
fig.set_size_inches(10, 10)
austin.plot(ax=ax, color="#f0f0f0", edgecolor="#cccccc", linewidth=1)
grid_gdf.plot(ax=ax)
plt.show()

