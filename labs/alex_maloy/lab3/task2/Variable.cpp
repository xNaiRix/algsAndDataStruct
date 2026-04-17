#include "Variable.h"

Variable::Variable() : name(""), value(std::nan("")), defined(false) {}

Variable::Variable(std::string n) : name(n), value(std::nan("")), defined(false) {}

void Variable::set(double v) {
    value = v;
    defined = true;
}

double Variable::get() const {
    return defined ? value : std::nan("");
}