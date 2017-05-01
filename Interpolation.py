import sys
import os
from random import randint

class Interpolation:
    def __init__(self, path):
        self.fd = open(path, 'rb')
        self.stat = os.stat(path)
        print("opened: {}".format(self.fd))

    def size(self):
        return self.stat.st_size

    def value_for_range(self, range_start, range_size):
        return randint(0, 9000)
