SRC_DIR=.
DST_DIR=${SRC_DIR}
INCLUDE=${CONDA}/include
LIBS=${CONDA}/lib

all:
	protoc -I=${SRC_DIR} --cpp_out=${DST_DIR} ${SRC_DIR}/poly.proto
	g++ -c poly.pb.cc -I${INCLUDE}
	g++ -c app.cc -I${INCLUDE}
	g++ app.o poly.pb.o  -I${INCLUDE} -L${LIBS} -lprotobuf

run:
	LD_LIBRARY_PATH=${LIBS} ./a.out

clean:
	rm *.out
	rm *.o
	rm *pb*

