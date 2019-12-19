import threading

class ThreadFuzz(threading.Thread):
    def __init__(self):
        self.is_fuzzing = False

