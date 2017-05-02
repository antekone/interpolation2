import sys
import os
from random import randint
from Log import Log
from math import log

def get_entropy(data):
    alpha = [0] * 256
    for b in data:
        alpha[b] += 1

    e = 0.0
    for i in range(0, 256):
        if alpha[i] > 0:
            prob = 1.0 * alpha[i] / len(data)
            e += prob * log(prob, 2)

    e = -e
    e *= 10000
    return e

def linear_interpolation(offset, left, right):
    offset_left, entropy_left = left
    offset_right, entropy_right = right

    e_left = (offset_right - offset) * entropy_left
    e_right = (offset - offset_left) * entropy_right
    entropy = (e_left + e_right) / (offset_right - offset_left)

    return entropy

class Interpolation:
    def __init__(self, path):
        self.fd = open(path, 'rb')
        self.stat = os.stat(path)

    def size(self):
        return self.stat.st_size

    def value_for_range(self, range_start, range_size):
        if self.fd.tell() != range_start:
            self.fd.seek(range_start)

        Log.put("reading offset %08x / %08x" % (range_start, range_size))

        data = self.fd.read(range_size)
        return get_entropy(data)

