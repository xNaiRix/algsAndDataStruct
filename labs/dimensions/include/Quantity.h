#pragma once
#include "Dimension.h"
#include "Unit.h"
#include <ostream>
#include <string>
class Quantity
{
    double valueSI;   // значение в СИ -- в будущем: другие представления числе - через базовый класс?
    Dimension dim;    // размерность

    friend std::ostream& operator<<(
        std::ostream& out, const Quantity& q);
 public:
    Quantity() = default;
    Quantity(double valueSI,
         const Dimension& dim);
    Quantity(double value,
        const Unit& unit);
    std::string valueWithDim(const Unit& unit) const;
    Quantity operator-() const;
    const Quantity& operator+() const;
    Quantity operator+(const Quantity& other ) const;
    Quantity operator-(const Quantity& other ) const;
    Quantity& operator+=(const Quantity& other );
    Quantity& operator-=(const Quantity& other );
    Quantity operator*(const Quantity& other ) const;
    Quantity operator/(const Quantity& other ) const;
    Quantity& operator*= (const Quantity& other);
    Quantity& operator/= (const Quantity& other);
    bool isEqualDim(const Unit& unit) const;


};

std::ostream& operator<<(
        std::ostream& out, const Quantity& q);