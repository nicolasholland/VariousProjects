import sys
from difflib import SequenceMatcher

def load(filename):
    with open(filename, 'r') as tmp:
        retval = tmp.readlines()
    return ''.join(retval)

loss = lambda val, gt : SequenceMatcher(None, val, gt).ratio()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Use with %s <filename> <filename>" % (sys.argv[0]))
    else:
        print(loss(load(sys.argv[1]), load(sys.argv[2])))
