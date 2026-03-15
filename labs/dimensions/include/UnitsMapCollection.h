#pragma once
#include <map>
#include <vector>
#include <string>
#include "Unit.h"
class UnitsMapCollection: public std::map<std::string, Unit>{
    void insertUnit(const Unit& unit);
    void initUnits();
 public:
    UnitsMapCollection();
    std::vector<std::string> getShortNames();
};