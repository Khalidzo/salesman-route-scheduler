import googlemaps
from dotenv import load_dotenv
import os

load_dotenv()

gmaps = googlemaps.Client(key=os.getenv("GOOGLE_MAPS_API_KEY"))
GOOGLE_MAPS_BASE_URL = "https://www.google.com/maps/dir/?api=1&"
HOME_ADDRESS = os.getenv("HOME_ADDRESS")


def validate_key(key: str) -> bool:
    """
    Validates the key provided by the user to generate the visiting plan.
    """
    return key == os.getenv("SECRET_KEY")
