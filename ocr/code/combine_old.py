"""
This is used to combine the results of ocropus recognition into a single file.
"""
import os
import subprocess
import argparse


def main():
    base = "preprocessed"
    for p in range(0, 700):
        page = "%.4d" % (p)
        filename = "result/%s.txt" % (page)

        cmd = "touch %s" % (filename)
        subprocess.call(cmd, shell=True)

        cmd = "echo [%s] > %s " % (page, filename)
        subprocess.call(cmd, shell=True)

        cmd = "cat %s/%s/??????.txt >> %s " % (base, page, filename)
        subprocess.call(cmd, shell=True)

if __name__ == '__main__':
    main()



