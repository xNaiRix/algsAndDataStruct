#pragma once
#include "Dimension.h"
#include <string>
#include <ostream>

class Quantity;

class Unit
{
    std::string name;// короткое имя: "m", "kg", "s"
    Dimension dim;
    double factor;// коэффициент перевода в SI
    friend class Quantity;
    friend std::ostream& operator<< 
        (std::ostream& out, const Unit& unit);
 public:
    Unit() = default;
    Unit(std::string name,
         const Dimension& dim,
         double factor = 1.);
    template<typename T>
    T calcValueSi(const T& value) const {
        return value * this->factor;
    }
    std::string getName()const;
};
std::ostream& operator<<
    (std::ostream& out, const Unit& unit);