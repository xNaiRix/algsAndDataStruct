#include "Function.h"
#include <cmath>

Function::Function() : name(""), left(""), op('\0'), right(""), isSimple(false), cached_value(0.0), cached_version(-1), has_cache(false) {}

Function::Function(std::string n, std::string id) : name(n), left(id), op('\0'), right(""), isSimple(true), cached_value(0.0), cached_version(-1), has_cache(false) {}

Function::Function(std::string n, std::string l, char o, std::string r) : name(n), left(l), op(o), right(r), isSimple(false), cached_value(0.0), cached_version(-1), has_cache(false) {}

double getValue(const std::string& id, const std::map<std::string, Variable>& vars, const std::map<std::string, Function>& funcs, int version) {
    auto it = vars.find(id);
    if (it != vars.end()) return it->second.get();
    auto fit = funcs.find(id);
    if (fit != funcs.end()) return fit->second.evaluate(vars, funcs, version);
    return std::nan("");
}

double Function::evaluate(const std::map<std::string, Variable>& vars, const std::map<std::string, Function>& funcs, int version) const {
    if (has_cache && cached_version == version) {
        return cached_value;
    }
    double result;
    if (isSimple) {
        result = getValue(left, vars, funcs, version);
    } else {
        double lval = getValue(left, vars, funcs, version);
        double rval = getValue(right, vars, funcs, version);
        if (std::isnan(lval) || std::isnan(rval)) result = std::nan("");
        else {
            switch (op) {
                case '+': result = lval + rval; break;
                case '-': result = lval - rval; break;
                case '*': result = lval * rval; break;
                case '/': if (rval == 0.0) result = std::nan(""); else result = lval / rval; break;
                default: result = std::nan(""); break;
            }
        }
    }
    cached_value = result;
    cached_version = version;
    has_cache = true;
    return result;
}