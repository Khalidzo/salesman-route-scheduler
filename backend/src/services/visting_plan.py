from typing import Tuple
import re
import requests
import pandas as pd
from core.config import gmaps
from schemas.visting_table import GeoLocation


def validate_visting_table(visiting_table_df: pd.DataFrame) -> bool:
    # Check if the visiting table has the required columns
    required_columns = ["Location"]
    if not all(column in visiting_table_df.columns for column in required_columns):
        return False

    # Check if the visiting table has at least one row
    if visiting_table_df.shape[0] == 0:
        return False

    return True


def extract_coordinates_and_name(url: str) -> Tuple[GeoLocation, str]:
    """
    Extracts the latitude, longitude, and place name from a Google Maps URL.
    Example for a url: https://goo.gl/maps/Yqi5rgM1WG6zpZaPA
    The function will return the latitude, longitude, and place name.
    """
    response = requests.get(url)
    resolved_url = response.url

    # Use regex to find the latitude, longitude, and place name in the resolved URL
    match_coords = re.search(r"@(-?\d+\.\d+),(-?\d+\.\d+)", resolved_url)
    match_name = re.search(r"/place/([^/]+)", resolved_url)

    if match_coords and match_name:
        lat, lng = match_coords.groups()
        name = match_name.group(1).replace("+", " ")
        location = GeoLocation(latitude=lat, longitude=lng)
        return location, name
    else:
        return GeoLocation(latitude=None, longitude=None), None


def find_place_by_name(place_name: str, location: GeoLocation, radius=100):
    # Use the textsearch API to find the place by name near the given location
    search_result = gmaps.places(
        query=place_name,
        location=(location.latitude, location.longitude),
        radius=radius,
    )

    if search_result["results"]:
        # Return the first result
        return search_result["results"][0]
    else:
        return None


def create_visiting_table(visiting_table_df: pd.DataFrame) -> pd.DataFrame:
    visiting_table_data = []

    for i, row in visiting_table_df.iterrows():
        if i < 4:
            # Extract coordinates and place name from the Google Maps link
            google_maps_link = row["Location"]
            geolocation, place_name = extract_coordinates_and_name(google_maps_link)

            # Find the place details using the extracted coordinates and name
            place = find_place_by_name(place_name, geolocation)
            pharmacy_address = place.get("formatted_address", "N/A")
            pharmacy_name = place.get("name", "N/A")
            google_place_id = place.get("place_id", "N/A")
            pharmacy_code = row[visiting_table_df.columns[0]]

            # Create a dictionary with the entry's values
            visiting_list_entry = {
                "name": pharmacy_name,
                "address": pharmacy_address,
                "latitude": geolocation.latitude,
                "longitude": geolocation.longitude,
                "google_place_id": google_place_id,
                "pharmacy_code": pharmacy_code,
            }

            # Add the dictionary to the list
            visiting_table_data.append(visiting_list_entry)
        else:
            break

    # Convert the list of dictionaries into a DataFrame
    visiting_table_df_result = pd.DataFrame(visiting_table_data)

    return visiting_table_df_result


def filter_visting_table(visiting_table_df: pd.DataFrame) -> pd.DataFrame:
    filtered_df = visiting_table_df[
        (
            visiting_table_df["Location"].str.startswith("https://goo.gl/maps/")
            | visiting_table_df["Location"].str.startswith("https://maps.app.goo.gl/")
        )
        & visiting_table_df["Location"].notna()
    ]

    # Drop rows with duplicate locations
    filtered_df = filtered_df.drop_duplicates(subset=["Location"], keep="first")

    return filtered_df
