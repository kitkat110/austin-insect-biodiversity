import pyinaturalist as pin
import pandas as pd

records = []

for page in range(1, 26):
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

df = pd.DataFrame(records)
df = df.dropna()

df.to_csv('insect_records.csv')
