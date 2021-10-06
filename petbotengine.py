import asyncio
import time
import threading
import discord
from discord.ext import commands

import pet_manager


# class PetBotEngine(threading.Thread):
#
#     def __init__(self):
#         threading.Thread.__init__(self)
#
#     def start(self):
#         super().start()
#
#     def run(self):
#         run_engine()


async def update():
    while True:
        await asyncio.sleep(900)
        await pet_manager.update_pets()


async def run_engine():
    asyncio.get_event_loop().create_task(update())
    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    # loop.run_until_complete(update())
    # loop.close()
    # while True:
    #     update()
    #     time.sleep(60)
