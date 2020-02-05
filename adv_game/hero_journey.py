from player import Player
from utils import Queue
from special_rooms import map_to_destination, map_to_room_id
import time

hero = Player()
new_name = "TheLessonHere"
time.sleep(2)

# hero.treasure_hunt(1000, 9)
# hero.treasure_hunt(1000, 2)
# hero.destination_travel("Pirate Ry's")
# hero.change_name(new_name)
# hero.destination_travel("Wishing Well")
# hero.examine("well")
# hero.destination_travel_id(133)
hero.get_last_proof()