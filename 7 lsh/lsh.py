import numpy as np
import random


class LSHashTable:
    def __init__(self, number, dimension, base):
        '''
        Input: `number`: number of hash tables (l)
               `dimension`: dimension of each feature (d)
               `base`: size of each base (k)
        '''
        # Initialize hash tables
        self.tables = []
        for i in range(number):
            self.tables.append({})
        
        # Generate hash functions
        self.bases = []
        for i in range(number):
            self.bases.append(random.sample(range(dimension * 2), base))
    

    def hash(self, feature, base):
        '''
        Hashing the input feature vector.

        Input: `feature`: Input feature vector
               `base`: Base used in the hash function
        Output: number of bucket for the feature
        '''
        bucket = []
        for i in range(1, len(feature) + 1):
            for x in filter(lambda p: (i - 1) * 2 < p <= i * 2, base):
                if x - (i - 1) * 2 <= feature[i - 1]:
                    bucket.append('1')
                else:
                    bucket.append('0')
        return int(''.join(bucket), 2)


    def insert(self, feature, label):
        '''
        Insert a feature into the LSHashTable.

        Input: `feature`: Input feature vector
               `label`: Label corresponding to the feature
        '''
        for i, table in enumerate(self.tables):
            bucket = self.hash(feature, self.bases[i])
            if bucket not in table:
                table[bucket] = {
                    'label': label,
                    'feature': feature
                }


    def search(self, feature):
        '''
        Search a feature in the LSHashTable.

        Input: `feature`: Input feature vector
        Output: `label`: Label predicted of the feature
        '''
        dist, label = float('inf'), None
        for i, table in enumerate(self.tables):
            bucket = self.hash(feature, self.bases[i])
            item = table[bucket]
            d = np.linalg.norm(item['feature'] - feature)
            if d < dist:
                dist = d
                label = item['label']
        return label
