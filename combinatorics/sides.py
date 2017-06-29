import sys
import numpy as np
import subprocess

def intro(f):
    """ Write intro. 

    Parameters
    ----------
    f : <file>
    """
    f.write("// FILE BUILD BY %s\n"%sys.argv[0])

def start(f):
    """ start include commands and main definition.

    Parameters
    ----------
    f : <file>
    """
    f.write("#include <stdio.h>\n")
    f.write("#include <stdlib.h>\n\n")
    f.write("#include <map>\n\n")
    f.write("int main(int argc, char** argv) {\n")

def if_for_faces(n, k, face, f):
    """ Writes if and for in order to check number of faces.

    Parameters
    ----------
    n : int
    k : int
    f : <file>
    """
    faces = "  // check if element shows only %d faces\n"%(face)

    f.write(faces)

def end(f):
    """ end main function.

    Parameters
    ----------
    f : <file>
    """
    f.write("return 0;\n}\n")

def init_map(f):
    """ Inits map object.

    Parameters
    ----------
    f : <file>
    """
    f.write("  std::map<int, int> ARR;\n")

def increment_map(k, f):
    """ increment map on element k.
    Parameters
    ----------
    f : <file>
    """
    line = "  ARR["
    line += k*"i"
    line += "]++;\n"

    f.write(line)

def map_size(face, f):
    """ Check if map size is equal to face.

    Parameters
    ----------
    face : int
    f : <file>
    """
    line = "  if (ARR.size() == %d)\n" %(face)
    line += "   face++;\n"

    f.write(line)

def int_n(n, f, name="n"):
    """ Writes an int declaration.

    Parameters
    ----------
    n : int
    f : <file>
    """
    dec = "int %s = "%(name)
    dec += str(n)
    dec += ";\n"

    f.write(dec)

def printf(k, f):
    """ Writes a printf.

    Parameters
    ----------
    k : int
    f : <file>
    """
    line = "  "
    line += "printf(\""
    line += k*"%d "
    line += "\\n\""
    for kk in range(1, k+1):
        line += ","
        line += kk*"i"
    line += ");\n"

    f.write(line)

def begin_logic(f):
    """ {
    Parameters
    ----------
    f : <file>
    """
    f.write("  {\n")

def end_logic(f):
    """ }
    Parameters
    ----------
    f : <file>
    """
    f.write("  }\n")


def for_loop(k, f):
    """ Writes a for loop.

    Parameters
    ----------
    k : int
    f : <file>
    """
    loop = " "
    loop += "for (int "
    loop += k*"i"
    loop += "=1; "
    loop += k*"i"
    loop += " <= n; "
    loop += k*"i"
    loop += "++)\n"

    f.write(loop)     

def result(face, f):
    """ printf result.

    Parameters
    ----------
    face : int
    f : <file>
    """
    line = "printf(\"Number of elements with %d faces is " %(face)
    line += "%d from %d\\n\", face, total);\n"

    f.write(line)

def main(n, k, face):
    f = open("dice.cpp", "w")

    intro(f)
    start(f)
    int_n(n, f)
    int_n(0, f, name="face")
    int_n(0, f, name="total")
    for kk in range(1, k+1):
        for_loop(kk, f)
    begin_logic(f)
    f.write("  total++;")
    printf(k, f)
    init_map(f)
    if_for_faces(n, k, face, f)
    for kk in range(1, k+1):
        increment_map(kk, f)
    map_size(face, f)
    end_logic(f)
    result(face, f)
    end(f)

    f.close()

if __name__ == '__main__':
    main(n=6, k=int(sys.argv[1]), face=2)
    subprocess.call(["g++", "dice.cpp"])
    subprocess.call(["./a.out"])

