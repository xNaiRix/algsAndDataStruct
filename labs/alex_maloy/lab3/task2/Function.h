#pragma once
#include <string>
#include <map>
#include "Variable.h"

class Function {
public:
    std::string name;
    std::string left;
    char op;
    std::string right;
    bool isSimple;    mutable double cached_value;
    mutable int cached_version;
    mutable bool has_cache;
    Function();
    Function(std::string n, std::string id);
    Function(std::string n, std::string l, char o, std::string r);
    double evaluate(const std::map<std::string, Variable>& vars, const std::map<std::string, Function>& funcs, int version) const;
};