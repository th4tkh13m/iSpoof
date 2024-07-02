from ispoof.objects.raid import Raid
from ispoof.spoofer.location import Location
from thefuzz.fuzz import partial_ratio
from sqlalchemy.orm import Session
from sqlalchemy.engine import Engine
from typing import List
from sqlalchemy import desc
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class RaidList:
    def __init__(self, engine: Engine):
        self.engine = engine
        self.timedelta = timedelta(minutes=2)

    def sort_by_name(self, reverse: bool = False) -> List[Raid]:
        with Session(self.engine) as session:
            if reverse:
                result = session.query(Raid).where(Raid.end_time > datetime.now() + self.timedelta) \
                    .order_by(desc(Raid.name))
            else:
                result = session.query(Raid).where(Raid.end_time > datetime.now() + self.timedelta) \
                    .order_by(Raid.name)
            session.commit()
            session.close()
        return result.all()

    def sort_by_level(self, reverse: bool = False) -> List[Raid]:
        with Session(self.engine) as session:
            if reverse:
                result = session.query(Raid).where(Raid.end_time > datetime.now() + self.timedelta) \
                    .order_by(desc(Raid.level))
            else:
                result = session.query(Raid).where(Raid.end_time > datetime.now() + self.timedelta) \
                    .order_by(Raid.level)
            session.commit()
            session.close()
        return result.all()

    def sort_by_distance(self, location: Location, reverse: bool = False) -> List[Raid]:
        with Session(self.engine) as session:
            result = session.query(Raid).where(Raid.end_time > datetime.now() + self.timedelta)
            session.commit()
            session.close()
        return sorted(result.all(), key=lambda raid: location.distance(raid.location), reverse=reverse)

    def search_by_name(self, query: str) -> List[Raid]:
        with Session(self.engine) as session:
            result = session.query(Raid).where(Raid.end_time > datetime.now() + self.timedelta)
            session.commit()
            session.close()
        return list(filter(lambda raid: partial_ratio(query.lower(), raid.name) >= 80, result.all()))

    def insert_to_database(self, raids: List[Raid]) -> None:
        logger.info("Insert RAIDS to Database.")
        with Session(self.engine) as session:
            session.add_all(raids)
            session.commit()
            session.close()

