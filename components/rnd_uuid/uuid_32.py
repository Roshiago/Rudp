import time

class RndSeqUnique:
    __instance = None
    """
    source : https://github.com/preshing/RandomSequence/blob/master/randomsequence.h
    descr: 
        generate random value in 32 bits
    """

    @staticmethod
    def permuteQRP(x):
        prime = 4294967291
        if (x >= prime):
            return x
        
        reside = (x * x) % prime
        return reside if x <= prime / 2 else prime - reside 

    def __init__(self, seed, seedOffset):
        self.index = RndSeqUnique.permuteQRP(RndSeqUnique.permuteQRP(seed) + 0x682f0161)
        self.offset = RndSeqUnique.permuteQRP(RndSeqUnique.permuteQRP(seedOffset) + 0x46790905)
    
    def next(self):
        first_permutate = RndSeqUnique.permuteQRP(self.index)
        second_permutate = (first_permutate + self.offset) ^ 0x5bf03635
        if second_permutate > 2**32:
            amount = round(second_permutate / 2**32)
            second_permutate -= amount*(2**32)
        third_permutate = RndSeqUnique.permuteQRP(second_permutate)
        return third_permutate#RndSeqUnique.permuteQRP((RndSeqUnique.permuteQRP(self.index) + self.offset) ^ 0x5bf03635)
    
    @classmethod
    def getInstance(cls):
        if not cls.__instance:
            now = time.time()
            cls.__instance = RndSeqUnique(int(now), int(now + 1))
        return cls.__instance

uuid4 = RndSeqUnique.getInstance()