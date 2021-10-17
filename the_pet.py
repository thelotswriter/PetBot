import datetime
import os
import discord
from discord.ext import commands
import random

from the_egg import Egg
import image_expander


# Defines a pet for players to care for. Includes all of its stats,
# ability for players to interact with the pet, and ability for the
# pet to interact with the player
class Pet:

    # Initialize values and run preliminary update
    def __init__(self, player_id, name='', level=0, birthday=datetime.datetime.now(), current_food=0.3, max_food=5,
                 base_food=5, hunger_rate=1.5, base_hunger_rate=1.5, current_happiness=0.5, max_happiness=5,
                 base_happiness=5, sadness_rate=1.5, base_sadness_rate=1.5, current_clean=1.0, max_clean=5,
                 base_clean=5, dirt_rate=0.75, base_dirt_rate=0.75, immunity=0.5, base_immunity=0.5, sick=False,
                 sleepiness=0, max_sleepiness=5, base_sleepiness=5, sleepiness_rate=1.5, base_sleepiness_rate=1.5,
                 sleepiness_recovery_rate=1.5, base_sleepiness_recovery_rate=1.5, asleep=False, lights=True, dna=[],
                 timestamp=datetime.datetime.now(), mute=False, context=None, age_tracker=0, pet_id=0, avg_food=0.0,
                 avg_happiness=0, avg_cleanliness=0, avg_sleepiness=0, avg_sick=0, tot_mins=0):
        self.player_id = player_id
        self.name = name
        self.level = level
        self.birthday = birthday
        self.max_food = float(max_food)
        self.base_food = float(base_food)
        self.current_food = current_food * self.max_food
        self.hunger_rate = float(hunger_rate)
        self.base_hunger_rate = float(base_hunger_rate)
        self.max_happiness = float(max_happiness)
        self.base_happiness = float(base_happiness)
        self.current_happiness = current_happiness * self.max_happiness
        self.sadness_rate = float(sadness_rate)
        self.base_sadness_rate = float(base_sadness_rate)
        self.max_cleanliness = float(max_clean)
        self.base_cleanliness = float(base_clean)
        self.cleanliness = current_clean * self.max_cleanliness
        self.dirt_rate = float(dirt_rate)
        self.base_dirt_rate = float(base_dirt_rate)
        self.immunity = float(immunity)
        self.base_immunity = float(base_immunity)
        self.sick = sick
        self.max_sleepiness = float(max_sleepiness)
        self.base_sleepiness = float(base_sleepiness)
        self.current_sleepiness = sleepiness * self.max_sleepiness
        self.sleepiness_rate = float(sleepiness_rate)
        self.base_sleepiness_rate = float(base_sleepiness_rate)
        self.sleepiness_recovery_rate = float(sleepiness_recovery_rate)
        self.base_sleepiness_recovery_rate = float(base_sleepiness_recovery_rate)
        self.asleep = asleep
        self.lights = lights
        self.age_tracker = age_tracker
        self.dna = dna
        if len(dna) == 0:
            self.dna.append(random.randint(1,4))
        if len(dna) == 1:
            self.generate_dna()
        self.last_check_time = timestamp
        self.alive = True
        self.mute = mute
        self.context = context
        self.pet_id = pet_id
        # Care tracking
        self.avg_food = float(avg_food)
        self.avg_happiness = float(avg_happiness)
        self.avg_cleanliness = float(avg_cleanliness)
        self.avg_sleepiness = float(avg_sleepiness)
        self.avg_sick = float(avg_sick)
        self.tot_mins = float(tot_mins)
        # Update pet
        self.update(loading_update=True)

    def set_context(self, context):
        self.context = context

    # Update the pet's current state. This is run periodically
    # by the engine.
    def update(self, loading_update=False, context=None):
        if context is not None:
            self.context = context
        cur_time = datetime.datetime.now()
        age = cur_time - self.birthday
        up_time = cur_time - self.last_check_time
        # If the pet wasn't just created or checked, update stats
        if up_time.days > 0 or up_time.seconds > 10:
            if self.level == 0:
                self.level = 1
            elif up_time.days > 10:
                self.alive = False
            elif self.level > 0:
                hours = float(up_time.days * 24 + float(up_time.seconds) / 60 / 60)
                if self.asleep:
                    self.sleep_update(hours)
                else:
                    self.awake_update(hours)
            if self.current_happiness <= 0 or self.current_food <= 0 or self.cleanliness <= 0:
                self.alive = False
            elif not self.asleep and self.level > 0:
                if not self.choose_to_sleep():
                    self.choose_to_alert()
            elif self.asleep and self.level > 0:
                if self.choose_to_wake():
                    self.choose_to_alert()
            if self.alive and not loading_update:
                up_mins = float(up_time.seconds) / 60 + float(up_time.days * 1440)
                self.avg_food += up_mins * self.current_food / self.max_food
                self.avg_happiness += up_mins * self.current_happiness / self.max_happiness
                self.avg_cleanliness += up_mins * self.cleanliness / self.max_cleanliness
                self.avg_sleepiness += up_mins * self.current_sleepiness / self.max_sleepiness
                if self.sick:
                    self.avg_sick += up_mins
                self.tot_mins += up_mins
        self.update_level(age)
        self.last_check_time = cur_time

    # Update when sleeping
    def sleep_update(self, hours):
        self.current_food -= self.hunger_rate * 0.25 * hours
        self.current_happiness -= self.sadness_rate * 0.1 * hours
        self.current_sleepiness -= self.sleepiness_recovery_rate * hours
        self.current_food = max(self.current_food, 0.0)
        self.current_happiness = max(self.current_happiness, 0.0)
        self.current_sleepiness = max(self.current_sleepiness, 0.0)
        self.choose_to_wake()

    # Update when awake
    def awake_update(self, hours):
        self.current_food -= self.hunger_rate * hours
        self.current_happiness -= self.sadness_rate * hours
        self.current_sleepiness += self.sleepiness_rate * hours
        self.cleanliness -= self.dirt_rate * hours
        cleanness_ratio = self.cleanliness / self.max_cleanliness
        if self.immunity < (1.0 - cleanness_ratio):
            sick_roll = random.random()
            if sick_roll > self.immunity:
                self.sick = True
        if self.sick:
            self.cleanliness -= self.dirt_rate * hours
        self.current_food = max(self.current_food, 0.0)
        self.current_happiness = max(self.current_happiness, 0.0)
        self.current_sleepiness = min(self.current_sleepiness, self.max_sleepiness)
        self.choose_to_sleep()

    # Check if ready to progress to the next level or, if at level 4,
    # if stats should decay
    def update_level(self, age):
        if self.level == 0:
            self.level = 1
        if self.level == 1 and (age.days > 0 or age.seconds > 60 * 60 * 4):
            self.level = 2
            self.max_food *= 1.5
            self.hunger_rate *= 0.8
            self.max_happiness *= 1.5
            self.sadness_rate *= 0.8
            self.max_cleanliness *= 1.5
            self.dirt_rate *= 0.8
            self.max_sleepiness *= 1.5
            self.sleepiness_rate *= 0.8
            self.sleepiness_recovery_rate *= 1.2
            self.immunity = min(0.9, self.immunity * 1.2)
        if self.level == 2 and age.days > 0:
            self.level = 3
            self.max_food *= 1.5
            self.hunger_rate *= 1.5
            self.max_happiness *= 1.5
            self.sadness_rate *= 0.8
            self.max_cleanliness *= 1.5
            self.dirt_rate *= 0.8
            self.max_sleepiness *= 1.5
            self.sleepiness_rate *= 0.8
            self.sleepiness_recovery_rate *= 1.2
            self.immunity = min(0.9, self.immunity * 1.2)
        if self.level == 3 and age.days > 2:
            self.level = 4
            self.max_food *= 1.5
            self.hunger_rate *= 1.5
            self.max_happiness *= 1.5
            self.sadness_rate *= 0.8
            self.max_cleanliness *= 1.5
            self.dirt_rate *= 0.8
            self.max_sleepiness *= 1.5
            self.sleepiness_rate *= 0.8
            self.sleepiness_recovery_rate *= 1.2
            self.immunity = min(0.9, self.immunity * 1.2)
        if self.level == 4 and age.days > 6:
            old_days = age.days - 6
            if old_days > 2 * self.age_tracker:
                self.age_tracker += 1
                self.max_food *= 0.9
                self.hunger_rate *= 1
                self.max_happiness *= 1
                self.sadness_rate *= 1.2
                self.max_cleanliness *= 0.9
                self.dirt_rate *= 1
                self.max_sleepiness *= 0.9
                self.sleepiness_rate *= 1.2
                self.sleepiness_recovery_rate *= 0.9
                self.immunity *= 0.9

    # Generates the dna. Called for new pets without a parent
    def generate_dna(self):
        for x in range(3):
            self.dna.append(random.randint(1,2))

    ##############INTERACTIONS WITH PLAYER###########

    # Show what the pet looks like
    async def show(self, context=None):
        if context is not None:
            self.context = context
        if self.context is not None:
            path = os.path.dirname(os.path.abspath(__file__))
            path = os.path.join(path, 'images')
            if self.lights:
                for x in range(self.level):
                    path = os.path.join(path, str(self.dna[x]))
                image_expander.expand(path)
                path = os.path.join(path, 'expanded_pet.png')
            elif self.asleep:
                path = os.path.join(path, 'expanded_sleep.png')
            else:
                path = os.path.join(path, 'expanded_dark.png')
            await context.send(self.name, file=discord.File(path))

    # List current stats
    async def show_status(self, context):
        self.context = context
        if self.sick:
            sickly = 'Yes'
        else:
            sickly = 'No'
        if self.asleep:
            sleeping = 'Yes'
        else:
            sleeping = 'No'
        await context.send(f'<@{self.player_id}>\'s pet {self.name}:\n' +
                           f'Hunger: {self.current_food:.0f} / {self.max_food:.0f} \n' +
                           f'Happiness: {self.current_happiness:.0f} / {self.max_happiness:.0f}\n' +
                           f'Cleanliness: {self.cleanliness:.0f} / {self.max_cleanliness:.0f}\n' +
                           f'Sleepiness: {self.current_sleepiness:.0f} / {self.max_sleepiness:.0f}\n' +
                           f'Sick: {sickly}\n' +
                           f'Sleeping: {sleeping}')

    # Increases current food
    def feed(self):
        self.current_food = min(self.max_food, self.current_food + 5)

    # Increases current happiness
    def pet(self):
        self.current_happiness = min(self.max_happiness, self.current_happiness + 5)

    # Increases current cleanliness
    def clean(self):
        if self.sick:
            self.cleanliness = min(self.max_cleanliness * 0.75, self.cleanliness + 10)
        else:
            self.cleanliness = self.max_cleanliness

    # Heals a sick pet. Healthy pets will lose happiness if medicated
    def medicate(self):
        if not self.sick:
            self.current_happiness -= self.sadness_rate
            self.current_happiness = max(self.current_happiness, 0.0)
        self.sick = False

    # Turns on the light
    def lights_on(self):
        self.lights = True

    # Turns off the light
    def lights_off(self):
        self.lights = False

    # Switches the light from on to off or off to on
    def lights(self):
        if self.lights:
            self.lights = False
        else:
            self.lights = True

    #################LEARNED BEHAVIORS#################

    # Chooses whether to wake from sleep
    def choose_to_wake(self):
        if self.lights and self.current_sleepiness <= 0.5 * self.max_sleepiness:
            self.asleep = False
            return True
        elif self.current_sleepiness <= 0.0:
            self.asleep = False
            return True
        else:
            return False

    # Choose to sleep
    def choose_to_sleep(self):
        if self.lights and self.current_sleepiness >= self.max_sleepiness * 0.9:
            self.asleep = True
            return True
        elif self.current_sleepiness >= 0.7 * self.max_sleepiness:
            self.asleep = True
            return True
        else:
            return False

    # Currently does nothing. With AI, will be allowed to choose
    # to send from a selection of messages (request food, petting, etc)
    def choose_to_alert(self):
        if self.context is None:
            return False
        if self.mute:
            return False
        else:
            return False

    # Will choose if a status shoule be shown
    def choose_status_to_show(self):
        return None

    #################TEST FUNCTIONS#################

    # Test function to level up
    def level_up(self):
        self.level = min(4, self.level + 1)
