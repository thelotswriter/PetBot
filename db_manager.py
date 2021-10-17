import sqlite3
from sqlite3 import Error
from os import path
import datetime

import player_manager
from the_player import Player
from the_pet import Pet
from the_egg import Egg
import pet_manager


# Add player to the database
def add_player(connection, player):
    sql = """INSERT INTO players(id,maxpets,maxeggs,xp)
             VALUES(?,?,?,?)"""
    player_data = (player.player_id, player.max_pets, player.max_eggs, player.xp)
    curs = connection.cursor()
    curs.execute(sql, player_data)
    connection.commit()
    player.player_id = curs.lastrowid


# Add the pet to the database
def add_pet(connection, pet):
    current_sql = """INSERT INTO current_pets(player_id,name,level,birthday,current_food,max_food,base_food,hunger_rate,base_hunger_rate,current_happiness,max_happiness,base_happiness,sadness_rate,base_sadness_rate,current_clean,max_clean,base_clean,dirt_rate,base_dirt_rate,immunity,base_immunity,sick,sleepiness,max_sleepiness,base_sleepiness,sleepiness_rate,base_sleepiness_rate,sleepiness_recovery_rate,base_sleepiness_recovery_rate,asleep,lights,dna,timestamp,mute,age_tracker,avg_food,avg_happiness,avg_cleanliness,avg_sleepiness,avg_sick,tot_mins)
             VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
    birthday = pet.birthday.strftime("%m:%d:%Y:%H:%M:%S")
    dna = ''
    for d in pet.dna:
        dna += str(d)
        dna += '+'
    dna = dna[:-1]
    timestamp = pet.last_check_time.strftime("%m:%d:%Y:%H:%M:%S")
    current_data = (pet.player_id, pet.name, pet.level, birthday, pet.current_food, pet.max_food, pet.base_food, pet.hunger_rate, pet.base_hunger_rate, pet.current_happiness, pet.max_happiness, pet.base_happiness, pet.sadness_rate, pet.base_sadness_rate, pet.cleanliness, pet.max_cleanliness, pet.base_cleanliness, pet.dirt_rate, pet.base_dirt_rate, pet.immunity, pet.base_immunity, pet.sick, pet.current_sleepiness, pet.max_sleepiness, pet.base_sleepiness, pet.sleepiness_rate, pet.base_sleepiness_rate, pet.sleepiness_recovery_rate, pet.base_sleepiness_recovery_rate, pet.asleep, pet.lights, dna, timestamp, pet.mute, pet.age_tracker, pet.avg_food, pet.avg_happiness, pet.avg_cleanliness, pet.avg_sleepiness, pet.avg_sick, pet.tot_mins)
    curs = connection.cursor()
    curs.execute(current_sql, current_data)
    connection.commit()
    pet.pet_id = curs.lastrowid
    pet_sql = """INSERT INTO pets(player_id,name,level,birthday,current_food,max_food,base_food,hunger_rate,base_hunger_rate,current_happiness,max_happiness,base_happiness,sadness_rate,base_sadness_rate,current_clean,max_clean,base_clean,dirt_rate,base_dirt_rate,immunity,base_immunity,sick,sleepiness,max_sleepiness,base_sleepiness,sleepiness_rate,base_sleepiness_rate,sleepiness_recovery_rate,base_sleepiness_recovery_rate,asleep,lights,dna,timestamp,mute,age_tracker,pet_id,avg_food,avg_happiness,avg_cleanliness,avg_sleepiness,avg_sick,tot_mins)
             VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
    pet_data = (pet.player_id, pet.name, pet.level, birthday, pet.current_food, pet.max_food, pet.base_food, pet.hunger_rate, pet.base_hunger_rate, pet.current_happiness, pet.max_happiness, pet.base_happiness, pet.sadness_rate, pet.base_sadness_rate, pet.cleanliness, pet.max_cleanliness, pet.base_cleanliness, pet.dirt_rate, pet.base_dirt_rate, pet.immunity, pet.base_immunity, pet.sick, pet.current_sleepiness, pet.max_sleepiness, pet.base_sleepiness, pet.sleepiness_rate, pet.base_sleepiness_rate, pet.sleepiness_recovery_rate, pet.base_sleepiness_recovery_rate, pet.asleep, pet.lights, dna, timestamp, pet.mute, pet.age_tracker, pet.pet_id, pet.avg_food, pet.avg_happiness, pet.avg_cleanliness, pet.avg_sleepiness, pet.avg_sick, pet.tot_mins)
    curs.execute(pet_sql, pet_data)
    connection.commit()


