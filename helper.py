class RangeOrder:
    def __init__(self, start, stop):
        self.start = start
        self.stop = stop

    def __iter__(self):
        return self

    def __next__(self):
        if self.start > self.stop:
            if self.start <= self.stop:
                raise StopIteration
            self.start -= 1
            return self.start + 1
        elif self.start < self.stop:
            if self.start >= self.stop:
                raise StopIteration
            self.start += 1
            return self.start - 1
        else:
            raise StopIteration




