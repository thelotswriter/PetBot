import db_manager
from the_player import Player
from the_pet import Pet
from the_egg import Egg

players = dict()


# Adds player to the players dict
def add_player(player):
    players[player.player_id] = player


# Adds the pet to the player
def add_pet_to_player(player_id, pet):
    players[player_id].add_pet(pet)


# Adds the egg to the player
def add_egg_to_player(player_id, egg):
    players[player_id].add_egg(egg)


# Gets the player with the given id
def get_player(player_id):
    return players[player_id]


# Removes the pet
def remove_pet(pet):
    connection = db_manager.create_connection()
    db_manager.remove_pet(connection, pet)
    players[pet.player_id].remove_pet(pet.name)
    db_manager.update_player(connection, players[pet.player_id])


# Removes the egg
def remove_egg(egg):
    players[egg.player_id].remove_egg(egg.egg_id)


# Returns a boolean whether the player has been added to petbot
def has_player(player_id):
    return player_id in players.keys()


# Checks if the player is able to add a pet
def can_add_pet(player_id):
    if player_id in players.keys():
        player = players[player_id]
        return player.max_pets > len(player.pets)
    else:
        return True


# Checks if the player has the given pet
def has_pet(player_id, name):
    if player_id in players.keys():
        for pet in players[player_id].pets:
            if pet == name:
                return True
    return False
