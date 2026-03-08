#include <iostream>
using namespace std;
void f(){}
template<typename... Args>
void f(int a, float b, Args&& ...args) {
     cout << a << ' ' << b << endl;
     cout << sizeof...(args) << endl;
    f(args...);
 }
void print() {
    cout << "VOID PRINT";
}

template<typename... Args, typename T>//но это наверное долгая история. МОж
void print(Args... args, T x) {
    // if (x) cout << "true" << endl;
    // else cout << "false" << endl;
    cout << "boolean : " << x << endl;
    print(args...);
}
template<typename... Args>
void print(string x, string y, Args... args) {
    // if (x) cout << "true" << endl;
    // else cout << "false" << endl;
    cout << "string2 : " << x << ' ' << y << endl;
    print(args...);
}



template<typename... Args>
void print(Args... args) {
    cout << sizeof...(args) << endl;
    cout << sizeof...(Args) << endl;
    (cout << ... << args )<< endl;
    //print(args...);
}
int main() {
    print((string)"Hello world!", (string)"ello worl", "*", ",", "aaa", true, false);
    //f(2, true, 3, 3.2, 4, 4.3);
}