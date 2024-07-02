from ispoof.spoofer.location import Location
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, DateTime, PrimaryKeyConstraint
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Tuple, Optional

Base = declarative_base()


class PlayerHistory(Base):
    __tablename__ = "player_history"

    time = Column(DateTime)
    location = Column(Location)
    PrimaryKeyConstraint(time, name="history_pk")

    def __init__(self, engine=None):
        self.engine = engine

    def get_last_activity(self) -> Optional[Tuple[datetime, Location]]:
        time, location = None, None
        with Session(self.engine) as session:
            result = session.query(PlayerHistory).order_by(PlayerHistory.time.desc()).first()
            if result:
                time, location = result.time, result.location
            session.commit()
            session.close()

        return time, location

    def add_activity(self, location: Location) -> None:
        with Session(self.engine) as session:
            self.time = datetime.now()
            self.location = location
            session.add(self)
            session.commit()
            session.close()
