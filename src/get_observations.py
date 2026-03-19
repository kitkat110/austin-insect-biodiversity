import logging
import pyinaturalist as pin # pyright: ignore[reportMissingImports]
import pandas as pd # pyright: ignore[reportMissingModuleSource]

records = []

# -------------------------
# Functions
# -------------------------
def retrieve_insect_records(pages: int) -> list:
    """
    Searches the iNaturalist database for Insecta entries in Austin and retrieves their coordinates.

    Args:
        pages: Number of pages of iNaturalist to search.

    Returns:
        records: List of matching records with coordinates.
    """

    for page in range(1, pages+1):
        obs = pin.get_observations(
            lat=30.2895,    # UT Austin area
            lng=-97.7368,
            radius=10,
            taxon_name = "Insecta",
            per_page = 200,
            page=page,
            verifiable=True
        )

        for o in obs["results"]:
            if o.get("geojson") and o.get("taxon"):
                records.append({
                    "id": o.get("id"),
                    "class": o["taxon"].get("species_guess", o["taxon"]["name"]),
                    "latitude": o["geojson"]["coordinates"][1],
                    "longitude": o["geojson"]["coordinates"][0]
                })
    
    if len(records) == 0:
        logging.warning("Unable to retrieve any records")
    else:
        logging.info(f"{len(records)} total records retrieved")
        return records

def save_records(recs: list, output_file: str) -> pd.DataFrame:
    """
    Converts records list to pandas dataframe and saves it as csv file.

    Args:
        recs: List of matching records with coordinates. 
        output_file: Name of the output csv file.

    Returns:
        rec_df: List of records as a dataframe.
    """

    rec_df = pd.DataFrame(recs)
    rec_df = rec_df.dropna()

    rec_df.to_csv(output_file)

    return rec_df
