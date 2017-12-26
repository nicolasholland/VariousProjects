cdef extern from "hello.h":
  int Hello(char* line)

def c_hello(char* line):
  Hello(line)
