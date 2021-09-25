import discord
from discord.ext import commands
import pet_manager
import the_pet


class Feed(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(brief='[pet] Give your pet some food')
    async def feed(self, context, *, message=None):
        player = context.author
        pid = player.id
        if pid in pet_manager.player_pets:
            if message is not None:
                counter = 0
                for pet_name in pet_manager.player_pets[pid].keys():
                    if pet_name in message:
                        counter += 1
                        pet_manager.player_pets[pid][pet_name].feed()
                        await context.send(f'{pet_name} was fed!')
                if counter == 0:
                    await context.send(f'No pets named {message} for you, <@{pid}>.')
            else:
                for pet_name in pet_manager.player_pets[pid].keys():
                    pet_manager.player_pets[pid][pet_name].feed()
                await context.send(f'Your pets were fed, <@{pid}>.')
        else:
            await context.send('Sorry, no pets to feed!')

def setup(client):
    client.add_cog(Feed(client))