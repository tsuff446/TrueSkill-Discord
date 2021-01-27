import time
import bisect

#maintains a sorted queue based on time of expiry
class PlayerQueue():
    def __init__(self):
        #queue will contain (leave_time, player) tuples
        self.queue = []
    
    #adds player to priority queue, expiry is time player
    #wants to be in queue in minutes
    def enqueue_player(self, player, expiry):
        leave_time = time.time() + expiry*60
        bisect.insort_left(self.queue, (leave_time, player))

    #removes players from queue if leave_time is reached
    def prune_queue(self):
        currTime = time.time()
        while self.queue[0][0] < currTime:
            self.queue.pop(0)

    #clears queue
    def clear_queue(self):
        self.queue.clear()