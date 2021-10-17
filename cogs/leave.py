import discord
from discord.ext import commands
import pet_manager


class Leave(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(brief='[pet] Abandon your pet')
    async def leave(self, context, *, message=None):
        player = context.author
        pid = player.id
        if message is None:
            await context.send('Which pet would you like to leave?')
            message = await self.client.wait_for('message', check=lambda message: message.author == context.author)
            message = message.content
        await context.send(f'Are you sure, <@{pid}> (yes/no)?')
        confirm = await self.client.wait_for('message', check=lambda message: message.author == context.author)
        confirm = confirm.content
        if confirm.lower() == 'yes':
            await pet_manager.leave(pid, message)
        else:
            await context.send(f'Your pet, {message}, was not abandoned.', context=context)


def setup(client):
    client.add_cog(Leave(client))