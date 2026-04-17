#include "Calculator.h"
#include <regex>
#include <iomanip>
#include <locale>
#include <sstream>
#include <algorithm>

Calculator::Calculator() : variable_version(0) {}

bool Calculator::isValidIdentifier(const std::string& id) const {
    if (id.empty() || std::isdigit(id[0])) return false;
    for (char c : id) {
        if (!std::isalnum(c) && c != '_') return false;
    }
    return true;
}

std::vector<std::string> Calculator::parseCommand(const std::string& cmd) {
    std::vector<std::string> parts;
    std::istringstream iss(cmd);
    std::string token;
    while (iss >> token) {
        parts.push_back(token);
    }
    return parts;
}

void Calculator::handleVar(const std::vector<std::string>& parts) {
    if (parts.size() != 2) {
        output << "Invalid usage" << std::endl;
        return;
    }
    std::string id = parts[1];
    if (!isValidIdentifier(id)) {
        output << "Invalid usage" << std::endl;
        return;
    }
    if (variables.count(id) || functions.count(id)) {
        output << "Name already exists" << std::endl;
        return;
    }
    variables[id] = Variable(id);
    variable_version++;
}

void Calculator::handleLet(const std::vector<std::string>& parts) {
    if (parts.size() != 2) {
        output << "Invalid usage" << std::endl;
        return;
    }
    std::string assignment = parts[1];
    size_t eqPos = assignment.find('=');
    if (eqPos == std::string::npos) {
        output << "Invalid usage" << std::endl;
        return;
    }
    std::string id = assignment.substr(0, eqPos);
    std::string valueStr = assignment.substr(eqPos + 1);
    if (!isValidIdentifier(id)) {
        output << "Invalid usage" << std::endl;
        return;
    }
    if (functions.count(id)) {
        output << "Invalid usage" << std::endl;
        return;
    }
    double val;
    std::locale old = std::locale::global(std::locale("C"));
    double numVal;
    bool isNumber = false;
    try {
        numVal = std::stod(valueStr);
        isNumber = true;
    } catch (...) {
    }
    std::locale::global(old);
    if (isNumber) {
        val = numVal;
    } else {
        if (!isValidIdentifier(valueStr)) {
            output << "Invalid usage" << std::endl;
            return;
        }
        auto vit = variables.find(valueStr);
        if (vit == variables.end()) {
            auto fit = functions.find(valueStr);
            if (fit == functions.end()) {
                output << "Name does not exist" << std::endl;
                return;
            }
            val = fit->second.evaluate(variables, functions, variable_version);
        } else {
            val = vit->second.get();
        }
    }
    if (variables.count(id)) {
        variables[id].set(val);
    } else {
        variables[id] = Variable(id);
        variables[id].set(val);
    }
    variable_version++;
}

