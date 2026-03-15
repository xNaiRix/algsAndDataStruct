//#pragma once
#include "Unit.h"
#include "Dimension.h"

Unit::Unit(std::string name,
         const Dimension& dim,
         double factor):
         name(name), factor(factor), dim(dim){}

std::string Unit::getName()const {return this->name;}

std::ostream& operator<<
    (std::ostream& out, const Unit& unit){
        out << unit.getName();
        return out;
}