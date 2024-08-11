import googlemaps
from dotenv import load_dotenv
import os

load_dotenv()

gmaps = googlemaps.Client(key=os.getenv("GOOGLE_MAPS_API_KEY"))

def validate_key(key: str) -> bool:
    """
    Validates the key provided by the user to generate the visiting plan.
    """
    return key == os.getenv("SECRET_KEY")