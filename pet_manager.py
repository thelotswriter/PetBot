from the_player import Player
from the_pet import Pet
from the_egg import Egg
import player_manager
import db_manager
import datetime


# Adds a new pet with the given name and starting dna
def add_pet(owner, name, dna):
    new_pet = Pet(owner, name=name, birthday=datetime.datetime.now(), dna=dna)
    connection = db_manager.create_connection()
    if not player_manager.has_player(owner):
        player = Player(owner)
        db_manager.add_player(connection, player)
        player_manager.add_player(player)
    db_manager.add_pet(connection, new_pet)
    player_manager.add_pet_to_player(owner, new_pet)


# Creates a new pet from an egg
def hatch_pet(owner, name, egg):
    new_pet = Pet(owner, name=name, birthday=datetime.datetime.now(), max_food=egg.max_food, base_food=egg.max_food, hunger_rate=egg.hunger_rate,
                  base_hunger_rate=egg.hunger_rate,  max_happiness=egg.max_happiness, base_happiness=egg.max_happiness,
                  sadness_rate=egg.sadness_rate, base_sadness_rate=egg.sadness_rate, max_clean=egg.max_cleanliness,
                  base_clean=egg.max_cleanliness, dirt_rate=egg.dirt_rate, base_dirt_rate=egg.dirt_rate,
                  immunity=egg.immunity, base_immunity=egg.immunity, max_sleepiness=egg.max_sleepiness,
                  base_sleepiness=egg.max_sleepiness, sleepiness_rate=egg.sleepiness_rate,
                  base_sleepiness_rate=egg.sleepiness_rate, sleepiness_recovery_rate=egg.sleepiness_recovery_rate,
                  base_sleepiness_recovery_rate=egg.sleepiness_recovery_rate, dna=egg.dna)
    if not player_manager.has_player(owner):
        player_manager.add_player(Player(owner))
    connection = db_manager.create_connection()
    db_manager.add_pet(connection, new_pet)
    db_manager.remove_egg(connection, egg)
    player_manager.add_pet_to_player(owner, new_pet)


# Gets the pet which has the defined owner and name
def get_pet(owner, name):
    pet = None
    if player_manager.has_player(owner):
        for a_pet in player_manager.get_player(owner).pets:
            if a_pet == name:
                pet = a_pet
    if player_manager.has_pet(owner, pet):
        return player_manager.get_player(owner).pets[pet]
    else:
        return None


# Checks if the player is able to add another pet
def can_add(owner):
    if player_manager.has_player(owner):
        player = player_manager.get_player(owner)
        n_pets = len(player.pets)
        max_pets = player.max_pets
        if n_pets >= max_pets:
            return False
    return True


# Updates the pets. If any pets are no longer alive, remove them
async def update_pets(context=None):
    connection = db_manager.create_connection()
    deceased_pets = []
    for player_id in player_manager.players.keys():
        player = player_manager.get_player(player_id)
        for pet_name in player.pets:
            pet = get_pet(player_id, pet_name)
            pet.update(context)
            if not pet.alive:
                deceased_pets.append(pet)
                context = pet.context
                if context is not None:
                    await context.send(f'Sorry to tell you <@{pet.player_id}>, but {pet.name} has passed away.')
            else:
                db_manager.update_pet(connection, pet)
    for passed_pet in deceased_pets:
        player_manager.remove_pet(passed_pet)

    return deceased_pets

##############PET COMMANDS###########


# Display the image of the pet
async def show(owner, pet_name=None, context=None):
    if player_manager.has_player(owner):
        if pet_name is None:
            for a_pet in player_manager.get_player(owner).pets:
                await get_pet(owner, a_pet).show(context)
        else:
            a_pet = get_pet(owner, pet_name)
            if a_pet is not None:
                await a_pet.show(context)
            elif context is not None:
                await context.send(f'Sorry <@{owner}>, you don\'t have a pet named {pet_name}.')
    elif context is not None:
        await context.send(f'Looks like you don\'t have any pets, <@{owner}>.')


# Display the status of the pet or all of the owner's pets
async def status(owner, pet_name=None, context=None):
    if player_manager.has_player(owner):
        if pet_name is None:
            pet_check = False
            player = player_manager.get_player(owner)
            for a_pet in player.pets:
                pet_check = True
                await get_pet(owner, a_pet).show_status(context=context)
            if not pet_check:
                await context.send(f'Sorry <@{owner}>, looks like you don\'t have any pets currently.')
        else:
            a_pet = get_pet(owner, pet_name)
            if a_pet is not None:
                await a_pet.show_status(context=context)
            elif context is not None:
                await context.send(f'Sorry <@{owner}>, you don\'t have a pet named {pet_name}.')
    elif context is not None:
        await context.send(f'Looks like you don\'t have any pets, <@{owner}>.')


