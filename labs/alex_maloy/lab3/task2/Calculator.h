#pragma once
#include <string>
#include <map>
#include <iostream>
#include <sstream>
#include <vector>
#include <algorithm>
#include "Variable.h"
#include "Function.h"

class Calculator {
private:
    std::map<std::string, Variable> variables;
    std::map<std::string, Function> functions;
    std::ostringstream output;
    int variable_version;

    bool isValidIdentifier(const std::string& id) const;
    std::vector<std::string> parseCommand(const std::string& cmd);
    void handleVar(const std::vector<std::string>& parts);
    void handleLet(const std::vector<std::string>& parts);
    void handleFn(const std::vector<std::string>& parts);
    void handlePrint(const std::vector<std::string>& parts);
    void handlePrintvars();
    void handlePrintfns();

public:
    Calculator();
    void processCommand(const std::string& cmd);
    std::string getOutput() const;
    void clearOutput();
};