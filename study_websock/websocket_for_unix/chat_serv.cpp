#include <unistd.h>
#include <stdio.h>
#include <sys/socket.h>
#include <stdlib.h>
#include <netinet/in.h>
#include <string.h>
#include <iostream>

int main() {
  int listen_fd, socket;
  struct sockaddr_in address;
  int addrlen = sizeof(address);

  char buffer[1024] = {0};

  listen_fd = socket(AF_INET, SOCK_STREAM, 0);
  if (listen_fd == 0) {
    perror("Creat socket failed...");
    exit(EXIT_FAILURE);
  }
  std::cout << addrlen << std::endl;
  memset(&address, '0', sizeof(address));

  address.sin_family = AF_INET;
  address.sin_port = htons(8000);
  address.sin_addr.s_addr = INADDR_ANY;
  if (bind(listen_fd, (struct sockaddr*)&address, sizeof(address)) == -1) {
    perror("Failed for binding");
    exit(EXIT_FAILURE);
  }
  printf("Binding to %u:%hu, Success",address.sin_addr.s_addr, address.sin_port);
}
