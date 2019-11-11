"""
I use this to create empty gt.txt files as input for ocropus training.
"""
import os
import shutil
import argparse

def touch(path):
    with open(path, 'a'):
        os.utime(path, None)

def main(path):
    sourcefiles = os.listdir(path)

    for filename in sourcefiles:
        newfile = ''.join([os.path.splitext(filename)[0][:-4], '.gt.txt'])
        print(newfile)
        touch(os.path.join(path, newfile))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='path to segfolder')
    parser.add_argument('path')
    args = parser.parse_args()
    main(args.path)
