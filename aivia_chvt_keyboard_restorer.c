#include <stdlib.h>

int main(int argc, char* argv[])
{

	char buf[1024] = "chvt ";
	buf[5] = argv[1][0];
	system(buf);
	buf[5] = argv[2][0];
	buf[6] = argv[2][1];
	buf[7] = argv[2][2];
	system(buf);
	return 0;

}
