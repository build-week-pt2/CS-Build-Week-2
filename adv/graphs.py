from util import Stack, Queue

class Map:
    """
    Represent Graph as a dict with `room_id` as the key, 
    and a dict with valid directions to move and their neighbor's
    `room_id` as the value

    {
        0: {'n': '?', 's': 5, 'w': '?', 'e': '?'},
        5: {'n': 0, 's': '?', 'e': '?'}
    }
    """

    def __init__(self):
        self.rooms = {}

    # Add current `room_id` and valid directions with `?` as a place-holder
    def add_current_room(self, json):
        room_id = json['room_id']
        directions = json['exits']

        # Add room_id and empty dict to rooms
        self.rooms[room_id] = {}

        # Fill in valid directions with `?` as place-holder
        for direction in directions:
            self.rooms[room_id][direction] = "?"

    def random_move(self, player):
        # Get Current Room
        current_room = player.current_room

        # Get possible directions
        unexplored_directions = [direction for direction in self.rooms[current_room] if self.rooms[current_room][direction] == "?"]

        # Return random choice

    # Get a dictionary of neighbors
    def get_neighbor_dict(self, room_id):
        return self.rooms[room_id]

    # # Get a room's neighbors
    # def get_neighbors(self, room_id):
    #     neighbors = []

    #     # Iter through dict and add values
    #     for key in self.rooms[room_id]:
    #         # print(key)
    #         neighbors.append(self.rooms[room_id][key])

    #     return neighbors

    # def find_nearest_unexplored_room(self, player):
    #     """
    #     Basically a breadth-first search
    #     """        
    #     # Create empty queue & enqueue starting room
    #     queue = Queue()
    #     queue.enqueue([player.current_room.id])
        
    #     # Create a new visited set
    #     bfs_visited = set()
        
    #     while queue.size() > 0:
            
    #         # dequeue the current room/path
    #         path = queue.dequeue()
    #         cur_room = path[-1]
            
    #         if cur_room not in bfs_visited:
                
    #             # Check if there is an unexplored exit
    #             if "?" in self.get_neighbors(cur_room):
    #                 # If so, return the path
    #                 return path
                
    #             # Mark as visited
    #             bfs_visited.add(cur_room)
                
    #             # Add it's neighbors
    #             for neighbor in self.get_neighbors(cur_room):
    #                 # Copy to avoid reference error
    #                 new_path = list(path)
    #                 new_path.append(neighbor)
    #                 queue.enqueue(new_path)

    # def find_longest_path(self):
    #     """
    #     Basically a BFS for the longest chain
    #     """
    #     # Create empty queue
    #     queue = Queue()
    #     queue.enqueue([0])
        
    #     max_path = []
        
    #     while queue.size() > 0:
    #         # Get path and current room back
    #         path = queue.dequeue()
    #         cur_room = path[-1]
            
    #         # If the path is longer than max_path_len
    #         if len(path) > len(max_path):
    #             max_path = path
                
    #         # Add the neighbors
    #         for neighbor in self.get_neighbors(cur_room):
    #             new_path = list(path)
    #             new_path.append(neighbor)
    #             queue.enqueue(new_path)
                
    #     return max_path

    # def path_to_directions(self, path):
    #     directions = []

    #     for i in range(len(path) - 1):
    #         # Get current and next room
    #         cur_room, next_room = path[i], path[i+1]

    #         # Iterate through keys, look for entry matching next_room
    #         for key in self.rooms[cur_room]:
    #             if self.rooms[cur_room][key] == next_room:
    #                 directions.append(key)
                    
    #     return directions

class RoomInfo:
    """
    Holds all the information for the rooms we travel to

    {
        0: {'title': 'A Room', 
            'description': 'A Description', 
            'coordinates': '(60, 60)', 
            'cooldown': 100.0, 
            'errors': ['maybe one', 'or two errors'], 
            'messages': ['maybe a message', 'or two']}
    }
    """

    def __init__(self):
        self.info = {}

    def add_room_info(self, room_id, room_response):
        pass