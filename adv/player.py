import requests
import json

class Player:
    """
    Player class
    """

    def __init__(self, api_key):
        self.api_key = api_key
        self.current_room = 0
        self.previous_room = 0

    def init_player(self):
        r = requests.get(
            "https://lambda-treasure-hunt.herokuapp.com/api/adv/init/",
            headers = {"Authorization": self.api_key}
            )

        self.current_room = r.json()['room_id']

        return r.json()

    def move(self, treasure_map, direction):
        # Set current_room as previous room
        self.previous_room = self.current_room
        
        # Move
        if treasure_map[self.current_room][direction] == "?":
            r = requests.post(
                "https://lambda-treasure-hunt.herokuapp.com/api/adv/move/",
                data = json.dumps({"direction": direction}),
                headers = {
                    "Authorization": self.api_key,
                    "Content-Type": "application/json"
                }
            )
        else:
            r = requests.post(
                "https://lambda-treasure-hunt.herokuapp.com/api/adv/move/",
                data = json.dumps({"direction": direction}, 
                                  {"next_room_id": treasure_map[self.current_room][direction]}),
                headers = {
                    "Authorization": self.api_key,
                    "Content-Type": "application/json"
                }
            )

        # Set new room as current room
        self.current_room = r.json()['room_id']

        return r.json()