from graphs import Map, RoomInfo
from player import Player
from time import sleep

# Put in your API Key
player = Player("Token 4e558caea9ae35eb8eddc5f9b256faa32804f67b")

# Instantiate our Map and RoomInfo and visited
treasure_map = Map()
visited = ()

# Initialize player in first room
json = player.init_player()

# Add the first room to Map and RoomInfo

# While len(visited) < 500:

    # Make a random move if there are unexplored directions

    # Do a BFS if we hit a dead end