# Adds the egg to the database
def add_egg(connection, egg):
    sql = """INSERT INTO eggs(player_id,max_food,hunger_rate,max_happiness,sadness_rate,max_clean,dirt_rate,immunity,max_sleepiness,sleepiness_rate,sleepiness_recovery_rate,dna)
             VALUES(?,?,?,?,?,?,?,?,?,?,?,?)"""
    dna = ''
    for d in egg.dna:
        dna += str(d)
        dna += '+'
    dna = dna[:-1]
    egg_data = (egg.player_id, egg.max_food, egg.hunger_rate, egg.max_happiness, egg.sadness_rate, egg.max_cleanliness, egg.dirt_rate, egg.immunity, egg.max_sleepiness, egg.sleepiness_rate, egg.sleepiness_recovery_rate, dna)
    curs = connection.cursor()
    curs.execute(sql, egg_data)
    connection.commit()
    egg.egg_id = curs.lastrowid


# Gets the players currently stored in the database and loads them into petbot
def get_players(connection):
    curs = connection.cursor()
    curs.execute("SELECT * FROM players")
    player_rows = curs.fetchall()
    for player_row in player_rows:
        player_manager.add_player(Player(player_row[0], max_pets=player_row[1], max_eggs=player_row[2], xp=player_row[3]))


# Gets the pets stored in the database and loads them into petbot
def get_pets(connection):
    curs = connection.cursor()
    curs.execute("SELECT * FROM current_pets")
    pet_rows = curs.fetchall()
    for pet_row in pet_rows:
        birthday = datetime.datetime.strptime(pet_row[33], "%m:%d:%Y:%H:%M:%S")
        split_dna = pet_row[32].split('+')
        dna = []
        for d in split_dna:
            if d != '':
                dna.append(int(d))
        timestamp = datetime.datetime.strptime(pet_row[33], "%m:%d:%Y:%H:%M:%S")
        pet = Pet(pet_row[1], name=pet_row[2], level=pet_row[3], birthday=birthday, current_food=pet_row[5] / pet_row[7],
                  max_food=pet_row[6], base_food=pet_row[7], hunger_rate=pet_row[8], base_hunger_rate=pet_row[9],
                  current_happiness=pet_row[10] / pet_row[11], max_happiness=pet_row[11], base_happiness=pet_row[12],
                  sadness_rate=pet_row[13], base_sadness_rate=pet_row[14], current_clean=pet_row[15] / pet_row[16],
                  max_clean=pet_row[16], base_clean=pet_row[17], dirt_rate=pet_row[18], base_dirt_rate=pet_row[19],
                  immunity=pet_row[20], base_immunity=pet_row[21], sick=pet_row[22], sleepiness=pet_row[23] / pet_row[24],
                  max_sleepiness=pet_row[24], base_sleepiness=pet_row[25], sleepiness_rate=pet_row[26],
                  base_sleepiness_rate=pet_row[27], sleepiness_recovery_rate=pet_row[28],
                  base_sleepiness_recovery_rate=pet_row[29], asleep=pet_row[30], lights=pet_row[31], dna=dna,
                  timestamp=timestamp, mute=pet_row[34], age_tracker=pet_row[35],
                  pet_id=pet_row[0], avg_food=pet_row[36], avg_happiness=pet_row[37], avg_cleanliness=pet_row[38],
                  avg_sleepiness=pet_row[39], avg_sick=pet_row[40], tot_mins=pet_row[41])
        player_manager.add_pet_to_player(pet.player_id, pet)


