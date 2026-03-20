import logging
import argparse
import socket

from get_observations import retrieve_insect_records, save_records
from calc_species_richness import create_grid, calc_richness, save_species_richness


# -------------------------
# Logging setup
# -------------------------
log_parser = argparse.ArgumentParser()
log_parser.add_argument(
    '-l', '--loglevel',
    type=str,
    required=False,
    default='INFO',
    help='set log level to DEBUG, INFO, WARNING, ERROR, or CRITICAL'
)
args = log_parser.parse_args()

format_str = (
    f'[%(asctime)s {socket.gethostname()}] '
    '%(filename)s:%(funcName)s:%(lineno)s - %(levelname)s: %(message)s'
)
logging.basicConfig(level=args.loglevel, format=format_str)


# -------------------------
# Pipeline
# -------------------------
def main():
    logging.info("Retrieving records from iNaturalist")
    insect_recs = retrieve_insect_records()

    logging.info("Writing records to csv file")
    records_df = save_records(insect_recs, "insect_records.csv")

    logging.info("Generating map grid")
    records_df = create_grid(records_df)

    logging.info("Calculating species richness by grid")
    species_richness = calc_richness(records_df)

    logging.info("Writing species richness calculations to csv file")
    save_species_richness(species_richness, "species_richness.csv")


if __name__ == "__main__":
    main()