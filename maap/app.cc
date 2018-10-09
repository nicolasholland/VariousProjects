#include <iostream>
#include <fstream>
#include <string>
#include <cmath>
#include <stdlib.h>
#include <time.h>
#include "poly.pb.h"

double evaluate(polynom::Polynom data, int input_ind) {
	double retval = data.coefficient(0);
	for (int ind = 1; ind < data.coefficient_size(); ind++)
		retval += data.inputs(input_ind) * pow(data.coefficient(ind), ind + 1);

	return retval;
}

void create_some_input(void) {
	srand (time(NULL));
	polynom::Polynom poly;

	for (int ind = 0; ind < 4; ind++) {
		float val = rand() % 2000;
		val = val/1000. - 1;
		poly.add_coefficient(val);
	}

	for (int ind = 0; ind < 100; ind++) {
		float val = rand() % 2000;
		val = val/100. - 10;
		poly.add_inputs(val);
	}

	std::string buffer;
	poly.SerializeToString(&buffer);
	std::ofstream outfile ("file.mf", std::ios::binary);
	outfile << buffer << std::endl;
	outfile.close();
}

int main(int argc, char** argv) {
	std::cout << "Messy Application Output" << std::endl;

	polynom::Polynom data;
	std::fstream input("input/file.mf", std::ios::in | std::ios::binary);
	data.ParseFromIstream(&input);

	for (int ind = 0; ind < data.inputs_size(); ind++)
		std::cout << evaluate(data, ind) << std::endl;
}
