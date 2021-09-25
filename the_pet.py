import datetime
import discord
from discord.ext import commands


class Pet:

    def __init__(self, player_id, pet_id, name='', level=0, birthday=datetime.datetime.now(), current_food=1.0, max_food=10, hunger_rate=1.0, current_happiness=1.0, max_happiness=10, sadness_rate=1.0, current_clean=1.0, max_clean=20, dirt_rate=1.0, immunity=0.5, sick=False, sleepiness=0, max_sleepiness=10, sleepiness_rate=1.0, sleepiness_recovery_rate=1.0, asleep=False, lights=True, image=None, timestamp=datetime.datetime.now(), mute=False, context=None):
        self.player_id = player_id
        self.pet_id = pet_id
        self.name = name
        self.level = level
        self.birthday = birthday
        self.max_food = float(max_food)
        self.current_food = current_food * self.max_food
        self.hunger_rate = float(hunger_rate)
        self.max_happiness = float(max_happiness)
        self.current_happiness = current_happiness * self.max_happiness
        self.sadness_rate = float(sadness_rate)
        self.max_cleanliness = float(max_clean)
        self.cleanliness = current_clean * self.max_cleanliness
        self.dirt_rate = float(dirt_rate)
        self.immunity = float(immunity)
        self.sick = sick
        self.max_sleepiness = float(max_sleepiness)
        self.current_sleepiness = sleepiness * self.max_sleepiness
        self.sleepiness_rate = sleepiness_rate
        self.sleepiness_recovery_rate = sleepiness_recovery_rate
        self.asleep = asleep
        self.lights = lights
        self.image = image
        self.last_check_time = timestamp
        self.alive = True
        self.mute = mute
        self.context = context
        self.update(loading_update=True)

    def set_context(self, context):
        self.context = context

    def update(self, loading_update=False, context=None):
        if context is not None:
            self.context = context
        cur_time = datetime.datetime.now()
        age = cur_time - self.birthday
        up_time = cur_time - self.last_check_time
        if up_time.days > 0 or up_time.seconds > 10:
            if self.level == 0:
                self.level = 1
                # await context.send('Your egg has hatched, ' + self.player_id + '!')
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
        self.last_check_time = cur_time

    def sleep_update(self, hours):
        self.current_food -= self.hunger_rate * 0.25 * hours
        self.current_happiness -= self.sadness_rate * 0.1 * hours
        self.current_sleepiness -= self.sleepiness_recovery_rate * hours
        self.current_food = max(self.current_food, 0.0)
        self.current_happiness = max(self.current_happiness, 0.0)
        self.current_sleepiness = max(self.current_sleepiness, 0.0)
        self.choose_to_wake()

    def awake_update(self, hours):
        self.current_food -= self.hunger_rate * hours
        self.current_happiness -= self.sadness_rate * hours
        self.current_sleepiness += self.sleepiness_rate * hours
        self.cleanliness -= self.dirt_rate * hours
        if self.sick:
            self.cleanliness -= self.dirt_rate * hours
        self.current_food = max(self.current_food, 0.0)
        self.current_happiness = max(self.current_happiness, 0.0)
        self.current_sleepiness = min(self.current_sleepiness, self.max_sleepiness)
        self.choose_to_sleep()

    ##############INTERACTIONS WITH PLAYER###########

    def show(self, context):
        self.context = context

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
        await context.send(f'<@{self.player_id}>\'s pet {self.name} (Lv. {self.level}):\n' +
                           f'Hunger: {self.current_food:.0f} / {self.max_food:.0f} \n' +
                           f'Happiness: {self.current_happiness:.0f} / {self.max_happiness:.0f}\n' +
                           f'Cleanliness: {self.cleanliness:.0f} / {self.max_cleanliness:.0f}\n' +
                           f'Sleepiness: {self.current_sleepiness:.0f} / {self.max_sleepiness:.0f}\n' +
                           f'Sick: {sickly}\n' +
                           f'Sleeping: {sleeping}')

    def feed(self):
        self.current_food = min(self.max_food, self.current_food + 5)

    def pet(self):
        self.current_happiness = min(self.max_happiness, self.current_happiness + 5)

    def clean(self):
        if self.sick:
            self.cleanliness = min(self.max_cleanliness * 0.75, self.cleanliness + 10)
        else:
            self.cleanliness = self.max_cleanliness

    def medicate(self):
        if not self.sick:
            self.current_happiness -= self.sadness_rate
            self.current_happiness = max(self.current_happiness, 0.0)
        self.sick = False

    def lights_on(self):
        self.lights = True

    def lights_off(self):
        self.lights = False

    #################LEARNED BEHAVIORS#################

    def choose_to_wake(self):
        if self.lights and self.current_sleepiness <= 0.5 * self.max_sleepiness:
            self.asleep = False
            return True
        elif self.current_sleepiness <= 0.0:
            self.asleep = False
            return True
        else:
            return False

    def choose_to_sleep(self):
        if self.lights and self.current_sleepiness >= self.max_sleepiness * 0.9:
            self.asleep = True
            return True
        elif self.current_sleepiness >= 0.7 * self.max_sleepiness:
            self.asleep = True
            return True
        else:
            return False

    def choose_to_alert(self):
        if self.context is None:
            return False
        if self.mute:
            return False
        else:
            return False

    def choose_status_to_show(self):
        return None
