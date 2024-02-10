import re
import pandas as pd
import os
import logging

import autocomplete_cities.data.schemas as schemas


def get_cities() -> dict[str, schemas.City]:
    only_letters_regex = re.compile("[^a-zA-Z]")

    cities = {}

    dir_path = os.path.dirname(os.path.realpath(__file__))
    datafile = os.path.join(dir_path, "./cities_canada-usa.tsv")

    cities_df = pd.read_csv(datafile, sep="\t", header=0)
    for _, row in cities_df.iterrows():
        population = row["population"]
        if population < 5000:
            logging.info(f"city {row['id']}'s population is too small")
            continue

        name_raw = row["ascii"]
        name = only_letters_regex.sub("", name_raw).lower()

        country = row["country"]
        region = row["admin1"]
        if country == "CA":
            region = f"Province {region}"

        city = schemas.City(
            id=row["id"],
            name=name,
            name_raw=name_raw,
            latitude=row["lat"],
            longitude=row["long"],
            country=row["country"],
            region=region
        )
        cities[row["id"]] = city

    return cities
