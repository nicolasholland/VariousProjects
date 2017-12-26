hello.o:
	gcc src_hello.c -c
	ar -cvq libhello.a *.o
	rm *.o
	gcc main.c -L./ -lhello
