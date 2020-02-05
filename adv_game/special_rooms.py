import pandas as pd
import json
import requests
from utils import *

df = pd.read_json("https://raw.githubusercontent.com/build-week-pt2/CS-Build-Week-2/matt/room_info.json").T


def map_to_room_id(start_id, end_id):
    short_path = bfs(str(start_id), str(end_id))
    directed_path = []
    for i in range(len(short_path) + 1):
        if i + 1 < len(short_path):
            direction = reverse_dict(
                traversial_graph[str(short_path[i])])[short_path[i+1]]
            directed_path.append(direction)
    return dict(zip(short_path, directed_path))
