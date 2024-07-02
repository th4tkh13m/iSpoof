from datetime import datetime
from sqlalchemy import Column, String, Integer, Boolean, DateTime, PrimaryKeyConstraint
from ispoof.spoofer.location import Location
from sqlalchemy.orm import declarative_base, Session

Base = declarative_base()


class Pokemon(Base):
    __tablename__ = "pokemon"
    name = Column(String(30))
    number = Column(Integer)
    location = Column(Location)
    cp = Column(Integer)
    level = Column(Integer)
    attack = Column(Integer)
    defense = Column(Integer)
    hp = Column(Integer)
    iv = Column(Integer)
    shiny = Column(Boolean)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    country = Column(String(2))
    visited = Column(Boolean, default=False)
    PrimaryKeyConstraint(name, location, start_time, end_time, name="pokemon_pk", sqlite_on_conflict='IGNORE')

    def __init__(self, name, number, location,
                 cp, level, attack, defense, hp,
                 iv, shiny, start_time, end_time,
                 country):
        super().__init__()
        self.name = name
        self.number = number
        self.location = location
        self.cp = cp
        self.level = level
        self.attack = attack
        self.defense = defense
        self.hp = hp
        self.iv = iv
        self.shiny = shiny
        self.start_time = start_time
        self.end_time = end_time
        self.country = country

    def is_despawned(self) -> bool:
        if datetime().now() > self.end_time:
            return True
        return False

    def __repr__(self) -> str:
        return f"{self.name}: {self.cp}, {self.level}, {self.attack}-{self.defense}-{self.hp}, shinable: {self.shiny}, end: {self.end_time}"

    
    