import datetime
import random

from the_pet import Pet
import pet_manager
from the_egg import Egg

player_eggs = dict()
eggs = []


def add_egg(owner, parent):
    if parent.tot_mins > 0:
        egg_id = 0
        for egg in eggs:
            if egg.egg_id > egg_id:
                egg_id = egg.egg_id + 1
        max_food = parent.base_food
        hunger_rate = parent.base_hunger_rate
        max_happiness = parent.base_happiness
        sadness_rate = parent.base_sadness_rate
        max_clean = parent.base_cleanliness
        dirt_rate = parent.base_dirt_rate
        immunity = parent.base_immunity
        max_sleepiness = parent.base_sleepiness
        sleepiness_rate = parent.base_sleepiness_rate
        sleepiness_recovery_rate = parent.base_sleepiness_recovery_rate
        age = datetime.datetime.now() - parent.birthday
        for x in range(age.days + 1):
            r = random.randint(1, 10)
            if r == 1:
                food = parent.avg_food / parent.tot_mins
                if food > 0.75:
                    max_food = min(10.0, max_food * 1.1)
                elif food < 0.25:
                    max_food = max(3.0, max_food * 0.9)
            elif r == 2:
                food = parent.avg_food / parent.tot_mins
                if food > 0.75:
                    hunger_rate = max(0.5, hunger_rate * 0.9)
                elif food < 0.25:
                    hunger_rate = min(4.0, hunger_rate * 1.1)
            elif r == 3:
                happiness = parent.avg_happiness / parent.tot_mins
                if happiness > 0.75:
                    max_happiness = min(10.0, max_happiness * 1.1)
                elif happiness < 0.25:
                    max_happiness = max(3.0, max_happiness * 0.9)
            elif r == 4:
                happiness = parent.avg_happiness / parent.tot_mins
                if happiness > 0.75:
                    sadness_rate = max(0.5, sadness_rate * 0.9)
                elif happiness < 0.25:
                    sadness_rate = min(4.0, sadness_rate * 1.1)
            elif r == 5:
                clean = parent.avg_cleanliness / parent.tot_mins
                if clean > 0.75:
                    max_clean = min(10.0, max_clean * 1.1)
                elif clean < 0.25:
                    max_clean = max(3.0, max_clean * 0.9)
            elif r == 6:
                clean = parent.avg_cleanliness / parent.tot_mins
                if clean > 0.75:
                    dirt_rate = max(0.5, dirt_rate * 0.9)
                elif clean < 0.25:
                    dirt_rate = min(4.0, dirt_rate * 1.1)
            elif r == 7:
                sick = parent.avg_sick / parent.tot_mins
                if sick > 0.4:
                    immunity = max(0.1, immunity * 0.9)
                elif sick < 0.1:
                    immunity = min(0.9, immunity * 1.1)
            elif r == 8:
                sleep = parent.avg_sleepiness / parent.tot_mins
                if sleep > 0.65:
                    max_sleepiness = max(3.0, max_sleepiness * 0.9)
                elif sleep < 0.35:
                    max_sleepiness = min(10.0, max_sleepiness * 1.1)
            elif r == 9:
                sleep = parent.avg_sleepiness / parent.tot_mins
                if sleep > 0.65:
                    sleepiness_rate = min(4.0, sleepiness_rate * 1.1)
                elif sleep < 0.35:
                    sleepiness_rate = max(10.0, sleepiness_rate * 0.9)
            else:
                sleep = parent.avg_sleepiness / parent.tot_mins
                if sleep > 0.65:
                    sleepiness_recovery_rate = max(0.5, sleepiness_recovery_rate * 0.9)
                elif sleep < 0.35:
                    sleepiness_recovery_rate = min(4.0, sleepiness_recovery_rate * 1.1)
        new_egg = Egg(owner, egg_id=egg_id, max_food=max_food, hunger_rate=hunger_rate, max_happiness=max_happiness,
                      sadness_rate=sadness_rate, max_clean=max_clean, dirt_rate=dirt_rate, immunity=immunity,
                      max_sleepiness=max_sleepiness, sleepiness_rate=sleepiness_rate,
                      sleepiness_recovery_rate=sleepiness_recovery_rate, dna=parent.dna)

        if owner not in player_eggs:
            player_eggs[owner] = dict()
        player_eggs[owner][egg_id] = new_egg
        eggs.append(new_egg)
    else:
        print('Not added')

def retrieve_egg(owner, egg_id):
    if owner in player_eggs:
        egg = player_eggs[owner][egg_id]
        del player_eggs[owner][egg_id]
        if len(player_eggs[owner]) <= 0:
            del player_eggs[owner]
        eg = 0
        for eg in range(len(eggs)):
            if eggs[eg].player_id == owner and eggs[eg].egg_id == egg_id:
                del eggs[eg]
                break
        return egg
    return None

# async def update_pets(context=None):
#     deceased_pets = []
#     for a_pet in pets:
#         a_pet.update(context)
#         if not a_pet.alive:
#             deceased_pets.append(a_pet)
#             context = a_pet.context
#     for passed_pet in deceased_pets:
#         del player_pets[passed_pet.player_id][passed_pet.name]
#         if len(player_pets[passed_pet.player_id]) <= 0:
#             del player_pets[passed_pet.player_id]
#         p = 0
#         for p in range(len(pets)):
#             if pets[p].player_id == passed_pet.player_id and pets[p].name == passed_pet.name:
#                 del pets[p]
#                 break
#     if len(deceased_pets) > 1:
#         await context.send(f'Unfortunately, {len(deceased_pets)} pets have passed away.')
#     elif len(deceased_pets) > 0:
#         await context.send(f'{deceased_pets[0].name} has passed away.')
#     return deceased_pets

