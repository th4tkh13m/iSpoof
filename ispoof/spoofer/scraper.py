from bs4 import BeautifulSoup
import requests
from ispoof.objects.pokemon import Pokemon
from ispoof.objects.raid import Raid
from ispoof.spoofer.location import Location
from datetime import datetime


class Scraper():
    def __init__(self):
        self.HUNDO_URL = "https://moonani.com/PokeList/index.php"
        self.PVP_URL = "https://moonani.com/PokeList/pvp.php"
        
    def get_pokemons(self, url):
        pokemon_lst = []
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "lxml")

        for row in soup.find_all("tr")[1:]:
            data = row.find_all("td")[1:]

            name = data[0].text.strip().strip("*")
            number = int(data[1].text)

            coordinates = map(float, data[2].text.split(","))
            location = Location(*coordinates)

            cp = int(data[3].text)
            level = int(data[4].text)
            attack = int(data[5].text)
            defense = int(data[6].text)
            hp = int(data[7].text)
            iv = int(data[8].text.rstrip("%"))
            shiny = data[9].text == "Yes"
            start_time = datetime.fromisoformat(data[10].text)
            end_time = datetime.fromisoformat(data[11].text)
            country = data[12].text.strip()

            pokemon = Pokemon(name=name, number=number, location=location, cp=cp, level=level, attack=attack,
                              defense=defense, hp=hp, iv=iv, shiny=shiny, start_time=start_time, end_time=end_time,
                              country=country)
            pokemon_lst.append(pokemon)
        
        return pokemon_lst

    def get_hundos(self):
        return self.get_pokemons(self.HUNDO_URL)
    
    def get_pvp(self):
        return self.get_pokemons(self.PVP_URL)

    def get_raids(self):
        raid_lst = []
        response = requests.get("https://moonani.com/PokeList/raid.php")
        soup = BeautifulSoup(response.text, "lxml")

        for row in soup.find_all("tr")[1:]:
            data = row.find_all("td")

            name = data[0].text
            number = int(data[1].text)
            level = int(data[2].text)

            coordinates = map(float, data[3].text.split(","))
            location = Location(*coordinates)

            start_time = datetime.fromisoformat(data[4].text)
            end_time = datetime.fromisoformat(data[5].text)
            country = data[6].text

            raid = Raid(name, number, level, location, start_time, end_time, country)
            raid_lst.append(raid)
        
        return raid_lst



