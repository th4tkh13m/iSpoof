from ispoof.objects.player import Player
from ispoof.spoofer.scraper import Scraper
from ispoof.spoofer.device import Device
from ispoof.lists import PokemonList, RaidList
from pathlib import Path
from ispoof.data import Database

if __name__ == "__main__":
    database = Database()
    database.initialize_database()
    engine = database.get_engine()
    player = Player(engine=engine)
    player.prepare_device()
    print("Choose Location")
    print("1. Last location")
    print("2. Provided location")
    while True:
        location_input = int(input("Choose: "))
        if location_input in (1, 2):
            break
    if location_input == 1:
        player.set_last_location()
    else:
        query = input("Enter your location: ")
        player.set_location_with_query(query)

    scraper = Scraper()
    pokemon_lst = PokemonList(engine=engine)
    raid_lst = RaidList(engine=engine)
    # while True:
    #     print("1. Raid")
    #     print("2. Pokemon")
    #     print("3. GPX file")
    #     raid_or_mon = int(input("Choose 1: "))
    #     if raid_or_mon == 1:
    #         raids = scraper.get_raids()
    #         raid_lst.insert_to_database(raids)
    #         print("1. Sort by name")
    #         print("2. Sort by level")
    #         print("3. Sort by distance")
    #         print("4. Search name")
    #         choice = int(input("Your choice: "))
    #         if choice == 1:
    #             raids = raid_lst.sort_by_name()
    #         elif choice == 2:
    #             raids = raid_lst.sort_by_level()
    #         elif choice == 3:
    #             raids = raid_lst.sort_by_distance(player.location)
    #         else:
    #             raids = raid_lst.search_by_name(input("Enter query: "))
    #         print("Raid List:")
    #         for i, raid in enumerate(raids):
    #             print(i, raid)
    #         i = int(input("Choose raid: "))
    #         pokemon = raids[i]
    #         location = raid.location
    #     else:
    #         pokemons = scraper.get_hundos()
    #         pokemon_lst.insert_to_database(pokemons)
    #         print("1. Sort by name")
    #         print("2. Sort by level")
    #         print("3. Sort by CP")
    #         print("4. Sort by distance")
    #         print("5. Search name")
    #         choice = int(input("Your choice: "))
    #         if choice == 1:
    #             pokemons = pokemon_lst.sort_by_name()
    #         elif choice == 2:
    #             pokemons = pokemon_lst.sort_by_level()
    #         elif choice == 3:
    #             pokemons = pokemon_lst.sort_by_cp()
    #         elif choice == 4:
    #             pokemons = pokemon_lst.sort_by_distance(player.location)
    #         else:
    #             pokemons = pokemon_lst.search_by_name(input("Enter query: "))
    #         print("Pokemon List:")
    #         for i, pokemon in enumerate(pokemons):
    #             print(i, pokemon)
    #         i = int(input("Choose pokemon: "))
    #         pokemon = pokemons[i]
    #         location = pokemon.location
    #         pokemon_lst.visit_pokemon(pokemon)
    #     device.spoof_gps(location)
    #     did_activity = None
    #     print("Spoof to")
    #     print(pokemon)
    #     while True:
    #         activity = input("Did you do any cooldown activities? [Y/N] ").lower()
    #         if activity in ("y", "n"):
    #             did_activity = activity == "y"
    #             break
    #     player.change_gps_by_location(location, did_activity)
    #     print(f"Current cooldown: {player.get_current_cooldown()} min")
    while True:
        player.gpx_walking(Path.home() / "Downloads/Sydney.gpx")
        while True:
            continue_prompt = input("Continue? [Y/N] ").lower()
            if continue_prompt in ("y", "n"):
                if continue_prompt == "n":
                    player.device.stop_spoofing()
                    exit(0)
                else:
                    break
