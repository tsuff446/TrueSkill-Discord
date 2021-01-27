import time
import math
from src.player import Player

#maintains a sorted queue based on how long player has
class PlayerQueue():
    def __init__(self):
        #queue will contain (leave_time, player) tuples
        self._queue = []
    
    #adds player to priority queue, expiry is time player
    #wants to be in queue in minutes
    def enqueue_player(self, player, expiry):
        leave_time = time.time() + expiry*60
        self._binary_insert((leave_time, player))
    
    #repurposed from python standard library
    def _binary_insert(self, tup):
        leave_time = tup[0]
        low = 0
        high = len(self._queue)
        while low < high:
            mid = (low + high)//2
            if self._queue[mid][0] < leave_time:
                low = mid+1
            else:
                high = mid
        self._queue.insert(low, tup)

    #removes players from queue if leave_time is reached
    def prune_queue(self):
        currTime = time.time()
        while len(self._queue) > 0 and self._queue[0][0] < currTime:
            self._queue.pop(0)

    #clears queue
    def clear_queue(self):
        self._queue.clear()

    #iterates through loop and removes specific player
    def remove_player(self, player):
        for index, tup in enumerate(self._queue):
            if player == tup[1]:
                self._queue.pop(index)
                return True
        return False

    #checks if player in queue
    def check_in_queue(self, player):
        for tup in self._queue:
            if tup[1] == player:
                return True
        return False
    
    #displays queue in str format
    def display_queue(self):
        to_return = []
        for tup in self._queue:
            to_return.append(tup[1].discord_alias + ": " + str(math.ceil((tup[0] - time.time()) / 60)) + " minutes left")
        return '\n'.join(to_return)