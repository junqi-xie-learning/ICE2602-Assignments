# SJTU EE208

from Bitarray import Bitarray
import random


# Modified from GeneralHashFunctions.BKDRHash to support random seeds
def BKDRHash(key, seed):
    hash = 0
    for i in range(len(key)):
        hash = (hash * seed) + ord(key[i])
    return hash


class BloomFilter:
    def __init__(self, n, f):
        '''
        Input: `n`: number of elements to be stored; \
               `f`: user-defined hash function with 2 parameters: key, seed
        '''
        self.bitarray = Bitarray(20 * n) # Randomly-chosen number
        self.hash_func = f
        self.size = 0

        # Generate seeds to obtain different hash functions
        self.seeds = set()
        for i in range(14): # Closest to `math.log(2) * 20`
            seed = random.randint(0, 128)
            self.seeds.add(seed)
    
    def __len__(self):
        return self.size
    
    def add(self, keyword):
        '''
        Add `keyword` into the Bitarray.

        Input: `keyword`: keyword to be added
        Output: None
        '''
        for seed in self.seeds:
            index = self.hash_func(keyword, seed) % self.bitarray.size
            self.bitarray.set(index) # Mark all the corresponding positions to `1`.
        self.size += 1
    
    def find(self, keyword):
        '''
        Determine if `keyword` is in the Bitarray.

        Input: `keyword`: keyword to be searched
        Output: a boolean constant indicating the result
        '''
        for seed in self.seeds:
            index = self.hash_func(keyword, seed) % self.bitarray.size
            if self.bitarray.get(index) == 0:
                return False # If any of the positions is `0`, `keyword` is not in the BloomFilter.
        return True # Otherwise, it's likely to be in the BloomFilter.
