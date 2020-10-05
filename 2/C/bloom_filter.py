# SJTU EE208

from Bitarray import Bitarray
import random
import copy


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
        self.bitarray = Bitarray(20 * n)  # Randomly-chosen number
        self.hash_func = f

        # Generate seeds to obtain different hash functions
        self.seeds = set()
        for i in range(14):  # Closest to `math.log(2) * 20`
            seed = random.randint(0, 2 ** 20)
            self.seeds.add(seed)
    
    def add(self, keyword):
        '''
        Add `keyword` into the Bitarray.

        Input: `keyword`: keyword to be added
        Output: None
        '''
        for seed in self.seeds:
            index = self.hash_func(keyword, seed) % self.bitarray.size
            self.bitarray.set(index)  # Mark all the corresponding positions to `1`.
    
    def find(self, keyword):
        '''
        Determine if `keyword` is in the Bitarray.

        Input: `keyword`: keyword to be searched
        Output: a boolean constant indicating the result
        '''
        for seed in self.seeds:
            index = self.hash_func(keyword, seed) % self.bitarray.size
            if self.bitarray.get(index) == 0:
                return False  # If any of the positions is `0`, `keyword` is not in the BloomFilter.
        return True  # Otherwise, it's likely to be in the BloomFilter.


# Test BloomFilter
def get_random_string():
    return ''.join(random.sample([chr(i) for i in range(48, 123)], 6))


def test_hashset(tocrawl):
    '''
    Split `tocrawl` in halves. Store the first half in the set, and find strings in the second half.
    Use `set` as the set. Intended to be used as a reference.

    Input: `tocrawl`: list of words to be tested
    Output: search result of the second half
    '''
    size = len(tocrawl)
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
    '''
    Split `tocrawl` in halves. Store the first half in the set, and find strings in the second half.
    Use `BloomFilter` as the set.

    Input: `tocrawl`: list of words to be tested
    Output: search result of the second half
    '''
    size = len(tocrawl)
    crawled = BloomFilter(size // 2, BKDRHash)
    result = []

    while tocrawl:
        page = tocrawl.pop()
        if len(tocrawl) >= size // 2:
            crawled.add(page)
        else:
            result.append(crawled.find(page))
    return result


if __name__ == '__main__':
    tocrawl = [get_random_string() for i in range(10 ** 6)]
    tocrawl_copy = copy.deepcopy(tocrawl)

    reference = test_hashset(tocrawl)
    result = test_bloomfilter(tocrawl_copy)

    # Count the total number of false positives
    count = 0
    for i in range(len(reference)):
        if reference[i] != result[i]:
            count += 1

    # Calculate the false positive rate
    print("{:.6f}".format(count / len(reference)))