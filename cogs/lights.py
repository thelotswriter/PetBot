import discord
from discord.ext import commands
import pet_manager
import the_pet


class Lights(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(brief='[on/off] [pet] Turn the lights on or off')
    async def lights(self, context, *, message=None):
        player = context.author
        pid = player.id
        if message is None:
            await context.send('Lights on or off?')
        elif 'on' in message:
            if pid in pet_manager.player_pets:
                if message is not None:
                    counter = 0
                    for pet_name in pet_manager.player_pets[pid].keys():
                        if pet_name in message:
                            counter += 1
                            pet_manager.player_pets[pid][pet_name].lights_on()
                    if counter == 0:
                        await context.send(f'No pets named {message} for you, <@{pid}>.')
                else:
                    for pet_name in pet_manager.player_pets[pid].keys():
                        print(pet_name)
                        pet_manager.player_pets[pid][pet_name].lights_on()
            else:
                await context.send('Sorry, no pets to turn lights on for!')
        elif 'off' in message:
            if pid in pet_manager.player_pets:
                if message is not None:
                    counter = 0
                    for pet_name in pet_manager.player_pets[pid].keys():
                        if pet_name in message:
                            counter += 1
                            pet_manager.player_pets[pid][pet_name].lights_off()
                        if counter == 0:
                            await context.send(f'No pets named {message} for you, <@{pid}>.')
                else:
                    for pet_name in pet_manager.player_pets[pid].keys():
                        print(pet_name)
                        pet_manager.player_pets[pid][pet_name].lights_off()
            else:
                await context.send('Sorry, no pets to turn the lights off for!')


def setup(client):
    client.add_cog(Lights(client))