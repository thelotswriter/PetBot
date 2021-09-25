from the_pet import Pet

player_pets = dict()
pets = []


def add_pet(owner, pet_id, name):
    new_pet = Pet(owner, pet_id, name)
    if owner not in player_pets:
        player_pets[owner] = dict()
    player_pets[owner][name] = new_pet
    pets.append(new_pet)

def update_pets(context):
    deceased_pets = []
    for a_pet in pets:
        a_pet.update(context)
        if not a_pet.alive:
            deceased_pets.append(a_pet)
    for passed_pet in deceased_pets:
        del player_pets[passed_pet.player_id][passed_pet.name]
        if len(player_pets[passed_pet.player_id]) <= 0:
            del player_pets[passed_pet.player_id]
        p = 0
        for p in range(len(pets)):
            if pets[p].pet_id == passed_pet.pet_id:
                del pets[p]
                break
    return deceased_pets

