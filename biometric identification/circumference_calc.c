#include <iostream>
#include <cmath>
#include <sstream>
#include <string>
#include <fstream>
#include <string.h>
#include <cstdlib>

using namespace std;

struct point {
	double x;
	double y;
};
double euclideanDistance(struct point , struct point );

int main(int argc, char** argv)
{

	double cm = 0;
	double w_max = 145.0;
	short started = 0; 
	short done = 0;
	double ul = 0;
	double ur = 0;
	double first = 0;
	double last = 0;
	struct point l_prev,r_prev;
	double left_sum = 0, right_sum = 0;
	double length = 0;
	double circumference = 0;	
	l_prev.x = 0;
    l_prev.y = 0;
    r_prev.x = 0;
    r_prev.y = 0;
	std::string line;
	char *tok1, *tok2;
	std::ifstream infile(argv[1]);
	char c_line[100];
	while (std::getline(infile, line))
	{
		strcpy(c_line,line.c_str());
		tok1 = strtok(c_line," ");
		strtok(NULL," "); // used to discard the '=' token
		tok2 = strtok(NULL," ");
		//cout << atof(tok2) <<endl;
		cm = atof(tok2);
		if(strcmp(tok1,"UR") == 0)
		{
			length+= 0.08*13;			
			if(cm >= w_max) //IGNORE THIS READING
			{

				//length = 0;
				//w_max = cm;
			}
			else if(cm <= 0.7*w_max)
			{				
				ul = cm;
				
			}
			else if (0.9*w_max <= cm && cm <= 0.99*w_max) // THIS MAY MEAN THAT NO ONE IS PASSING BY 
			{
				//INITIALIZE ALL VARIABLES AND FINISH UP THE CALCULATION IF NOT YET DONE
				if(first != 0 && last != 0)
				{
					if(right_sum > 0)
					{
						circumference = left_sum + right_sum + first +last;
						//cout << "circumference: " << circumference << ", left: " << left_sum << ", right: " << right_sum << ", first: " << first << ", last: " << last << endl;
						cout << "circumference: "<< circumference << endl;
					}
					//printf("circumference = %f\n",circumference);
					//INITIALIZING VARIABLES
					length = 0;
					left_sum = 0;
					right_sum = 0;

					r_prev.x = 0;
					r_prev.y = 0;
					l_prev.x = 0;
					l_prev.y = 0;

					first  = 0;
					last = 0;
				}
			}
		}
		if(strcmp(tok1,"UL") == 0)
		{
			length+= 0.08*13; 			
			if(cm <= 0.7*w_max && ul > 0)
			{	
				
				ur = cm;
				double width = w_max - ur - ul;
				
				if(width > 0)
				{
					
					if(first == 0 || (length - r_prev.y) > 10)// the second condition is when the first is very noted long go
					{
						first  = width;
						//cout << "first: " <<first << ", length: " << length << endl;						
					}
					else
					  last = width;
					//now compute the lengths
					struct point r_current,l_current;
					
					if(r_prev.y == 0 && l_prev.y == 0) // THIS IS BECAUSE IT THE FIRST POINT SO JUST SAVE IT IN THE PREVIOUS TO BE USE IN THE NEXT ROUND
					{
						r_prev.x = width/2;
						r_prev.y = length;
						l_prev.x = width/2;
						l_prev.y = length;
					}
					else
					{
						r_current.x = width/2;
						r_current.y = length;
						l_current.x = width/2;
						l_current.y = length;
						if((l_current.y - l_prev.y) < 5.0)
						{
							cout << "width: " << width << ", ur: " << ur <<", ul: " << ul << ", length: "<< length <<endl;
							left_sum += euclideanDistance(l_current,l_prev);
							right_sum += euclideanDistance(r_current,r_prev);
						}
						else
						{
							left_sum = 0;
							right_sum = 0;

						}


						r_prev.x = r_current.x;
						r_prev.y = r_current.y;
						l_prev.x = l_current.x;
						l_prev.y = l_current.y;
					}
				}
			}
		}
	}

	return 0;
}
double euclideanDistance(struct point a, struct point b)
{
    return sqrt(pow(a.x-b.x,2) + pow(a.y-b.y,2));
}

