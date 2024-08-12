import googlemaps
from dotenv import load_dotenv
import os

load_dotenv()

gmaps_key = os.getenv("GMAPS_API_KEY")
gmaps = googlemaps.Client(key=gmaps_key)

GOOGLE_MAPS_BASE_URL = "https://www.google.com/maps/dir/?api=1"
HOME_ADDRESS = os.getenv("HOME_ADDRESS")


def validate_key(key: str) -> bool:
    """
    Validates the key provided by the user to generate the visiting plan.
    """
    return key == os.getenv("SECRET_KEY")
