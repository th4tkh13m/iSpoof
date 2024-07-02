from __future__ import annotations
from math import radians, sin, cos, asin, sqrt, atan2, degrees
from sqlalchemy.types import TypeDecorator, String
from typing import List
from geographiclib.geodesic import Geodesic


class Location(TypeDecorator):
    impl = String
    cache_ok = True

    def __init__(self, latitude: float = None, longitude: float = None):
        self.latitude = latitude
        self.longitude = longitude

    def get_tuple(self):
        return self.latitude, self.longitude

    def process_bind_param(self, value, dialect):
        if value:
            return str(value)

    def process_result_value(self, value, dialect):
        if value:
            return Location(* map(float, value.split(",")))

    def load_dialect_impl(self, dialect):
        # Provide the implementation for the specified dialect
        return dialect.type_descriptor(String)

    def calculate_distance(self, other: Location):
        return Geodesic.WGS84.Inverse(*self.get_tuple(), *other.get_tuple())["s12"] / 1000

    def generate_intermediate_points(self, other: Location, num_points) -> List[Location]:
        # Calculate the distance between the start and end points
        _distance = self.calculate_distance(other) * 1000
        spacing = _distance / (num_points + 1)

        # Calculate the intermediate points along the geodesic line
        points = []
        for i in range(1, num_points + 1):
            # Calculate the position of the i-th intermediate point
            d = i * spacing
            g = Geodesic.WGS84.InverseLine(*self.get_tuple(), *other.get_tuple()).Position(d)
            lat, lon = g['lat2'], g['lon2']
            points.append(Location(lat, lon))

        return points
    
    def get_cooldown(self, other):
        _distance = self.calculate_distance(other)

        if _distance <= 2:
            return 1
        elif _distance <= 5:
            return 2
        elif _distance <= 7:
            return 5
        elif _distance <= 10:
            return 7
        elif _distance <= 12:
            return 8
        elif _distance <= 18:
            return 10
        elif _distance <= 26:
            return 15
        elif _distance <= 42:
            return 19
        elif _distance <= 65:
            return 22
        elif _distance <= 81:
            return 25
        elif _distance <= 100:
            return 35
        elif _distance <= 220:
            return 40
        elif _distance <= 250:
            return 45
        elif _distance <= 350:
            return 51
        elif _distance <= 375:
            return 54
        elif _distance <= 460:
            return 62
        elif _distance <= 500:
            return 65
        elif _distance <= 565:
            return 69
        elif _distance <= 700:
            return 78
        elif _distance <= 800:
            return 84
        elif _distance <= 900:
            return 92
        elif _distance <= 1000:
            return 99
        elif _distance <= 1100:
            return 107
        elif _distance <= 1200:
            return 114
        elif _distance <= 1300:
            return 117
        else:
            return 120

    def __str__(self):
        return str(self.latitude) + "," + str(self.longitude)

    def __repr__(self):
        return str(self.latitude) + "," + str(self.longitude)

    def __eq__(self, other):
        if isinstance(other, Location):
            return (self.latitude == other.latitude and
                    self.longitude == other.longitude)
        return False

    def __hash__(self):
        return hash(self.get_tuple())

        