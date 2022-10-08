# Read, parse airports.csv from https://github.com/davidmegginson/ourairports-data

import csv
import sys

rows = 0
with open(sys.argv[1], newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    next(reader)  # Skip headers
    # Headers:
    # "id","ident","type","name","latitude_deg","longitude_deg","elevation_ft","continent","iso_country","iso_region","municipality","scheduled_service","gps_code","iata_code","local_code","home_link","wikipedia_link","keywords"
    for row in reader:
        (a_id, ident, a_type, name, lat_deg, lon_deg, elevation, continent, iso_country, iso_region, municipality,
         scheduled_service, gps_code, iata_code, local_code, home_link, wiki_link, keywords) = row
        name = name.replace("'", "''")
        municipality = municipality.replace("'", "''")

        if a_type != "closed":
            print(
                f"INSERT INTO airport (name, type, latitude_deg, longitude_deg, continent, iso_country, municipality, gps_code, iata_code)"
                f" VALUES('{name}','{a_type}','{lat_deg}','{lon_deg}','{continent}','{iso_country}','{municipality}','{gps_code}','{iata_code}');")
        rows += 1
