from ispoof.objects import Pokemon, Raid
from ispoof.lists.playerhistory import PlayerHistory
from sqlalchemy.exc import ArgumentError
from sqlalchemy import create_engine
from ispoof.utils import get_home_folder
import logging
from sqlalchemy.engine import Engine

logger = logging.getLogger(__name__)


class Database:
    def __init__(self):
        self.data = get_home_folder() / "data"
        self.data.mkdir(parents=True, exist_ok=True)
        self.engine = create_engine(f"sqlite:///{(self.data / 'data.db').absolute()}")

    def initialize_database(self) -> bool:
        logger.info("Creating databases.")
        try:
            Pokemon.metadata.create_all(self.engine)
            Raid.metadata.create_all(self.engine)
            PlayerHistory.metadata.create_all(self.engine)
        except ArgumentError:
            logger.info("Databases existed.")
        finally:
            return True

    def get_engine(self) -> Engine:
        return self.engine