void Calculator::handleFn(const std::vector<std::string>& parts) {
    if (parts.size() < 2) {
        output << "Invalid usage" << std::endl;
        return;
    }
    std::string rest = "";
    for (size_t i = 1; i < parts.size(); ++i) {
        rest += parts[i];
        if (i < parts.size() - 1) rest += " ";
    }
    // Remove spaces around =
    size_t eqPos = rest.find('=');
    if (eqPos == std::string::npos) {
        output << "Invalid usage" << std::endl;
        return;
    }
    std::string name = rest.substr(0, eqPos);
    std::string expr = rest.substr(eqPos + 1);
    // Trim spaces
    name.erase(name.begin(), std::find_if(name.begin(), name.end(), [](int ch) { return !std::isspace(ch); }));
    name.erase(std::find_if(name.rbegin(), name.rend(), [](int ch) { return !std::isspace(ch); }).base(), name.end());
    expr.erase(expr.begin(), std::find_if(expr.begin(), expr.end(), [](int ch) { return !std::isspace(ch); }));
    expr.erase(std::find_if(expr.rbegin(), expr.rend(), [](int ch) { return !std::isspace(ch); }).base(), expr.end());
    if (!isValidIdentifier(name)) {
        output << "Invalid usage" << std::endl;
        return;
    }
    if (variables.count(name) || functions.count(name)) {
        output << "Name already exists" << std::endl;
        return;
    }
    // Parse expr
    char op = '\0';
    size_t opPos = std::string::npos;
    if ((opPos = expr.find('+')) != std::string::npos) op = '+';
    else if ((opPos = expr.find('-')) != std::string::npos) op = '-';
    else if ((opPos = expr.find('*')) != std::string::npos) op = '*';
    else if ((opPos = expr.find('/')) != std::string::npos) op = '/';
    if (op != '\0') {
        std::string left = expr.substr(0, opPos);
        std::string right = expr.substr(opPos + 1);
        left.erase(left.begin(), std::find_if(left.begin(), left.end(), [](int ch) { return !std::isspace(ch); }));
        left.erase(std::find_if(left.rbegin(), left.rend(), [](int ch) { return !std::isspace(ch); }).base(), left.end());
        right.erase(right.begin(), std::find_if(right.begin(), right.end(), [](int ch) { return !std::isspace(ch); }));
        right.erase(std::find_if(right.rbegin(), right.rend(), [](int ch) { return !std::isspace(ch); }).base(), right.end());
        if (!isValidIdentifier(left) || !isValidIdentifier(right)) {
            output << "Invalid usage" << std::endl;
            return;
        }
        functions[name] = Function(name, left, op, right);
    } else {
        if (!isValidIdentifier(expr)) {
            output << "Invalid usage" << std::endl;
            return;
        }
        functions[name] = Function(name, expr);
    }
}

void Calculator::handlePrint(const std::vector<std::string>& parts) {
    if (parts.size() != 2) {
        output << "Invalid usage" << std::endl;
        return;
    }
    std::string id = parts[1];
    if (!isValidIdentifier(id)) {
        output << "Invalid usage" << std::endl;
        return;
    }
    auto vit = variables.find(id);
    if (vit != variables.end()) {
        double val = vit->second.get();
        output << std::fixed << std::setprecision(2) << val << std::endl;
        return;
    }
    auto fit = functions.find(id);
    if (fit != functions.end()) {
        double val = fit->second.evaluate(variables, functions, variable_version);
        output << std::fixed << std::setprecision(2) << val << std::endl;
        return;
    }
    output << "Name does not exist" << std::endl;
}

void Calculator::handlePrintvars() {
    std::vector<std::pair<std::string, double>> vars;
    for (const auto& p : variables) {
        vars.emplace_back(p.first, p.second.get());
    }
    std::sort(vars.begin(), vars.end());
    for (const auto& p : vars) {
        output << p.first << ":" << std::fixed << std::setprecision(2) << p.second << std::endl;
    }
}

void Calculator::handlePrintfns() {
    std::vector<std::pair<std::string, double>> fns;
    for (const auto& p : functions) {
        fns.emplace_back(p.first, p.second.evaluate(variables, functions, variable_version));
    }
    std::sort(fns.begin(), fns.end());
    for (const auto& p : fns) {
        output << p.first << ":" << std::fixed << std::setprecision(2) << p.second << std::endl;
    }
}

void Calculator::processCommand(const std::string& cmd) {
    std::vector<std::string> parts = parseCommand(cmd);
    if (parts.empty()) return;
    std::string command = parts[0];
    if (command == "var") {
        handleVar(parts);
    } else if (command == "let") {
        handleLet(parts);
    } else if (command == "fn") {
        handleFn(parts);
    } else if (command == "print") {
        handlePrint(parts);
    } else if (command == "printvars") {
        handlePrintvars();
    } else if (command == "printfns") {
        handlePrintfns();
    } else {
        output << "Unknown command" << std::endl;
    }
}

std::string Calculator::getOutput() const {
    return output.str();
}

void Calculator::clearOutput() {
    output.str("");
    output.clear();
}