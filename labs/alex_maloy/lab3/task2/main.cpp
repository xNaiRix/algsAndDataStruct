#include "Calculator.h"
#include <iostream>
#include <string>

int main() {
    std::cout << "Welcome to calculator!" << std::endl;
    std::cout << "Enter commands (Ctrl+Z then Enter on Windows, Ctrl+D on Linux to end):" << std::endl;
    Calculator calc;
    std::string line;
    while (std::getline(std::cin, line)) {
        if (line.empty()) continue;
        calc.processCommand(line);
        std::cout << calc.getOutput();
        calc.clearOutput();
    }
    return 0;
}