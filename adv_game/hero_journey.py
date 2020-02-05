import sys
import os
from player import Player
from utils import Queue
from special_rooms import map_to_destination, map_to_room_id
import time
import subprocess

hero = Player()
new_name = "TheLessonHere"
mining_room = 133
clue = None
time.sleep(2)

if hero.status()['name'] == [new_name]:
    print("Acquiring new name.")
    hero.treasure_hunt(1000, 9)
    hero.treasure_hunt(1000, 2)
    hero.destination_travel("Pirate Ry's")
    hero.change_name(new_name)
hero.destination_travel("Wishing Well")
hero.examine_well()
subprocess.run(["python", "handle_bin.py"], shell=False)
subprocess.run(["python", "ls8.py secret.ls8"], shell=False)
with open('clue.txt', 'r') as f:
    for line in f:
        clue = line[:3]
if clue[0] == " ":
    mining_room = clue[:2]
    print(F"Clue 2 digits {mining_room}")
elif clue[1] == " ":
    mining_room = clue[:1]
    print(F"Clue 1 digit {mining_room}")
else:
    mining_room = clue
    print(F"Clue 3 digits {mining_room}")
mining_room = int(mining_room)
hero.destination_travel_id(mining_room)
hero.mine()
