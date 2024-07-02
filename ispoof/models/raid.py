from datetime import datetime
from ispoof.spoofer.location import Location
from sqlalchemy import Column, String, Integer, Boolean, DateTime, PrimaryKeyConstraint
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Raid(Base):
    __tablename__ = "raid"

    name = Column(String(30))
    number = Column(Integer)
    location = Column(Location)
    level = Column(Integer)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    country = Column(String(2))
    PrimaryKeyConstraint(name, location, start_time, end_time, name="raid_pk", sqlite_on_conflict='IGNORE')

    def __init__(self, name, number, level, location, start_time, end_time, country):
        super().__init__()
        self.name = name
        self.number = number
        self.level = level
        self.location = location
        self.start_time = start_time
        self.end_time = end_time
        self.country = country

    def is_dispawned(self) -> bool:
        if datetime().now() > self.end_time:
            return True
        return False

    def __repr__(self) -> str:
        return f"(Raid: {self.name} - {self.level}-star - {self.location} - Start: {self.start_time} - End: {self.end_time})"
        