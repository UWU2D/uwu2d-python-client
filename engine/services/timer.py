from timeit import default_timer as timer


class Timer:

    def __init__(self, timeout_in_ms):
        self.timeout_in_ms = timeout_in_ms
        self.last_check = None

    def is_elapsed(self):
        if self.last_check is None:
            return True

        return (timer() - self.last_check) * 1000 >= self.timeout_in_ms

    def reset(self):
        self.last_check = timer()
