#include <iostream>
class A{
public:
  int c, d;
  A(int a, int b) : c(a+b), d(a-b){};
};
int main(){
  int a, b = 1, 2;
  A a = A(a,b);
  std::cout << a.c + " " + a.d << std::endl;
}