# Gets the eggs stored in the database and loads them into petbot
def get_eggs(connection):
    curs = connection.cursor()
    curs.execute("SELECT * FROM eggs")
    egg_rows = curs.fetchall()
    for egg_row in egg_rows:
        split_dna = egg_row[12].split('+')
        dna = []
        for d in split_dna:
            if d != '':
                dna.append(int(d))
        egg = Egg(egg_row[1], egg_id=egg_row[0], max_food=egg_row[2], hunger_rate=egg_row[3], max_happiness=egg_row[4],
                  sadness_rate=egg_row[5], max_clean=egg_row[6], dirt_rate=egg_row[7], immunity=egg_row[8],
                  max_sleepiness=egg_row[9], sleepiness_rate=egg_row[10], sleepiness_recovery_rate=egg_row[11], dna=dna)
        player_manager.add_egg_to_player(egg.player_id, egg)


# Updates the stored data in the database to reflect current stats
def update_player(connection, player):
    sql = """UPDATE players
              SET maxpets = ? ,
                  maxeggs = ? ,
                  xp = ?
                WHERE id = ?"""
    player_data = (player.max_pets, player.max_eggs, player.xp, player.player_id)
    curs = connection.cursor()
    curs.execute(sql, player_data)
    connection.commit()


# Updates the current pets and adds to the pet tracking
def update_pet(connection, pet):
    cur_sql = """UPDATE current_pets
                  SET level = ? ,
                      current_food = ? ,
                      max_food = ? ,
                      hunger_rate = ? ,
                      current_happiness = ? ,
                      max_happiness = ? ,
                      sadness_rate = ? ,
                      current_clean = ? ,
                      max_clean = ? ,
                      dirt_rate = ? ,
                      immunity = ? ,
                      sick = ? ,
                      sleepiness = ? ,
                      max_sleepiness = ? ,
                      sleepiness_rate = ? ,
                      sleepiness_recovery_rate = ? ,
                      asleep = ? ,
                      lights = ? ,
                      timestamp = ? ,
                      mute = ? ,
                      age_tracker = ? ,
                      avg_food = ? ,
                      avg_happiness = ? ,
                      avg_cleanliness = ? ,
                      avg_sleepiness = ? ,
                      avg_sick = ? ,
                      tot_mins = ?
                  WHERE id = ?"""
    birthday = pet.birthday.strftime("%m:%d:%Y:%H:%M:%S")
    dna = ''
    for d in pet.dna:
        dna += str(d)
        dna += '+'
    timestamp = pet.last_check_time.strftime("%m:%d:%Y:%H:%M:%S")
    cur_data = (pet.level, pet.current_food, pet.max_food, pet.hunger_rate, pet.current_happiness, pet.max_happiness,
    pet.sadness_rate, pet.cleanliness, pet.max_cleanliness, pet.dirt_rate, pet.immunity, pet.sick,
    pet.current_sleepiness, pet.max_sleepiness, pet.sleepiness_rate, pet.sleepiness_recovery_rate, pet.asleep,
    pet.lights, timestamp, pet.mute, pet.age_tracker, pet.avg_food, pet.avg_happiness, pet.avg_cleanliness,
    pet.avg_sleepiness, pet.avg_sick, pet.tot_mins, pet.pet_id)
    curs = connection.cursor()
    curs.execute(cur_sql, cur_data)
    connection.commit()
    pet_sql = """INSERT INTO pets(player_id,name,level,birthday,current_food,max_food,base_food,hunger_rate,base_hunger_rate,current_happiness,max_happiness,base_happiness,sadness_rate,base_sadness_rate,current_clean,max_clean,base_clean,dirt_rate,base_dirt_rate,immunity,base_immunity,sick,sleepiness,max_sleepiness,base_sleepiness,sleepiness_rate,base_sleepiness_rate,sleepiness_recovery_rate,base_sleepiness_recovery_rate,asleep,lights,dna,timestamp,mute,age_tracker,pet_id,avg_food,avg_happiness,avg_cleanliness,avg_sleepiness,avg_sick,tot_mins)
                 VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
    pet_data = (
    pet.player_id, pet.name, pet.level, birthday, pet.current_food, pet.max_food, pet.base_food, pet.hunger_rate,
    pet.base_hunger_rate, pet.current_happiness, pet.max_happiness, pet.base_happiness, pet.sadness_rate,
    pet.base_sadness_rate, pet.cleanliness, pet.max_cleanliness, pet.base_cleanliness, pet.dirt_rate,
    pet.base_dirt_rate, pet.immunity, pet.base_immunity, pet.sick, pet.current_sleepiness, pet.max_sleepiness,
    pet.base_sleepiness, pet.sleepiness_rate, pet.base_sleepiness_rate, pet.sleepiness_recovery_rate,
    pet.base_sleepiness_recovery_rate, pet.asleep, pet.lights, dna, timestamp, pet.mute, pet.age_tracker, pet.pet_id,
    pet.avg_food, pet.avg_happiness, pet.avg_cleanliness, pet.avg_sleepiness, pet.avg_sick, pet.tot_mins)
    curs.execute(pet_sql, pet_data)
    connection.commit()


# Removes the pet from the current pet table and removes all data from the pet tracking
def remove_pet(connection, pet):
    current_sql = f'DELETE FROM current_pets WHERE id={pet.pet_id}'
    curs = connection.cursor()
    curs.execute(current_sql)
    connection.commit()
    pets_sql = f'DELETE FROM pets WHERE pet_id={pet.pet_id}'
    curs.execute(pets_sql)
    connection.commit()


# Removes the egg from the database
def remove_egg(connection, egg):
    current_sql = f'DELETE FROM eggs WHERE id={egg.egg_id}'
    curs = connection.cursor()
    curs.execute(current_sql)
    connection.commit()


# Creates a connection to the sql server
def create_connection():
    db = path.dirname(path.abspath(__file__))
    db = path.join(db, 'db')
    db = path.join(db, 'petsql.db')
    connection = None
    try:
        connection = sqlite3.connect(db)
        return connection
    except Error as er:
        print(er)
    return connection


# Creates the tables used by petbot
def create_tables(connection):
    players_table_sql = """CREATE TABLE IF NOT EXISTS players (
                            id integer PRIMARY KEY,
                            maxpets integer NOT NULL,
                            maxeggs integer NOT NULL,
                            xp integer NOT NULL
                        );"""
    pets_table_sql = """CREATE TABLE IF NOT EXISTS pets (
                                id integer PRIMARY KEY,
                                player_id integer NOT NULL,
                                name text NOT NULL,
                                level integer NOT NULL,
                                birthday text NOT NULL,
                                current_food real NOT NULL,
                                max_food real NOT NULL,
                                base_food real NOT NULL,
                                hunger_rate real NOT NULL,
                                base_hunger_rate real NOT NULL,
                                current_happiness real NOT NULL,
                                max_happiness real NOT NULL,
                                base_happiness real NOT NULL,
                                sadness_rate real NOT NULL,
                                base_sadness_rate real NOT NULL,
                                current_clean real NOT NULL,
                                max_clean real NOT NULL,
                                base_clean real NOT NULL,
                                dirt_rate real NOT NULL,
                                base_dirt_rate real NOT NULL,
                                immunity real NOT NULL,
                                base_immunity real NOT NULL,
                                sick integer NOT NULL,
                                sleepiness real NOT NULL,
                                max_sleepiness real NOT NULL,
                                base_sleepiness real NOT NULL,
                                sleepiness_rate real NOT NULL,
                                base_sleepiness_rate real NOT NULL,
                                sleepiness_recovery_rate real NOT NULL,
                                base_sleepiness_recovery_rate real NOT NULL,
                                asleep integer NOT NULL,
                                lights integer NOT NULL,
                                dna text NOT NULL,
                                timestamp text NOT NULL,
                                mute integer NOT NULL,
                                age_tracker integer NOT NULL,
                                pet_id integer NOT NULL,
                                avg_food real NOT NULL,
                                avg_happiness real NOT NULL,
                                avg_cleanliness real NOT NULL,
                                avg_sleepiness real NOT NULL,
                                avg_sick real NOT NULL,
                                tot_mins real NOT NULL,
                                FOREIGN KEY (player_id) REFERENCES players (id)
                                FOREIGN KEY (pet_id) REFERENCES current_pets (id)
                            );"""
    eggs_table_sql = """CREATE TABLE IF NOT EXISTS eggs (
                                id integer PRIMARY KEY,
                                player_id integer NOT NULL,
                                max_food real NOT NULL,
                                hunger_rate real NOT NULL,
                                max_happiness real NOT NULL,
                                sadness_rate real NOT NULL,
                                max_clean real NOT NULL,
                                dirt_rate real NOT NULL,
                                immunity real NOT NULL,
                                max_sleepiness real NOT NULL,
                                sleepiness_rate real NOT NULL,
                                sleepiness_recovery_rate real NOT NULL,
                                dna text NOT NULL,
                                FOREIGN KEY (player_id) REFERENCES players (id)
                            );"""
    current_pets_table_sql = """CREATE TABLE IF NOT EXISTS current_pets (
                                id integer PRIMARY KEY,
                                player_id integer NOT NULL,
                                name text NOT NULL,
                                level integer NOT NULL,
                                birthday text NOT NULL,
                                current_food real NOT NULL,
                                max_food real NOT NULL,
                                base_food real NOT NULL,
                                hunger_rate real NOT NULL,
                                base_hunger_rate real NOT NULL,
                                current_happiness real NOT NULL,
                                max_happiness real NOT NULL,
                                base_happiness real NOT NULL,
                                sadness_rate real NOT NULL,
                                base_sadness_rate real NOT NULL,
                                current_clean real NOT NULL,
                                max_clean real NOT NULL,
                                base_clean real NOT NULL,
                                dirt_rate real NOT NULL,
                                base_dirt_rate real NOT NULL,
                                immunity real NOT NULL,
                                base_immunity real NOT NULL,
                                sick integer NOT NULL,
                                sleepiness real NOT NULL,
                                max_sleepiness real NOT NULL,
                                base_sleepiness real NOT NULL,
                                sleepiness_rate real NOT NULL,
                                base_sleepiness_rate real NOT NULL,
                                sleepiness_recovery_rate real NOT NULL,
                                base_sleepiness_recovery_rate real NOT NULL,
                                asleep integer NOT NULL,
                                lights integer NOT NULL,
                                dna text NOT NULL,
                                timestamp text NOT NULL,
                                mute integer NOT NULL,
                                age_tracker integer NOT NULL,
                                avg_food real NOT NULL,
                                avg_happiness real NOT NULL,
                                avg_cleanliness real NOT NULL,
                                avg_sleepiness real NOT NULL,
                                avg_sick real NOT NULL,
                                tot_mins real NOT NULL,
                                FOREIGN KEY (player_id) REFERENCES players (id)
                            );"""
    execute_sql_command(connection, players_table_sql)
    execute_sql_command(connection, current_pets_table_sql)
    execute_sql_command(connection, pets_table_sql)
    execute_sql_command(connection, eggs_table_sql)


# Helper function to execute a sql command given a connection and command string
def execute_sql_command(connection, sql_command):
    try:
        cursor = connection.cursor()
        cursor.execute(sql_command)
    except Error as er:
        print(er)

