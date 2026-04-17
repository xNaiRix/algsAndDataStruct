#include "Calculator.h"
#include <iostream>
#include <sstream>
#include <string>
#include <vector>
#include <iomanip>

void runTest(const std::string& testName, const std::vector<std::string>& commands, const std::string& expectedOutput) {
    Calculator calc;
    std::string actualOutput;

    std::cout << "========================================" << std::endl;
    std::cout << "TEST: " << testName << std::endl;
    std::cout << "----------------------------------------" << std::endl;
    std::cout << "Input commands:" << std::endl;
    for (size_t i = 0; i < commands.size(); ++i) {
        std::cout << "  " << (i + 1) << ". " << commands[i] << std::endl;
        calc.processCommand(commands[i]);
    }
    std::cout << "----------------------------------------" << std::endl;

    actualOutput = calc.getOutput();
    std::cout << "Actual output:" << std::endl;
    if (actualOutput.empty()) {
        std::cout << "  (none)" << std::endl;
    } else {
        std::istringstream actualStream(actualOutput);
        std::string line;
        int lineNum = 1;
        while (std::getline(actualStream, line)) {
            std::cout << "  " << lineNum << ": " << line << std::endl;
            lineNum++;
        }
    }

    std::cout << "Expected output:" << std::endl;
    if (expectedOutput.empty()) {
        std::cout << "  (none)" << std::endl;
    } else {
        std::istringstream expectedStream(expectedOutput);
        std::string line;
        int lineNum = 1;
        while (std::getline(expectedStream, line)) {
            std::cout << "  " << lineNum << ": " << line << std::endl;
            lineNum++;
        }
    }

    if (actualOutput == expectedOutput) {
        std::cout << "RESULT: PASS" << std::endl;
    } else {
        std::cout << "RESULT: FAIL" << std::endl;
        std::cout << "Differences:" << std::endl;
        std::istringstream actualStream(actualOutput);
        std::istringstream expectedStream(expectedOutput);
        std::string actualLine;
        std::string expectedLine;
        int lineNum = 1;
        while (std::getline(actualStream, actualLine) || std::getline(expectedStream, expectedLine)) {
            if (actualLine != expectedLine) {
                std::cout << "  line " << lineNum << ": actual='" << actualLine << "' expected='" << expectedLine << "'" << std::endl;
            }
            lineNum++;
        }
    }
    std::cout << std::endl;
}

int main() {
    // Test 1: Basic variable assignment
    std::vector<std::string> commands1 = {
        "var x",
        "print x",
        "let x=42",
        "print x",
        "let x=1.234",
        "print x",
        "let y=x",
        "let x=99",
        "printvars"
    };
    std::string expected1 = "nan\n42.00\n1.23\nx:99.00\ny:1.23\n";
    runTest("Basic variable assignment", commands1, expected1);

    // Test 2: Function declaration
    std::vector<std::string> commands2 = {
        "var x",
        "var y",
        "fn XPlusY=x+y",
        "print XPlusY",
        "let x=3",
        "let y=4",
        "print XPlusY",
        "let x=10",
        "print XPlusY",
        "let z=3.5",
        "fn XPlusYDivZ=XPlusY/z",
        "printfns"
    };
    std::string expected2 = "nan\n7.00\n14.00\nXPlusY:14.00\nXPlusYDivZ:4.00\n";
    runTest("Function declaration", commands2, expected2);

    // Test 3: Difference between fn and let
    std::vector<std::string> commands3 = {
        "let v=42",
        "let variable=v",
        "fn function=v",
        "let v=43",
        "print variable",
        "print function"
    };
    std::string expected3 = "42.00\n43.00\n";
    runTest("Difference between fn and let", commands3, expected3);

    // Test 4: Circle area calculation
    std::vector<std::string> commands4 = {
        "var radius",
        "let pi=3.14159265",
        "fn radiusSquared=radius*radius",
        "fn circleArea=pi*radiusSquared",
        "let radius=10",
        "print circleArea",
        "let circle10Area=circleArea",
        "let radius=20",
        "let circle20Area=circleArea",
        "printfns",
        "printvars"
    };
    std::string expected4 = "314.16\ncircleArea:1256.64\nradiusSquared:400.00\ncircle10Area:314.16\ncircle20Area:1256.64\npi:3.14\nradius:20.00\n";
    runTest("Circle area calculation", commands4, expected4);

    // Test 5: Fibonacci sequence
    std::vector<std::string> commands5 = {
        "let v0=0",
        "let v1=1",
        "fn fib0=v0",
        "fn fib1=v1",
        "fn fib2=fib1+fib0",
        "fn fib3=fib2+fib1",
        "fn fib4=fib3+fib2",
        "fn fib5=fib4+fib3",
        "fn fib6=fib5+fib4",
        "printfns",
        "let v0=1",
        "let v1=1",
        "printfns"
    };
    std::string expected5 = "fib0:0.00\nfib1:1.00\nfib2:1.00\nfib3:2.00\nfib4:3.00\nfib5:5.00\nfib6:8.00\nfib0:1.00\nfib1:1.00\nfib2:2.00\nfib3:3.00\nfib4:5.00\nfib5:8.00\nfib6:13.00\n";
    runTest("Fibonacci sequence", commands5, expected5);

    // Additional logic tests
    // Test invalid commands
    Calculator calc;
    calc.processCommand("unknown");
    std::string out = calc.getOutput();
    if (out == "Unknown command\n") {
        std::cout << "Invalid command test: PASS" << std::endl;
    } else {
        std::cout << "Invalid command test: FAIL" << std::endl;
    }

    // Test name already exists
    calc.clearOutput();
    calc.processCommand("var x");
    calc.processCommand("var x");
    out = calc.getOutput();
    if (out == "Name already exists\n") {
        std::cout << "Name already exists test: PASS" << std::endl;
    } else {
        std::cout << "Name already exists test: FAIL" << std::endl;
    }

    return 0;
}