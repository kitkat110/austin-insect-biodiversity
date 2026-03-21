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

# Richness grid
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="4%", pad=0.1)

grid_gdf.plot(ax=ax, column="normalized_richness", cmap="YlGnBu", linewidth=0.3, alpha=0.85,
              cax=cax, legend=True, zorder=2, vmin=0,
              missing_kwds={
                  "color":"lightgrey",
                  "edgecolor": "red",
                  "hatch": "///",
                  "label": "Too few observations"
                }
            )

# Top 10 cells
top_cells.plot(ax=ax, facecolor="none", edgecolor="#e63946", linewidth=2, zorder=3)

# Austin boundary on top
austin.plot(ax=ax, color="none", edgecolor="#555555", linewidth=1.2, zorder=4)

cax.set_ylabel('Number of species/Total observations', fontsize=9, labelpad=8)
ax.set_title('Austin Insect Biodiversity', fontsize=18, fontweight='bold')
ax.set_xlabel('Longitude', fontsize=9)
ax.set_ylabel('Latitude', fontsize=9)
ax.tick_params(labelsize=8)
top_patch = mpatches.Patch(facecolor="none", edgecolor="#e63946", linewidth=2, label="Top 10 biodiversity cells")
ax.legend(handles=[top_patch], loc="lower left", fontsize=9, framealpha=0.9)

plt.savefig("austin_insect_richness.png", dpi=150, bbox_inches="tight")
plt.show()

