# Specify compiler and flags
CPP = g++
CPPFLAGS = -w -g -O3 -fopenmp
# Normal object files to be created
OBJECTS = main.o Visualize.o Needle.o
# Program name
PROGRAM = a.out
# Include-file location
INCLUDES = -I/usr/local/include
# Library location and name
LIBS = -lm 
MYLIBS = -lSDL2 $(LIBS)

# Rule to build the programm
$(PROGRAM): $(OBJECTS) 
	$(CPP) $(CPPFLAGS) $(OBJECTS) $(MYLIBS) -o $(PROGRAM)
%.o: %.cpp *.h
	$(CPP) $(CPFLAGS) $(INCLUDES) -c $<
clean:
	rm -f *.o $(PROGRAM)
