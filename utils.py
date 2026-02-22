from time import perf_counter

class TimePerf:
    def __init__(self, name=None):
            self.name = name
            self.s = 0
        
    def __enter__(self):
        self.s = perf_counter()
    
    def __exit__(self, *_):
        if self.name:
            print(self.name, end=': ')
        print(perf_counter()-self.s)