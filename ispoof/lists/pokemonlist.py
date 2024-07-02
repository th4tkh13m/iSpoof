from ispoof.objects.pokemon import Pokemon
from ispoof.spoofer.location import Location
from thefuzz.fuzz import partial_ratio
from sqlalchemy.orm import Session
from sqlalchemy.engine import Engine
from typing import List
from sqlalchemy import desc
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class PokemonList:
    def __init__(self, engine: Engine):
        self.engine = engine
        self.timedelta = timedelta(minutes=2)
    
    def sort_by_name(self, reverse: bool = False) -> List[Pokemon]:
        with Session(self.engine) as session:
            if reverse:
                result = session.query(Pokemon).where(Pokemon.visited.is_(False), Pokemon.end_time > datetime.now() + self.timedelta)\
                        .order_by(desc(Pokemon.name))
            else:
                result = session.query(Pokemon).where(Pokemon.visited.is_(False), Pokemon.end_time > datetime.now() + self.timedelta)\
                        .order_by(Pokemon.name)
            session.commit()
            session.close()
        return result.all()

    def sort_by_cp(self, reverse: bool = False) -> List[Pokemon]:
        with Session(self.engine) as session:
            if reverse:
                result = session.query(Pokemon).where(Pokemon.visited.is_(False), Pokemon.end_time > datetime.now() + self.timedelta) \
                    .order_by(desc(Pokemon.cp))
            else:
                result = session.query(Pokemon).where(Pokemon.visited.is_(False), Pokemon.end_time > datetime.now() + self.timedelta) \
                    .order_by(Pokemon.cp)
            session.commit()
            session.close()
        return result.all()

    def sort_by_level(self, reverse: bool = False) -> List[Pokemon]:
        with Session(self.engine) as session:
            if reverse:
                result = session.query(Pokemon).where(Pokemon.visited.is_(False), Pokemon.end_time > datetime.now() + self.timedelta) \
                    .order_by(desc(Pokemon.level))
            else:
                result = session.query(Pokemon).where(Pokemon.visited.is_(False), Pokemon.end_time > datetime.now() + self.timedelta) \
                    .order_by(Pokemon.level)
            session.commit()
            session.close()
        return result.all()

    def sort_by_distance(self, location: Location, reverse: bool = False) -> List[Pokemon]:
        with Session(self.engine) as session:
            result = session.query(Pokemon).where(Pokemon.visited.is_(False), Pokemon.end_time > datetime.now() + self.timedelta)
            session.commit()
            session.close()
        return sorted(result.all(), key=lambda pokemon: location.distance(pokemon.location), reverse=reverse)

    def search_by_name(self, query: str) -> List[Pokemon]:
        with Session(self.engine) as session:
            result = session.query(Pokemon).where(Pokemon.visited.is_(False), Pokemon.end_time > datetime.now() + self.timedelta)
            session.commit()
            session.close()
        return list(filter(lambda pokemon: partial_ratio(query.lower(), pokemon.name) >= 80, result.all()))

    def insert_to_database(self, pokemons: List[Pokemon]) -> None:
        logger.info("Add pokemons to database.")
        with Session(self.engine) as session:
            session.add_all(pokemons)
            session.commit()
            session.close()

    def visit_pokemon(self, pokemon: Pokemon) -> None:
        with Session(self.engine) as session:
            new_pokemon = session.query(Pokemon).where(Pokemon.name == pokemon.name,
                                                       Pokemon.location == pokemon.location,
                                                       Pokemon.start_time == pokemon.start_time,
                                                       Pokemon.end_time == pokemon.end_time).one()
            new_pokemon.visited = True
            session.commit()
            session.close()


