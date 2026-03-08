#include <iostream>
#include <vector>
#include <memory>
using namespace std;
class T {
  public:
    int x;
};
int main() {
    T t = T();
    t.x = 10;
    shared_ptr<T> p1 = shared_ptr<T>(t);
    t.x = 20;
    cout << p1->x << endl;
    //weak_ptr<T> p2;
}