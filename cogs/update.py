import discord
from discord.ext import commands
import pet_manager
import the_pet


class Update(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def update(self, context):
        passed_pets = []
        passed_pets.extend(pet_manager.update_pets(context))
        if len(passed_pets) > 1:
            await context.send(f'Unfortunately, {len(passed_pets)} pets have passed away.')
        elif len(passed_pets) > 0:
            await context.send(f'Sadly, {passed_pets[0].name} has passed away.')


def setup(client):
    client.add_cog(Update(client))