# Feed the pet or all of the owner's pets
async def feed(owner, pet_name=None, context=None):
    if player_manager.has_player(owner):
        if pet_name is None:
            for a_pet in player_manager.get_player(owner).pets:
                get_pet(owner, a_pet).feed()
            if context is not None:
                await context.send(f'<@{owner}>, your pets have been fed.')
        else:
            a_pet = get_pet(owner, pet_name)
            if a_pet is not None:
                a_pet.feed()
                if context is not None:
                    await context.send(f'Your pet {pet_name} has been fed.')
            elif context is not None:
                await context.send(f'Sorry <@{owner}>, you don\'t have a pet named {pet_name}.')
    elif context is not None:
        await context.send(f'Looks like you don\'t have any pets, <@{owner}>.')


# Pets the pet or all the owner's pets
async def pet(owner, pet_name=None, context=None):
    if player_manager.has_player(owner):
        if pet_name is None:
            for a_pet in player_manager.get_player(owner).pets:
                get_pet(owner, a_pet).pet()
            if context is not None:
                await context.send(f'<@{owner}>, your pets have been petted.')
        else:
            a_pet = get_pet(owner, pet_name)
            if a_pet is not None:
                a_pet.pet()
                if context is not None:
                    await context.send(f'Your pet {pet_name} has been petted.')
            elif context is not None:
                await context.send(f'Sorry <@{owner}>, you don\'t have a pet named {pet_name}.')
    elif context is not None:
        await context.send(f'Looks like you don\'t have any pets, <@{owner}>.')


# Cleans the pet or all the owner's pets
async def clean(owner, pet_name=None, context=None):
    if player_manager.has_player(owner):
        if pet_name is None:
            for a_pet in player_manager.get_player(owner).pets:
                get_pet(owner, a_pet).clean()
            if context is not None:
                await context.send(f'<@{owner}>, your pets have been cleaned.')
        else:
            a_pet = get_pet(owner, pet_name)
            if a_pet is not None:
                a_pet.clean()
                if context is not None:
                    await context.send(f'Your pet {pet_name} has been cleaned.')
            elif context is not None:
                await context.send(f'Sorry <@{owner}>, you don\'t have a pet named {pet_name}.')
    elif context is not None:
        await context.send(f'Looks like you don\'t have any pets, <@{owner}>.')


# Medicates the pet or all the owner's pets
async def medicate(owner, pet_name=None, context=None):
    if player_manager.has_player(owner):
        if pet_name is None:
            for a_pet in player_manager.get_player(owner).pets:
                get_pet(owner, a_pet).medicate()
            if context is not None:
                await context.send(f'<@{owner}>, your pets have been medicated.')
        else:
            a_pet = get_pet(owner, pet_name)
            if a_pet is not None:
                a_pet.medicate()
                if context is not None:
                    await context.send(f'Your pet {pet_name} has been medicated.')
            elif context is not None:
                await context.send(f'Sorry <@{owner}>, you don\'t have a pet named {pet_name}.')
    elif context is not None:
        await context.send(f'Looks like you don\'t have any pets, <@{owner}>.')


# Adjusts the lights on or off for the specified pet or all the owner's pets
async def lights(owner, message=None, context=None):
    if message is not None:
        if player_manager.has_player(owner):
            if 'on' in message:
                specific = False
                for a_pet in player_manager.get_player(owner).pets:
                    if a_pet in message:
                        specific = True
                        get_pet(owner, a_pet).lights_on()
                        if context is not None:
                            await context.send(f'Lights on for {a_pet.name}.')
                if not specific:
                    for a_pet in player_manager.get_player(owner).pets:
                        get_pet(owner, a_pet).lights_on()
                    if context is not None:
                        await context.send('Lights on!')
            elif 'off' in message:
                specific = False
                for a_pet in player_manager.get_player(owner).pets:
                    if a_pet in message:
                        specific = True
                        get_pet(owner, a_pet).lights_off()
                        if context is not None:
                            await context.send(f'Lights off for {a_pet.name}.')
                if not specific:
                    for a_pet in player_manager.get_player(owner).pets:
                        get_pet(owner, a_pet).lights_off()
                    if context is not None:
                        await context.send('Lights off!')
            elif context is not None:
                await context.send(f'Please specify on or off next time.')
        elif context is not None:
            await context.send(f'Looks like you don\'t have any pets, <@{owner}>.')
    elif player_manager.has_player(owner) and context is not None:
        await context.send(f'Please specify on or off next time.')
    elif context is not None:
        await context.send(f'Looks like you don\'t have any pets, <@{owner}>.')


# Leave the specified pet and remove them from all storage
async def leave(owner, pet_name, context=None):
    if player_manager.has_player(owner) and (pet_name is not None):
        remove_pet = None
        for a_pet in player_manager.get_player(owner).pets:
            if a_pet in pet_name:
                remove_pet = a_pet
        if remove_pet is not None:
            rpet = get_pet(owner, remove_pet)
            player_manager.get_player(owner).remove_pet(remove_pet)
            connection = db_manager.create_connection()
            db_manager.remove_pet(connection, rpet)
            db_manager.update_player(connection, player_manager.get_player(owner))
            if context is not None:
                await context.send(f'{remove_pet} was left')
        elif context is not None:
            context.send(f'Unable to remove the pet {pet_name}.')
    elif context is not None:
        context.send(f'Sorry <@{owner}>, couldn\'t leave that pet.')
