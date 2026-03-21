import logging
import pandas as pd 

# -------------------------
# Constants
# -------------------------
GRID_SIZE = 0.025 # ~2.5 km


# -------------------------
# Functions
# -------------------------
def create_grid(rec_df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates map grid based on record coordinates.

    Args:
        rec_df: List of records as a dataframe.

    Returns:
        None: This function does not return a value.
    """

    min_lat, min_lon = rec_df["latitude"].min(), rec_df["longitude"].min()
    max_lat, max_lon = rec_df["latitude"].max(), rec_df["longitude"].max()

    lat_bins = pd.interval_range(start=min_lat, end=max_lat + GRID_SIZE, freq=GRID_SIZE)
    lon_bins = pd.interval_range(start=min_lon, end=max_lon + GRID_SIZE, freq=GRID_SIZE)

    rec_df["lat_bin"] = pd.cut(rec_df["latitude"], bins=lat_bins)
    rec_df["lon_bin"] = pd.cut(rec_df["longitude"], bins=lon_bins)

    return rec_df


def calc_richness(rec_df: pd.DataFrame) -> pd.DataFrame:
    """
    Groups data by map grid and calculates species richness normalized by observation count, with a minimum observation filter to exclude sparse cells.

    Args:
        rec_df: List of records as dataframe.

    Returns:
        richness: Species richness calculations as dataframe, sorted by richness rank.
    """

    richness = rec_df.groupby(["lat_bin", "lon_bin"]).agg(
        species_count=("species", "nunique"),
        observation_count=("species", "count")
    ).reset_index()

    richness["normalized_richness"] = richness["species_count"] / richness["observation_count"]

    # Only rank cells with >= 50 observations
    rankable = richness[richness["observation_count"] >= 50].sort_values(
        ["normalized_richness", "species_count"], ascending=[False, False]
    ).assign(richness_rank=range(1, len(richness[richness["observation_count"] >= 50]) + 1))

    richness = richness.merge(rankable[["lat_bin", "lon_bin", "richness_rank"]], on=["lat_bin", "lon_bin"], how="left")

    logging.info(f"Species richness calculated for {len(richness)} grid cells")
    return richness.sort_values("richness_rank")


def save_species_richness(richness: pd.DataFrame, output_file: str) -> None:
    """
    Saves species richness dataframe as a csv file.

    Args:
        richness: Species richness calculations as dataframe.
        output_file: Name of the output csv file.

    Returns:
        None: This function does not return a value; it writes output to disk.
    """

    richness.to_csv(output_file)
