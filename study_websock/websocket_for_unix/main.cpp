#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <string.h>
#include <unistd.h>
#include <sys/types.h> 
#include <sys/socket.h>
#include <netinet/in.h>

using namespace std;

int main(){
	int listen_fd, new_socket;
	struct sockaddr_in address;
	int opt=1;
	int addrlen = sizeof(address);

	char buffer[1024] = {0};
	
	listen_fd = socket(AF_INET, SOCK_STREAM,0);
	if (listen_fd == 0) {
		perror("socket failed : ");
		exit(EXIT_FAILURE);
	}
	memset(&address, '0', sizeof(address));
	address.sin_family = AF_INET;
	address.sin_addr.s_addr = INADDR_ANY;
	address.sin_port = htons(8000);
	if (bind(listen_fd, (struct sockaddr *)&address, sizeof(address)) < 0) {
		perror("bind failed : ");
		exit(EXIT_FAILURE);
	}
}
