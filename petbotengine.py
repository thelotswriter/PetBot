import asyncio
import time
import threading
import discord
from discord.ext import commands

import pet_manager


# Run update function every 15 minutes
async def update():
    while True:
        await asyncio.sleep(900)
        await pet_manager.update_pets()


# Run event loop
async def run_engine():
    asyncio.get_event_loop().create_task(update())
