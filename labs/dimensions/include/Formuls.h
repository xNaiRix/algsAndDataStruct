#pragma once
#include "UnitsMapCollection.h"
#include "Quantity.h"
class Formuls{
    UnitsMapCollection units;

 public:
    Quantity calcSpeed(const Quantity& s, const Quantity& t);
    Quantity calcAccelaration(const Quantity& v,
         const Quantity& t);
    Quantity calcForce(const Quantity& m, const Quantity& a);
    Quantity calcWork(const Quantity& F, const Quantity s);
    Quantity calcPower(const Quantity& A, const Quantity t);
    Quantity calcCharge(const Quantity& I, const Quantity t);
    Quantity calcVoltage(const Quantity& A, const Quantity q);
    Quantity calcResistance(const Quantity& U,
        const Quantity I);
    Quantity calcElectricityPower(const Quantity& U, 
        const Quantity I);
};