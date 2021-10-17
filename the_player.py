from datetime import datetime
from the_pet import Pet
from the_egg import Egg


# Represents the player
class Player:

    def __init__(self, player_id, pets=dict(), max_pets=3, eggs=dict(), max_eggs=3, xp=0):
        self.player_id = player_id
        self.pets = pets
        self.max_pets = max_pets
        self.eggs = eggs
        self.max_eggs = max_eggs
        self.xp = xp

    # Add pet to the player's pets
    def add_pet(self, new_pet):
        self.pets[new_pet.name] = new_pet

    # Add egg to the player's eggs
    def add_egg(self, new_egg):
        self.eggs[new_egg.egg_id] = new_egg

    # Removes the pet from the player
    def remove_pet(self, pet_name):
        now = datetime.now()
        age = now - self.pets[pet_name].birthday
        self.xp += age.days
        self.update()
        del self.pets[pet_name]
        self.update()

    # Removes the egg from the player
    def remove_egg(self, egg_id):
        del self.eggs[egg_id]

    # Update based on current xp (called after a pet is removed)
    def update(self):
        if self.xp >= 3:
            self.max_pets = 4
        if self.xp >= 6:
            self.max_eggs = 4
        if self.xp >= 12:
            self.max_pets = 5
        if self.xp >= 20:
            self.max_eggs = 5
