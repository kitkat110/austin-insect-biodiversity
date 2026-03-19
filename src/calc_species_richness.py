import logging
import pandas as pd
import numpy as np


# -------------------------
# Constants
# -------------------------
GRID_SIZE = 0.01 # ~1 km


# -------------------------
# Functions
# -------------------------
def create_grid(rec_df: str) -> None:
    """
    Creates map grid based on record coordinates.

    Args:
        rec_df: List of records as a dataframe.

    Returns:
        None
    """

    min_lat, min_lon = rec_df["latitude"].min(), rec_df["longitude"].min()
    max_lat, max_lon = rec_df("latitude").max(), rec_df["longitude"].max()

    lat_bins = pd.interval_range(start=min_lat, end=max_lat + GRID_SIZE, freq=GRID_SIZE)
    lon_bins = pd.interval_range(start=min_lon, end=max_lon + GRID_SIZE, freq=GRID_SIZE)

    rec_df["lat_bin"] = pd.cut(rec_df["latitude"], bins=lat_bins)
    rec_df["lon_bin"] = pd.cut(rec_df["longitude"], bins=lon_bins)
