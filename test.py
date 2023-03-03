import random
import sys
from map import Map

if __name__ == "__main__":
    seed = random.randrange(sys.maxsize)
    print("Seed was:", seed)
    lh = Map(seed)
    print(str(lh))

