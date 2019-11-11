"""
This is used to combine the results of ocropus recognition into a single file.
"""
import os
import subprocess
import argparse


def main():
    base = "split"
    a_path = os.path.join(base, 'a_rec')
    b_path = os.path.join(base, 'b_rec')
    for p in range(0, 700):
        page = "%.4d" % (p)
        filename = "result/%s.txt" % (page)

        cmd = "touch %s" % (filename)
        subprocess.call(cmd, shell=True)

        cmd = "echo [%s A] > %s " % (page, filename)
        subprocess.call(cmd, shell=True)

        cmd = "cat %s/%s/??????.txt >> %s " % (a_path, page, filename)
        subprocess.call(cmd, shell=True)
        
        cmd = "echo [%s B] >> %s " % (page, filename)
        subprocess.call(cmd, shell=True)

        cmd = "cat %s/%s/??????.txt >> %s " % (b_path, page, filename)
        subprocess.call(cmd, shell=True)

if __name__ == '__main__':
    main()



