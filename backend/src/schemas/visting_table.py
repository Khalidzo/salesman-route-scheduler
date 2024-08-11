from pydantic import BaseModel


class GeoLocation(BaseModel):
    latitude: float
    longitude: float


class VistingTableEntry(BaseModel):
    name: str
    address: str
    location: GeoLocation
    google_place_id: str
