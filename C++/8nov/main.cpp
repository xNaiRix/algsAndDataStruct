#include <iostream>
using std::cout, std::cin;
int main() {
    setlocale(LC_ALL, "ru");
    int a,b,c; cin >> a >> b;
    c = a+b;
    cout << "Сумма " << a << " + " << b << " = " << c << '\n';
    return 0;
}