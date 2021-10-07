from the_pet import Pet
from the_egg import Egg
import datetime

player_pets = dict()
pets = []


def add_pet(owner, name, dna):
    new_pet = Pet(owner, name=name, birthday=datetime.datetime.now(), dna=dna)
    if owner not in player_pets:
        player_pets[owner] = dict()
    player_pets[owner][name] = new_pet
    pets.append(new_pet)


def hatch_pet(owner, name, egg):
    new_pet = Pet(owner, name=name, birthday=datetime.datetime.now(), max_food=egg.max_food, base_food=egg.max_food, hunger_rate=egg.hunger_rate,
                  base_hunger_rate=egg.hunger_rate,  max_happiness=egg.max_happiness, base_happiness=egg.max_happiness,
                  sadness_rate=egg.sadness_rate, base_sadness_rate=egg.sadness_rate, max_clean=egg.max_cleanliness,
                  base_clean=egg.max_cleanliness, dirt_rate=egg.dirt_rate, base_dirt_rate=egg.dirt_rate,
                  immunity=egg.immunity, base_immunity=egg.immunity, max_sleepiness=egg.max_sleepiness,
                  base_sleepiness=egg.max_sleepiness, sleepiness_rate=egg.sleepiness_rate,
                  base_sleepiness_rate=egg.sleepiness_rate, sleepiness_recovery_rate=egg.sleepiness_recovery_rate,
                  base_sleepiness_recovery_rate=egg.sleepiness_recovery_rate, dna=egg.dna)
    if owner not in player_pets:
        player_pets[owner] = dict()
    player_pets[owner][name] = new_pet
    pets.append(new_pet)


async def update_pets(context=None):
    deceased_pets = []
    for a_pet in pets:
        a_pet.update(context)
        if not a_pet.alive:
            deceased_pets.append(a_pet)
            context = a_pet.context
    for passed_pet in deceased_pets:
        del player_pets[passed_pet.player_id][passed_pet.name]
        if len(player_pets[passed_pet.player_id]) <= 0:
            del player_pets[passed_pet.player_id]
        p = 0
        for p in range(len(pets)):
            if pets[p].player_id == passed_pet.player_id and pets[p].name == passed_pet.name:
                del pets[p]
                break
    if len(deceased_pets) > 1:
        await context.send(f'Unfortunately, {len(deceased_pets)} pets have passed away.')
    elif len(deceased_pets) > 0:
        await context.send(f'{deceased_pets[0].name} has passed away.')
    return deceased_pets

