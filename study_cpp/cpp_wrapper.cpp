#include <iostream>
class A{
public:
  int c, d;
  explicit A(int a, int b) : c(a+b), d(a-b){};
};
int main(){
  int a, b;
  a = 1;
  b = 2;
  A a_object(a,b);
  std::cout << a_object.c << std::endl;
  std::cout << a_object.d << std::endl;
}
