#include <unistd.h>
#include <stdio.h>
#include <sys/socket.h>
#include <sys/wait.h>
#include <stdlib.h>
#include <netinet/in.h>
#include <string.h>
#include <iostream>
#include <signal.h>

int max_connection_process = 10;

void child_process(int concli) {
  char buffer[1024];
  char* data = 0x0;
  int len = 0;
  int s;

  while ((s=recv(concli,buffer,1023,0))>0) {
    buffer[s] = 0x0;
    if (data == 0x0) {
      data = strdup(buffer);
      len = s;
    }
    else {
      data = (char*) realloc(data, len + s + 1) ;
      strncpy(data + len, buffer, s) ;
      data[len + s] = 0x0 ;
      len += s ;
    }
  }
  printf("> %s\n", data);
  close(concli);
  exit(0);
}

void sigchld_handler(int sig) {
  
}

int main() {
  signal(SIGCHLD, sigchld_handler);

  int listen_fd, accept_connection;
  struct sockaddr_in address;
  int addrlen = sizeof(address);

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
    if (max_connection_process >= 0) {
      if (listen(listen_fd, 16) == -1) {
        perror("Failed to listen...");
        exit(EXIT_FAILURE);
      }

      accept_connection = accept(listen_fd, (struct sockaddr*)&address, (socklen_t*)&addrlen);
      if (accept_connection == -1) {
        perror("Failed to accept connection...");
        exit(EXIT_FAILURE);
      }

      max_connection_process -= 1;
      std::cout << max_connection_process << std::endl;

      if(fork() == 0){
        child_process(accept_connection);
      }
      else{
        close(accept_connection);
      }
    }
  }
}
