import os
import discord


class Egg:

    def __init__(self, player_id, egg_id=0, max_food=5, hunger_rate=1.5, max_happiness=5, sadness_rate=1.5, max_clean=5, dirt_rate=0.75, immunity=0.5, max_sleepiness=5, sleepiness_rate=1.5, sleepiness_recovery_rate=1.5, dna=[]):
        self.player_id = player_id
        self.egg_id = egg_id
        self.max_food = float(max_food)
        self.hunger_rate = float(hunger_rate)
        self.max_happiness = float(max_happiness)
        self.sadness_rate = float(sadness_rate)
        self.max_cleanliness = float(max_clean)
        self.dirt_rate = float(dirt_rate)
        self.immunity = float(immunity)
        self.max_sleepiness = float(max_sleepiness)
        self.sleepiness_rate = sleepiness_rate
        self.sleepiness_recovery_rate = sleepiness_recovery_rate
        self.dna = dna

    async def show(self, context=None):
        if self.context is not None:
            path = os.path.dirname(os.path.abspath(__file__))
            path = os.path.join(path, 'images')
            path = os.path.join(path, str(self.dna[0]))
            path = os.path.join(path, 'expanded_egg.png')
            await context.send(file=discord.File(path))