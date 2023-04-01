from bitmap import BitMap
import hashlib

class BloomFilter:
    def __init__(self, m, k):
        self.m = m
        self.k = k
        self.n = 0
        self.bf = BitMap(self.m)
    
    def getPositions(self, item):
        positions = []
        for i in range(1, self.k+1):
            hash_val = int(hashlib.sha256((item + str(i)).encode()).hexdigest(), 16)
            positions.append(hash_val % self.m)
        return positions
    
    def add(self, item):
        positions = self.getPositions(item)
        for pos in positions:
            self.bf.set(pos)
        self.n += 1
    
    def contains(self, item):
        positions = self.getPositions(item)
        for pos in positions:
            if not self.bf.test(pos):
                return False
        return True
    
    def reset(self):
        self.bf = BitMap(self.m)
        self.n = 0
    
    def __repr__(self):
        num_ones = self.bf.count()
        return f"M = {self.m}, K = {self.k}\nBitMap = {str(self.bf)}\n항목의 수 = {self.n}, 1인 비트수 = {num_ones}"
    
if __name__ == "__main__":
    bf = BloomFilter(53, 3)
    for ch in "AEIOU":
        bf.add(ch)
    print(bf)
    for ch in "ABCDEFGHIJ":
        print(ch, bf.contains(ch))