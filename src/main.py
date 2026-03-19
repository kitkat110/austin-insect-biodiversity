import logging
import argparse
import socket

from get_observations import retrieve_insect_records, save_records
from calc_species_richness import create_grid


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
    insect_recs = retrieve_insect_records(25)

    logging.info("Writing records to csv file")
    records_df = save_records(insect_recs, "insect_records.csv")

    logging.info("Generating map grid")
    create_grid(records_df)


if __name__ == "__main__":
    main()