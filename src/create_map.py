import logging
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import osmnx as ox
from shapely.geometry import box
from mpl_toolkits.axes_grid1 import make_axes_locatable


richness = pd.read_csv("data/species_richness.csv")

def interval_to_midpoint(s):
    left, right = s.strip("()[]").split(",")
    return (float(left) + float(right)) / 2

richness["lat_bin"] = richness["lat_bin"].apply(interval_to_midpoint)
richness["lon_bin"] = richness["lon_bin"].apply(interval_to_midpoint)

austin = ox.geocode_to_gdf("Austin, Texas, USA")
austin = austin.to_crs(epsg=4326)

# Pull Austin parks
parks = ox.features_from_place("Austin, Texas, USA", tags={"leisure": "park"})
parks = parks[parks.geometry.type.isin(["Polygon", "MultiPolygon"])]
parks = parks.to_crs(epsg=4326)

# Pull Austin water bodies
water = ox.features_from_place("Austin, Texas, USA", tags={"natural": "water"})
water = water[water.geometry.type.isin(["Polygon", "MultiPolygon"])]
water = water.to_crs(epsg=4326)
water = gpd.clip(water, austin)

GRID_SIZE = 0.025

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

top_cells = grid_gdf[grid_gdf["richness_rank"] <= 10]

fig, ax = plt.subplots(1, 1)
fig.set_size_inches(10, 10)

# Base layer
austin.plot(ax=ax, color="#e8e8e8", edgecolor="#aaaaaa", linewidth=0.8, zorder=1)

# Park grid
parks.plot(ax=ax, color="#6b8e4e", edgecolor="#3d5a2a", linewidth=0.5, alpha=0.6, zorder=3)

# Water grid
water.plot(ax=ax, color="#a8c8e8", edgecolor="#4a90c4", linewidth=0.5, alpha=0.6, zorder=4)

# Richness grid
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="4%", pad=0.1)

grid_gdf.plot(ax=ax, column="species_count", cmap="YlGnBu", linewidth=0.3, alpha=1,
              cax=cax, legend=True, zorder=2, vmin=0,
              missing_kwds={
                  "color":"lightgrey",
                  "edgecolor": "red",
                  "hatch": "///",
                  "label": "Too few observations"
                }
            )


# Austin boundary on top
austin.plot(ax=ax, color="none", edgecolor="#555555", linewidth=1.2, zorder=5)

cax.set_ylabel('Species Count', fontsize=9, labelpad=8)
ax.set_title('Austin Insect Biodiversity', fontsize=18, fontweight='bold')
ax.set_xlabel('Longitude', fontsize=9)
ax.set_ylabel('Latitude', fontsize=9)
ax.tick_params(labelsize=8)

# Park patch legend
park_patch = mpatches.Patch(facecolor="#6b8e4e", edgecolor="#3d5a2a", alpha=0.6, label="Parks")
ax.legend(handles=[park_patch], loc="lower left", fontsize=9, framealpha=0.9)

# Water patch legend
water_patch = mpatches.Patch(facecolor="#a8c8e8", edgecolor="#4a90c4", alpha=0.6, label="Water")
ax.legend(handles=[park_patch, water_patch], loc="lower left", fontsize=9, framealpha=0.9)

plt.savefig("austin_insect_richness.png", dpi=150, bbox_inches="tight")
plt.show()

