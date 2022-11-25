#ifndef SERVER_MAIN_H
#define SERVER_MAIN_H
#define _WINSOCK_DEPRECATED_NO_WARNINGS

#include

#pragma comment(lib, "ws2_32")

#include
using std::cout;
using std::endl;

#include
using std::random_device;
using std::mt19937;
using std::uniform_int_distribution;

#include
#include

#include
#include

#define SERVER_PORT 8000
#define BUF_SIZE 4096
#define QUEUE_SIZE 10
#define IPAddress "127.0.0.1"

#endif