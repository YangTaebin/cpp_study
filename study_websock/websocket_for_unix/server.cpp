#include <unistd.h>
#include <stdio.h>
#include <sys/socket.h>
#include <stdlib.h>
#include <netinet/in.h>
#include <string.h>

void child_proc(int conn){
  char buf[1024] ;
  char * data = 0x0 ;
  int len = 0 ;
  int s ;

  while ( (s = recv(conn, buf, 1023, 0)) > 0 ) {
    buf[s] = 0x0 ;
    if (data == 0x0) {
      data = strdup(buf) ;
      len = s ;
    }
    //다시 메모리할당해줘요
    else {
      data = (char*) realloc(data, len + s + 1) ;
      strncpy(data + len, buf, s) ;
      data[len + s] = 0x0 ;
      len += s ;
    }

  }
  printf(">%s\n", data) ;
  //conn한테 다시 데이터를 보내줘요
  //s 만큼만 보내줄거에요 반복해요
  while (len > 0 && (s = send(conn, data, len, 0)) > 0) {
    data += s ;
    len -= s ;
  }
  shutdown(conn, SHUT_WR) ;
}

int main(int argc, char const *argv[])
{
  int listen_fd, new_socket ;
  struct sockaddr_in address;
  int opt = 1;
  int addrlen = sizeof(address);

  char buffer[1024] = {0};

  listen_fd = socket(AF_INET /*IPv4*/, SOCK_STREAM /*TCP*/, 0 /*IP*/) ;
  if (listen_fd == 0)  {
    perror("socket failed : ");
    exit(EXIT_FAILURE);
  }
  memset(&address, '0', sizeof(address));
  address.sin_family = AF_INET;
  address.sin_addr.s_addr = INADDR_ANY /* the localhost*/ ;
  address.sin_port = htons(8000);
  if (bind(listen_fd, (struct sockaddr *)&address, sizeof(address)) < 0) {
    perror("bind failed : ");
    exit(EXIT_FAILURE);
  }

  while (1) {
    if (listen(listen_fd, 16 /* the size of waiting queue*/) < 0) {
      perror("listen failed : ");
      exit(EXIT_FAILURE);
    }
    //message가 들어오면 시작해봅시다
    //new comer를 위해서 new socket을 생성해주자
    new_socket = accept(listen_fd, (struct sockaddr *) &address, (socklen_t*)&addrlen) ;
    if (new_socket < 0) {
      perror("accept");
      exit(EXIT_FAILURE);
    }

    if (fork() > 0) {
      //child보고 일하라고 하고 parent는 리스닝 다시
      child_proc(new_socket) ;
    }
    else {
      close(new_socket) ;
    }
  }
}
