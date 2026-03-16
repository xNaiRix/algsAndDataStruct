#include <iostream>
#include "Quantity.h"
#include "UnitsMapCollection.h"
#include "Formuls.h"
//g++ -g (Resolve-Path *.cpp) -o program -std=c++20 -Iinclude  
UnitsMapCollection units;
Formuls formuls;

void tests(){
    std::cout <<std::endl << "2 m + 30 cm = " << 
    (Quantity(2., units.at("m")) + Quantity(30, units.at("cm"))).
    valueWithDim(units.at("m"));

    std::cout <<std::endl << "2 kg + 3s = " << 
    (Quantity(2., units.at("kg")) + Quantity(3., units.at("s"))).
    valueWithDim(units.at("s"));

    std::cout <<std::endl << "100 m / 20 s = " << 
    (Quantity(100., units.at("m")) / 
        Quantity(20, units.at("s"))).
    valueWithDim(units.at("m/s"));

    std::cout <<std::endl << "10 m/s / 2 s = " << 
    (Quantity(10., units.at("m/s")) / 
        Quantity(2, units.at("s"))).
        valueWithDim(units.at("m/s^2"));

    std::cout <<std::endl << "2 kg *  5 m/s^2 = " << 
    (Quantity(2., units.at("kg")) * 
        Quantity(5, units.at("m/s^2"))).
        valueWithDim(units["N"]);

    std::cout <<std::endl << "4 kg /  0.002 m^3 = " << 
    (Quantity(4., units.at("kg")) /
        Quantity(0.002, units.at("m^3"))).
        valueWithDim(units.at("kg/m^3"));//
    
    std:: cout << std::endl<<"Tests done! Also need to"
            " check answers\n";

}
void run(){
    std::string unitName;
    double value;

    std::cout << "Введите значение: ";
    std::cin >> value;

    std::cout << "Введите единицу: ";
    std::cin >> unitName;
    try {
    Unit u = units.at(unitName);
    Quantity q {value, u};
    std::cout << q;
    }
    catch (const std::exception& e){
        std::cout << "Ошибка " << e.what() << std::endl;
    }
}

int main() {
    setlocale(LC_ALL, "ru");
    //formuls = Formuls(units);
    auto names = units.getShortNames();
    for (auto& c: names){
        std::cout << c << '\n';
    }
    Quantity s = Quantity(3200, units.at("cm"));
    Quantity t = Quantity(20, units.at("s"));
    Quantity v = formuls.calcSpeed(s, t);
    std::cout << v.valueWithDim(units.at("m/s"));
    //tests();
    //run();
    //+-*/ 
    

    return 0;
}
