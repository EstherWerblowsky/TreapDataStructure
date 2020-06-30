##this file is Professor Alan Broder's code file

import random

# setup a list of random 64-bit values to be used by BitHash
__bits = [0] * (64*1024)
__rnd = random.Random()

# seed the generator to produce repeatable results
__rnd.seed("BitHash random numbers") 

# fill the list
for i in range(64*1024): 
    __bits[i] = __rnd.getrandbits(64)

def BitHash(s, h = 0):
    for c in s: 
        h  = (((h << 1) | (h >> 63)) ^ __bits[ord(c)]) 
        h &= 0xffffffffffffffff
    return h


def __main():
    while True:
        s = input("String to hash? ")
        print("%016x" % BitHash(s))
    
                        
if __name__ == '__main__':
    __main()       
                
                       

