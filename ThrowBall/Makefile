# Specify compiler and flags
CPP = g++
CPPFLAGS = -Wall -g -O3 -fopenmp
# Normal object files to be created
OBJECTS = main.o simulate.o
# Program name
PROGRAM = opt
# Include-file location
INCLUDES = -I/usr/local/include
# Library location and name
LIBS = -lm 
MYLIBS = -ladept $(LIBS)

# Rule to build the programm
$(PROGRAM): $(OBJECTS) 
	$(CPP) $(CPPFLAGS) $(OBJECTS) $(MYLIBS) -o $(PROGRAM)
%.o: %.cpp *.h /usr/local/include/adept.h
	$(CPP) $(CPFLAGS) $(INCLUDES) -c $<
clean:
	rm -f *.o $(PROGRAM)
