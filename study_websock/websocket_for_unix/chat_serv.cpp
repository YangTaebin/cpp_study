#include <unistd.h>
#include <stdio.h>
#include <sys/socket.h>
#include <stdlib.h>
#include <netinet/in.h>
#include <string.h>
#include <iostream>

void child_process(int concli) {

}

int main() {
  int listen_fd, accept_connection;
  struct sockaddr_in address;
  int addrlen = sizeof(address);

  char buffer[1024] = {0};

  listen_fd = socket(AF_INET, SOCK_STREAM, 0);
  if (listen_fd == 0) {
    perror("Creat socket failed...");
    exit(EXIT_FAILURE);
  }
  memset(&address, '0', sizeof(address));

  address.sin_family = AF_INET;
  address.sin_addr.s_addr = INADDR_ANY;
  address.sin_port = htons(8000);
  if (bind(listen_fd, (struct sockaddr*)&address, sizeof(address)) == -1) {
    perror("Failed for binding");
    exit(EXIT_FAILURE);
  }
  printf("Binding to %u:%hu, Success\n",address.sin_addr.s_addr, address.sin_port);

  while (1) {
    if (listen(listen_fd, 16) == -1) {
      perror("Failed to listen...");
      exit(EXIT_FAILURE);
    }

    accept_connection = accept(listen_fd, (struct sockaddr*)&address, (socklen_t*)&addrlen);
    if (accept_connection == -1) {
      perror("Failed to accept connection...");
      exit(EXIT_FAILURE);
    }

    child_process(accept_connection);
  }
}
