import logging
import sys
import time
import pyinaturalist as pin
import pandas as pd 

# -------------------------
# Functions
# -------------------------
def retrieve_insect_records(pages: int = 25) -> list:
    """
    Searches the iNaturalist database for Insecta entries in Austin and retrieves their coordinates.

    Args:
        pages: Number of pages of iNaturalist to search.

    Returns:
        records: List of matching records with coordinates.
    """

    records = []

    for page in range(1, pages+1):
        obs = pin.get_observations(
            nelat=30.7,
            nelng=-97.5,
            swlat=30.0,
            swlng=-97.9,
            taxon_id = 47158, # Insecta class taxon ID
            per_page = 200,
            page=page
        )

        if not obs["results"]:
            logging.info(f"No results on page {page}, stopping early.")
            break

        for o in obs["results"]:
            taxon = o.get("taxon")
            geo = o.get("geojson")

            if not taxon or not geo:
                continue

            if taxon.get("rank") != "species":  # Skip non-species level observations
                continue

            records.append({
                "id": o.get("id"),
                "taxon_id": taxon["id"],
                "species": taxon["name"],
                "latitude": geo["coordinates"][1],
                "longitude": geo["coordinates"][0]
            })

        time.sleep(1)  # Avoid hitting iNaturalist's rate limit
    
    if len(records) == 0:
        sys.exit("Unable to retrieve any records")
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
