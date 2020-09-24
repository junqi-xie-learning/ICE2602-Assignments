# SJTU EE208

from Bitarray import Bitarray
import math
import copy
import random


# modified from GeneralHashFunctions.BKDRHash
def BKDRHash(key, seed):
    hash = 0
    for i in range(len(key)):
        hash = (hash * seed) + ord(key[i])
    return hash


class BloomFilter:
    def __init__(self, n, f):
        self.bitarray = Bitarray(20 * n) # Randomly-chosen number
        self.hash_func = f

        self.seeds = set()
        for i in range(14): # Closest to `math.log(2) * 20`
            index = random.randint(0, 2 ** 32)
            self.seeds.add(index)
    
    def add(self, keyword):
        for seed in self.seeds:
            index = self.hash_func(keyword, seed) % self.bitarray.size
            self.bitarray.set(index)
    
    def find(self, keyword):
        for seed in self.seeds:
            index = self.hash_func(keyword, seed) % self.bitarray.size
            if self.bitarray.get(index):
                return False
        return True

def get_random_string():
    import random
    return ''.join(random.sample([chr(i) for i in range(48, 123)], 6))


size = 10 ** 6
tocrawl = [get_random_string() for i in range(size)]
tocrawl_copy = copy.deepcopy(tocrawl)

def test_hashtable(tocrawl):
    crawled = set()
    result = []

    while tocrawl:
        page = tocrawl.pop()
        if len(tocrawl) >= size // 2:
            crawled.add(page)
        else:
            result.append(page in crawled)
    return result

def test_bloomfilter(tocrawl):
    crawled = BloomFilter(size // 2, BKDRHash)
    result = []

    while tocrawl:
        page = tocrawl.pop()
        if len(tocrawl) >= size // 2:
            crawled.add(page)
        else:
            result.append(crawled.find(page))
    return result

reference = test_hashtable(tocrawl)
result = test_bloomfilter(tocrawl_copy)

count = 0
for i in range(len(reference)):
    if reference[i] != result[i]:
        count += 1

print("{:.6f}".format(count / len(reference)))