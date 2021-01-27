import time
import bisect

#maintains a sorted queue based on time of expiry
class PlayerQueue():
    def __init__(self):
        #queue will contain (leave_time, player) tuples
        self._queue = []
    
    #adds player to priority queue, expiry is time player
    #wants to be in queue in minutes
    def enqueue_player(self, player, expiry):
        leave_time = time.time() + expiry*60
        self.binary_insert((leave_time, player))
    
    #repurposed from python standard library
    def binary_insert(self, tup):
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
        while self._queue[0][0] < currTime:
            self._queue.pop(0)

    #clears queue
    def clear_queue(self):
        self._queue.clear()
