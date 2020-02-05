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

r = requests.get("https://raw.githubusercontent.com/build-week-pt2/CS-Build-Week-2/matt/room_info.json")
room_information = dict(r.json())
r = requests.get("https://raw.githubusercontent.com/build-week-pt2/CS-Build-Week-2/matt/room_map.json")
traversial_graph = dict(r.json())


class Player:


    def __init__(self):
        self.token = my_token
        r = requests.get(
            base_url + "init/",
            headers = {"Authorization": self.token}
        )
        response = dict(r.json())
        self.current_room_id = response['room_id']
        pp.pprint(response)



    def move(self, direction, wise_travel = None):
        next_room_id = traversial_graph[str(self.current_room_id)][direction]
        condition_1 = room_information[next_room_id]['elevation'] > 0
        condition_2 = 'fly' in self.status()['abilities']
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
        self.current_room_id = response['room_id']
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


    def status(self):
        r = requests.post(
            base_url + "status/",
            headers = base_header
        )
        response = dict(r.json())
        print(f"Waiting {response['cooldown']} seconds for cooldown.")
        sleep(response['cooldown'])
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
        pp.pprint(response)
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


    def mine(self):
        proof_info = self.get_proof()
        last_proof = proof_info['proof']
        difficulty = proof_info['difficulty']
        leading_zeros = '0' * difficulty
        # Does hash(last_proof, proof) contain N leading zeroes
        # where N is the current difficulty level?
        proof = 0
        guess = f'{last_proof}{proof}'.encode()
        while guess.decode()[:difficulty] != leading_zeros:
            guess = f'{last_proof}{proof}'.encode()
            guess_hash = hashlib.sha256(guess).hexdigest()
            print(guess.decode()[:difficulty])
            print(leading_zeros)
            proof += 1
        new_proof = proof
        r = requests.post(
            base_url[:-4] + "bc/mine/",
            data = json.dumps({"proof": new_proof}),
            headers = base_header
        )
        response = dict(r.json())
        pp.pprint(response)
        return response


    def destination_travel_id(self, destination):
        destination_map = map_to_room_id(self.current_room_id, destination)

        while room_information[str(self.current_room_id)]["title"] != destination:
            direction = destination_map[str(self.current_room_id)]
            wise_travel_id = traversial_graph[str(self.current_room_id)][direction]
            self.move(direction, wise_travel_id)


    def treasure_hunt(self, threshhold):
        # while gold under threshhold
        status = self.status()
        while status['gold'] < threshhold:
            #while encumbrance < strength
            while status['encumbrance'] < status['strength'] - 1:
                # pick a random direction
                rand_direction = random.choice(list(traversial_graph[str(self.current_room_id)].keys()))
                wise_travel_id = traversial_graph[str(self.current_room_id)][rand_direction]
                # wise travel
                movement = self.move(rand_direction, wise_travel_id)
                status = self.status()
                # if item treasure
                if len(movement['items']) != 0:
                    # pick it up
                    for i in range(len(movement['items'])):
                        if status['encumbrance'] < status['strength'] - 1:
                            self.pickup(movement['items'][i])
                            status = self.status()
            #go to shop and sell treasure
            self.destination_travel('Shop')
            status = self.status()
            for item in self.status()['inventory']:
                self.sell(item)
                status = self.status()
