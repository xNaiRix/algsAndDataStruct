#pragma once
#include <string>
#include <map>
#include <cmath>

class Variable {
public:
    std::string name;
    double value;
    bool defined;

    Variable();
    Variable(std::string n);
    void set(double v);
    double get() const;
};