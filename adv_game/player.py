import requests
import json
import time
from time import sleep
import random
import sys
import hashlib
import pprint
pp = pprint.PrettyPrinter(indent=4)

from special_rooms import *

#my_token = sys.argv[1]
my_token = "Token 9a118462c7930cbb7786d91ceeedf67f3d76c643"
base_url = "https://lambda-treasure-hunt.herokuapp.com/api/adv/"
base_header = {
    "Authorization": my_token,
    "Content-Type": "application/json"
}

r = requests.get("https://raw.githubusercontent.com/build-week-pt2"
                 "/CS-Build-Week-2/matt/room_info.json")
room_information = dict(r.json())

r = requests.get("https://raw.githubusercontent.com/build-week-pt2"
                 "/CS-Build-Week-2/matt/room_map.json")
traversial_graph = dict(r.json())


class Player:


    def __init__(self):
        self.token = my_token
        r = requests.get(
            base_url + "init/",
            headers = {"Authorization": self.token}
        )
        response = dict(r.json())
        print(f"Waiting {response['cooldown']} seconds for cooldown.")
        sleep(response['cooldown'])
        self.current_rm = str(response['room_id'])
        pp.pprint(response)


    def move(self, direction, wise_travel = None):
        next_room_id = traversial_graph[self.current_rm][direction]
        condition_1 = room_information[next_room_id]['elevation'] > 0
        condition_2 = 'fly' in self.status(show = False)['abilities']
        if condition_1 and condition_2:
            r = requests.post(
                base_url + "fly/",
                data = json.dumps({"direction": direction}),
                headers = base_header
            )
        else:
            if wise_travel == None:
                r = requests.post(
                    base_url + "move/",
                    data = json.dumps({"direction": direction}),
                    headers = base_header
                )
            else:
                r = requests.post(
                    base_url + "move/",
                    data = json.dumps({
                        "direction": direction,
                        "next_room_id": wise_travel
                        }),
                    headers = base_header
                )
        response = dict(r.json())
        print(f"Waiting {response['cooldown']} seconds for cooldown.")
        sleep(response['cooldown'])
        self.current_rm = str(response['room_id'])
        pp.pprint(response)
        return response


    def pickup(self, item):
        r = requests.post(
            base_url + "take/",
            data = json.dumps({"name": item}),
            headers = base_header
        )
        response = dict(r.json())
        print(f"Waiting {response['cooldown']} seconds for cooldown.")
        sleep(response['cooldown'])
        pp.pprint(response)
        return response


    def drop(self, item):
        r = requests.post(
            base_url + "drop/",
            data = json.dumps({"name": item}),
            headers = base_header
        )
        response = dict(r.json())
        pp.pprint(response)
        return response


    def sell(self, item):
        r = requests.post(
            base_url + "sell/",
            data = json.dumps({
                "name": item,
                "confirm": "yes"
            }),
            headers = base_header
        )
        response = dict(r.json())
        print(f"Waiting {response['cooldown']} seconds for cooldown.")
        sleep(response['cooldown'])
        pp.pprint(response)
        return response


    def status(self, show = True):
        r = requests.post(
            base_url + "status/",
            headers = base_header
        )
        response = dict(r.json())
        print(f"Waiting {response['cooldown']} seconds for cooldown.")
        sleep(response['cooldown'])
        if show == True:
            pp.pprint(response)
        return response


    def examine(self, name):
        r = requests.post(
            base_url + "examine/",
            data = json.dumps({"name": name}),
            headers = base_header
        )
        response = r.text
        pp.pprint(response)
        return response


    def examine_well(self):
        r = requests.post(
            base_url + "examine/",
            data = json.dumps({"name": "well"}),
            headers = base_header
        )
        response = r.text
        pp.pprint(response)
        with open("binary_file.txt", 'w') as f:
            f.write(response)
            f.close()
        return response


    def wear(self, item):
        r = requests.post(
            base_url + "wear/",
            data = json.dumps({"name": [item]}),
            headers = base_header
        )
        response = dict(r.json())
        pp.pprint(response)
        return response


    def undress(self, item):
        r = requests.post(
            base_url + "undress/",
            data = json.dumps({"name": [item]}),
            headers = base_header
        )
        response = dict(r.json())
        pp.pprint(response)
        return response


    def change_name(self, new_name):
        r = requests.post(
            base_url + "change_name/",
            data = json.dumps({
                "name": [new_name],
                "confirm": "aye"
            }),
            headers = base_header
        )
        response = dict(r.json())
        pp.pprint(response)
        return response


    def pray(self):
        r = requests.post(
            base_url + "pray/",
            headers = base_header
        )
        response = dict(r.json())
        print(f"Waiting {response['cooldown']} seconds for cooldown.")
        sleep(response['cooldown'])
        pp.pprint(response)
        return response


    def dash(self, direction, num_rooms, next_ids):
        r = requests.post(
            base_url + "dash/",
            data = json.dumps({
                "direction": direction,
                "num_rooms": str(num_rooms),
                "next_room_ids": ','.join(next_ids)
            }),
            headers = base_header
        )
        response = dict(r.json())
        print(f"Waiting {response['cooldown']} seconds for cooldown.")
        sleep(response['cooldown'])
        pp.pprint(response)
        self.current_rm = str(response['room_id'])
        return response


    def get_proof(self):
        r = requests.get(
            base_url[:-4] + "bc/last_proof/",
            headers = base_header
        )
        response = dict(r.json())
        print(f"Waiting {response['cooldown']} seconds for cooldown.")
        sleep(response['cooldown'])
        pp.pprint(response)
        return response


    def valid_proof(self, last_proof, guess_proof, difficulty):
        guess = f"{last_proof}{guess_proof}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:difficulty] == "0" * difficulty


    def proof_of_work(self):
        # Get the vars we need for valid proof
        proof_info = self.get_proof()
        last_proof = proof_info['proof']
        difficulty = proof_info['difficulty']
        guess_proof = 23
        while self.valid_proof(last_proof, guess_proof, difficulty) is False:
            guess_proof += 13
        return guess_proof


    def mine(self):
        while True:
            # Get your proof
            proof = self.proof_of_work()
            r = requests.post(
                base_url[:-4] + "bc/mine/",
                data = json.dumps({"proof": proof}),
                headers = base_header
            )
            response = dict(r.json())
            pp.pprint(response)
            cooldown = response['cooldown']
            time.sleep(cooldown)


    def get_balance(self):
        r = requests.get(
            base_url[:-4] + "bc/get_balance/",
            headers = {
                "Authorization": self.token,
                "Content-Type": "application/json"
            }
        )
        response = dict(r.json())
        print(f"Waiting {response['cooldown']} seconds for cooldown.")
        sleep(response['cooldown'])
        pp.pprint(response)
        return response


    def destination_travel_id(self, destination):
        destination_map = map_to_room_id(int(self.current_rm), destination)
        cur_title = room_information[self.current_rm]["title"]

        while cur_title != destination:
            direction = destination_map[self.current_rm]
            wise_id = traversial_graph[self.current_rm][direction]
            self.move(direction, wise_id)


    def go_fast(self, destination):
        # While the current room isn't the destination
        while self.current_rm != str(destination):
            # Find the shortest path of room IDs
            short_path = bfs(self.current_rm, str(destination))

            # Find the directions we need to go
            directed_path = []
            for i in range(len(short_path) + 1):
                if i + 1 < len(short_path):
                    direction = reverse_dict(
                        traversial_graph[str(short_path[i])])[short_path[i+1]]
                    directed_path.append((direction, short_path[i]))
            # directed path [(exit_direction, room_id), ...]

            i = 0
            move = directed_path[0][0]
            dash_path = []
            while directed_path[i][0] == move and len(directed_path) > 2:
                dash_path.append(directed_path[i][1])
                i += 1
            if len(dash_path) > 2:
                print(f"dash_path: {dash_path}")
                self.dash(direction = move,
                          num_rooms = len(dash_path) - 1,
                          next_ids = dash_path[1:])
            elif len(directed_path) == 1:
                self.move(direction = directed_path[0][0],
                          wise_travel = short_path[-1])
            else:
                self.move(direction = directed_path[0][0],
                          wise_travel = directed_path[1][1])
        return


    def treasure_hunt(self, threshhold):
        # while gold under threshhold
        status = self.status(show = False)
        while status['gold'] < threshhold:
            #while encumbrance < strength
            while status['encumbrance'] < status['strength'] - 1:
                # pick a random direction
                possible = traversial_graph[self.current_rm].keys()
                rand_direction = random.choice(list(possible))
                wise_id = traversial_graph[self.current_rm][rand_direction]
                # wise travel
                movement = self.move(rand_direction, wise_id)
                status = self.status(show = False)
                if len(movement['items']) != 0:
                    # pick it up
                    for i in range(len(movement['items'])):
                        if status['encumbrance'] < status['strength'] - 1:
                            self.pickup(movement['items'][i])
                            status = self.status()
            #go to shop and sell treasure
            self.destination_travel_id(1)
            status = self.status(show = False)
            for item in status['inventory']:
                self.sell(item)
                status = self.status()
