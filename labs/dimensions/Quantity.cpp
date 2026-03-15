//#pragma once
#include <format>
#include <stdexcept>
#include "Dimension.h"
#include "Unit.h"
#include "Quantity.h"

Quantity::Quantity(double valueSI,
         const Dimension& dim):
         valueSI(valueSI), dim(dim){}
Quantity::Quantity(double value,
        const Unit& unit):
    valueSI(unit.calcValueSi(value)), dim(unit.dim){}
std::string Quantity::valueWithDim(const Unit& unit) const{
    if (this->dim != unit.dim)
    {
        throw std::logic_error("Ошибка: величину нельзя вывести"
            " в этой единице!");
    }

    double value = this->valueSI / unit.factor;
    return std::format("{} {}", value, unit.name);
}


Quantity Quantity::operator-() const{
    double new_valueSI = -this->valueSI;
    Dimension new_dim = this->dim;
    return Quantity(new_valueSI, new_dim);
}
const Quantity& Quantity::operator+() const{
    return (*this);
}

Quantity Quantity::operator+(const Quantity& other ) const{
    if (this->dim != other.dim)
    {
        throw std::logic_error("Нельзя складывать"
        " величины разных размерностей!");
    }

    double new_valueSI = this->valueSI + other.valueSI;
    Dimension new_dim = this->dim;
    return Quantity(new_valueSI, new_dim);
}
Quantity Quantity::operator-(const Quantity& other ) const{
    return (*this) + (-other);
}
Quantity& Quantity::operator+=(const Quantity& other ){
    (*this) = (*this) + other;
    return (*this);
}
Quantity& Quantity::operator-=(const Quantity& other ){
    (*this) += (-other);
    return (*this);
}

Quantity Quantity::operator*(const Quantity& other ) const{
    Quantity result;
    result.valueSI = this->valueSI * other.valueSI;
    result.dim = this->dim * other.dim;
    return result;
}
Quantity Quantity::operator/(const Quantity& other ) const{
        if (other.valueSI == 0)
    {
        throw std::runtime_error("Деление на ноль!");
    }
    Quantity result;
    result.valueSI = this->valueSI / other.valueSI;
    result.dim = this->dim / other.dim;
    return result;
}
Quantity& Quantity::operator*= (const Quantity& other) {
    (*this) = (*this) * other;
    return (*this);
}
Quantity& Quantity::operator/= (const Quantity& other) {
    (*this) = (*this) / other;
    return (*this);
}
bool Quantity::isEqualDim(const Unit& unit) const{
    return this->dim == unit.dim;
}

std::ostream& operator<<(
        std::ostream& out, const Quantity& q){
            out << q.valueSI << ' '
                <<  q.dim;
        return out;
}