from geopy.geocoders import Nominatim
from ispoof.spoofer.location import Location
from ispoof.spoofer.device import Device
from ispoof.lists.playerhistory import PlayerHistory
from datetime import datetime, timedelta
from typing import Tuple, Optional
from pathlib import Path
from math import ceil
import gpxpy
import time

TIME = 1


class Player:

    def __init__(self, engine, speed=1.4, location=None, cooldown=0):
        self.location = location
        self.cooldown = cooldown
        self.speed = speed
        self.history = PlayerHistory(engine=engine)
        self.device = Device()

    def prepare_device(self) -> None:
        self.device.mount_image()

    def set_location_with_query(self, query: str) -> None:
        loc = Nominatim(user_agent="GetLoc")
        get_loc = loc.geocode(query)

        self.location = Location(get_loc.latitude, get_loc.longitude)
        self.device.spoof_gps(self.location)

    def get_last_activity(self) -> Optional[Tuple[datetime, Location]]:
        return self.history.get_last_activity()

    def set_location(self, location: Location) -> None:
        self.location = location
        self.device.spoof_gps(self.location)

    def do_activity(self, location: Location) -> None:
        self.history.add_activity(location)

    def get_location(self) -> Location:
        return self.location

    def distance_to(self, other: Location) -> float:
        return self.location.distance(other)

    def get_cooldown(self, location: Location) -> int:
        _time, history_location = self.get_last_activity()
        if time and history_location:
            cooldown = history_location.get_cooldown(location)
            current_cooldown = ceil((_time + timedelta(minutes=cooldown) - datetime.now()).total_seconds() / 60)
            if current_cooldown < 0:
                current_cooldown = 0
        else:
            current_cooldown = 0
        return current_cooldown

    def get_current_cooldown(self) -> int:
        self.cooldown = self.get_cooldown(self.location)
        return self.cooldown

    def change_gps_by_query(self, query: str, do_activity: bool = False) -> None:
        self.set_location_with_query(query)
        if do_activity:
            self.do_activity(self.location)

    def change_gps_by_location(self, location: Location, do_activity: bool = False) -> None:
        self.set_location(location)
        if do_activity:
            self.do_activity(self.location)

    def set_last_location(self) -> None:
        _, location = self.get_last_activity()
        self.set_location(location)

    def set_speed(self, speed: float) -> None:
        self.speed = speed

    def gpx_walking(self, gpx_file: Path) -> None:
        with open(gpx_file) as f:
            gpx = gpxpy.parse(f)
        gpx_points = []
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    gpx_points.append(Location(point.latitude, point.longitude))
        num_location_points = len(gpx_points)
        point_lst = []
        for i in range(num_location_points - 1):
            start = gpx_points[i]
            end = gpx_points[i+1]
            distance = start.calculate_distance(end)
            _time = distance / self.speed
            num_points = int((distance * 1000) / self.speed) + 1
            intermediate_points = start.generate_intermediate_points(end, num_points)
            point_lst = point_lst + intermediate_points
        for point in point_lst:
            self.set_location(point)
            time.sleep(TIME)




