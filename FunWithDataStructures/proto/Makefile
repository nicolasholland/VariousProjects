SRC_DIR=.
DST_DIR=${SRC_DIR}
INCLUDE=${HOME}/anaconda3/include/
LIBS=${HOME}/anaconda3/lib/

python:
	protoc -I=${SRC_DIR} --python_out=${DST_DIR} ${SRC_DIR}/poly.proto
	python test.py

cpp:
	protoc -I=${SRC_DIR} --cpp_out=${DST_DIR} ${SRC_DIR}/poly.proto
	g++ -c poly.pb.cc -I${INCLUDE}
	g++ -c test.cc -I${INCLUDE}
	g++ test.o poly.pb.o  -I${INCLUDE} -L${LIBS} -lprotobuf -lgtest
	LD_LIBRARY_PATH=${LIBS} ./a.out

clean:
	rm *.out
	rm *.o
	rm *pb*

