import time
import threading
import discord
from discord.ext import commands

import pet_manager


class PetBotEngine(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def start(self):
        super().start()

    def run(self):
        run_engine()


def update():
    pet_manager.update_pets(None)


def run_engine():
    while True:
        update()
        time.sleep(1800)
