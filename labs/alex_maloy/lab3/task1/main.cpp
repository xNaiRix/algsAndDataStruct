#include "CommandProcessor.h"
#include <iostream>
#include <string>

int main() {
    CommandProcessor processor;
    std::string line;
    while (std::getline(std::cin, line)) {
        processor.processCommand(line);
    }
    return 0;
}