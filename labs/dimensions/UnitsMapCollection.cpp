//#pragma once
#include "UnitsMapCollection.h"
#include "Unit.h"
#include <string>

void UnitsMapCollection::insertUnit(const Unit& unit){
    (*this)[unit.getName()] = unit;
}
void UnitsMapCollection::initUnits(){
    this->insertUnit(Unit("m", Dimension(0, 1, 0), 1.0));
    this->insertUnit(Unit("cm", Dimension(0, 1, 0), 0.01));
    this->insertUnit(Unit("s", Dimension(0, 0, 1), 1.0));
    this->insertUnit(Unit("kg", Dimension(1, 0, 0), 1.0));
    this->insertUnit(Unit("m/s", Dimension(0, 1, -1)));
    this->insertUnit(Unit("m/s^2", Dimension(0, 1, -2)));
    this->insertUnit(Unit("N", Dimension(1, 1, -2)));
    this->insertUnit(Unit("m^3", Dimension(0, 3, 0)));
    this->insertUnit(Unit("kg/m^3", Dimension(1, -3, 0)));
    this->insertUnit(Unit("J", Dimension(1, 2, -2)));
    this->insertUnit(Unit("W", Dimension(1, 2, -3)));
    this->insertUnit(Unit("A", Dimension(0, 0, 0, 1)));
    this->insertUnit(Unit("q", Dimension(0, 0, 1, 1)));
    this->insertUnit(Unit("V", Dimension(1, 2, -3, -1)));
    this->insertUnit(Unit("Om", Dimension(1, 2, -3, -2)));
}
UnitsMapCollection::UnitsMapCollection(){this->initUnits();}
std::vector<std::string> UnitsMapCollection::getShortNames(){
    std::vector<std::string> short_names;
    for (const auto& [key, value] : (*this)){
        short_names.push_back(key);
    }
    return short_names;
}