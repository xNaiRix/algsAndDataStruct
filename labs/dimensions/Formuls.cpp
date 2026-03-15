//#pragma once
#include "Formuls.h"
#include <stdexcept>
Quantity Formuls::calcSpeed(const Quantity& s, const Quantity& t){
    if (!s.isEqualDim(units.at("m"))){
        throw std::logic_error("'s' must be space dim");
    }
    if (!t.isEqualDim(units.at("s"))){
        throw std::logic_error("'t' must be time dim");
    }
    return s/t;
}
Quantity Formuls::calcAccelaration(const Quantity& v, const Quantity& t){
    if (!v.isEqualDim(units.at("m/s"))){
        throw std::logic_error("'v' must be speed dim");
    }
    if (!t.isEqualDim(units.at("s"))){
        throw std::logic_error("'t' must be time dim");
    }
    return v/t;
}
Quantity Formuls::calcForce(const Quantity& m, const Quantity& a){
    if (!m.isEqualDim(units.at("kg"))){
        throw std::logic_error("'m' must be mass dim");
    }
    if (!a.isEqualDim(units.at("m/s^2"))){
        throw std::logic_error("'a' must be accelaration dim");
    }
    return m*a;
}
Quantity Formuls::calcWork(const Quantity& F, const Quantity s){
    if (!F.isEqualDim(units.at("N"))){
        throw std::logic_error("'F' must be force dim");
    }
    if (!s.isEqualDim(units.at("m"))){
        throw std::logic_error("'s' must be space dim");
    }
    return F*s;
}
Quantity Formuls::calcPower(const Quantity& A, const Quantity t){
    if (!A.isEqualDim(units.at("J"))){
        throw std::logic_error("'A' must be energy dim");
    }
    if (!t.isEqualDim(units.at("s"))){
        throw std::logic_error("'t' must be time dim");
    }
    return A/t;
}

Quantity Formuls::calcCharge(const Quantity& I, const Quantity t){
    if (!I.isEqualDim(units.at("A"))){
        throw std::logic_error("'I' must be amperage dim");
    }
    if (!t.isEqualDim(units.at("s"))){
        throw std::logic_error("'t' must be time dim");
    }
    return I*t;
}
Quantity Formuls::calcVoltage(const Quantity& A, const Quantity q){
    if (!A.isEqualDim(units.at("J"))){
        throw std::logic_error("'A' must be energy dim");
    }
    if (!q.isEqualDim(units.at("q"))){
        throw std::logic_error("'q' must be charge dim");
    }
    return A/q;
}
Quantity Formuls::calcResistance(const Quantity& U, const Quantity I){
    if (!U.isEqualDim(units.at("V"))){
        throw std::logic_error("'V' must be voltage dim");
    }
    if (!I.isEqualDim(units.at("I"))){
        throw std::logic_error("'I' must be amperage dim");
    }
    return U/I;
}
Quantity Formuls::calcElectricityPower(const Quantity& U, const Quantity I){
    if (!U.isEqualDim(units.at("V"))){
        throw std::logic_error("'V' must be voltage dim");
    }
    if (!I.isEqualDim(units.at("I"))){
        throw std::logic_error("'I' must be amperage dim");
    }
    return U*I;
}
