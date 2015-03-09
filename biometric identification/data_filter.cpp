#include <iostream>
#include <cmath>
#include <sstream>
#include <string>
#include <fstream>
#include <string.h>
#include <cstdlib>

using namespace std;

struct reading{
	double ur;
	double ut;
	double ul;
};

int main(int argc, char** argv)
{
	std::ifstream infile(argv[1]);
	har c_line[100];
	while (std::getline(infile, line))
	{
		strcpy(c_line,line.c_str());
		if(c_line[0] != 'U')
			continue;
		tok1 = strtok(c_line," ");
		strtok(NULL," "); // used to discard the '=' token
		tok2 = strtok(NULL," ");
		//cout << atof(tok2) <<endl;
		cm = atof(tok2);
		if(strcmp(tok1,"UR") == 0)
		{

		}
	}
}