from typing import NamedTuple, Optional

import googlemaps
from constance import config
from django.contrib.gis.geos import Point


class GeoCodedAddress(NamedTuple):
    address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    pin_code: Optional[str]
    lat: Optional[float]
    lng: Optional[float]
    location: Optional[Point]
    country: Optional[str]


class GeoCode:
    def __init__(self, coordinated):
        self.coordinated = coordinated

    def reverse_geocode(self):
        gmaps = googlemaps.Client(key=config.GOOGLE_MAPS_API_KEY)
        geocode_results = gmaps.reverse_geocode(self.coordinated)

        formatted_address = ""
        for result in geocode_results:
            address = result.get("formatted_address", "")
            if (
                address.__len__() > formatted_address.__len__()
                and not "Unnamed" in address
                and not "+" in address
            ):
                formatted_address = address

        if len(geocode_results) > 0:
            geocode_result = geocode_results[0]
        if len(geocode_result) == 0:
            return None
        if "country" in geocode_result["types"] or (
            "partial_match" in geocode_result and geocode_result["partial_match"]
        ):
            return None
        address_components = geocode_result["address_components"]
        country = None
        pin_code = None
        state = None
        city = None
        lat = None
        lng = None
        location = None

        # We iterate the address_components to find the specific items that matches required type.
        for item in address_components:
            if "country" in item["types"]:
                country = item["long_name"]
            if "postal_code" in item["types"]:
                pin_code = item["long_name"]
            if "administrative_area_level_1" in item["types"]:
                state = item["long_name"]
            if "administrative_area_level_2" in item["types"]:
                city = item["long_name"]

        lat = geocode_result["geometry"]["location"]["lat"]
        lng = geocode_result["geometry"]["location"]["lng"]

        location = Point(x=lng, y=lat)

        return GeoCodedAddress(
            address=formatted_address,
            city=city,
            state=state,
            pin_code=pin_code,
            lat=lat,
            lng=lng,
            location=location,
            country=country,
        )
