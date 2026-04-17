#include "TVSet.h"
#include "CommandProcessor.h"
#include <iostream>
#include <string>
#include <sstream>
#include <vector>

// Test helper
void logTest(const std::string& testName, bool passed) {
    std::cout << "[" << (passed ? "PASS" : "FAIL") << "] " << testName << std::endl;
}

bool checkCondition(const std::string& description, bool condition) {
    logTest(description, condition);
    return condition;
}

// Function to run examples from the assignment
void runExamples() {
    std::cout << "\n=== Прогон примеров из задания ===\n";

    struct Example {
        std::string name;
        std::string input;
        std::string expectedOutput;
    };

    std::vector<Example> examples = {
        {
            "Пример 1 (базовый)",
            "TurnOn\nInfo\nTurnOff\nInfo\n",
            "TV is turned on\nTV is turned on\nChannel is: 1\nTV is turned off\nTV is turned off\n"
        },
        {
            "Пример 2 (SelectChannel)",
            "TurnOn\nSelectChannel 5\nInfo\n",
            "TV is turned on\nChannel switched to: 5\nTV is turned on\nChannel is: 5\n"
        },
        {
            "Пример 3 (ошибка SelectChannel)",
            "TurnOn\nSelectChannel 100\nInfo\n",
            "TV is turned on\nERROR\nTV is turned on\nChannel is: 1\n"
        },
        {
            "Пример SelectPreviousChannel 1",
            "TurnOn\nSelectChannel 2\nSelectChannel 5\nSelectPreviousChannel\nInfo\n",
            "TV is turned on\nChannel switched to: 2\nChannel switched to: 5\nSwitched to previous channel\nTV is turned on\nChannel is: 2\n"
        },
        {
            "Пример SelectPreviousChannel 2 (ошибка)",
            "TurnOn\nSelectPreviousChannel\n",
            "TV is turned on\nERROR\n"
        },
        {
            "Пример имен каналов 1",
            "TurnOn\nSetChannelName 5 OTP\nSelectChannel OTP\nInfo\n",
            "TV is turned on\nChannel name set: 5 - OTP\nChannel switched to: OTP\nTV is turned on\nChannel is: 5\n5 - OTP\n"
        },
        {
            "Пример имен каналов 2",
            "TurnOn\nSetChannelName 3 MTV\nGetChannelByName MTV\nInfo\nDeleteChannelName MTV\nGetChannelByName MTV\nInfo\n",
            "TV is turned on\nChannel name set: 3 - MTV\nChannel for name MTV: 3\nTV is turned on\nChannel is: 1\n3 - MTV\nChannel name deleted: MTV\nERROR\nTV is turned on\nChannel is: 1\n"
        }
    };

    for (const auto& ex : examples) {
        std::cout << "\n--- " << ex.name << " ---\n";
        std::cout << "Вход:\n" << ex.input << "\n";

        // Simulate processing
        std::istringstream inputStream(ex.input);
        std::ostringstream outputStream;
        // Redirect cout to outputStream
        std::streambuf* oldCout = std::cout.rdbuf();
        std::cout.rdbuf(outputStream.rdbuf());

        CommandProcessor processor;
        std::string line;
        while (std::getline(inputStream, line)) {
            processor.processCommand(line);
        }

        std::cout.rdbuf(oldCout); // Restore cout
        std::string actualOutput = outputStream.str();

        std::cout << "Выход программы:\n" << actualOutput << "\n";
        std::cout << "Ожидаемый выход:\n" << ex.expectedOutput << "\n";

        bool match = (actualOutput == ex.expectedOutput);
        std::cout << "Совпадение: " << (match ? "ДА" : "НЕТ") << "\n";

        if (!match) {
            std::cout << "Различия:\n";
            // Simple diff
            std::istringstream iss1(actualOutput);
            std::istringstream iss2(ex.expectedOutput);
            std::string line1, line2;
            int lineNum = 1;
            while (std::getline(iss1, line1) || std::getline(iss2, line2)) {
                if (line1 != line2) {
                    std::cout << "Строка " << lineNum << ":\n";
                    std::cout << "  Факт: '" << line1 << "'\n";
                    std::cout << "  Ожид: '" << line2 << "'\n";
                }
                lineNum++;
            }
        }
    }
}

// Other tests remain similar, but using includes
void testBasicFunctionality() {
    std::cout << "\n=== Базовый функционал ===" << std::endl;
    TVSet tv;

    checkCondition("Изначально выключен", !tv.IsOn());
    checkCondition("Начальный канал = 1", tv.GetCurrentChannel() == 1);

    // ... (similar to before, but using TVSet directly)
}

int main() {
    std::cout << "Запуск тестов..." << std::endl;

    testBasicFunctionality();
    // ... other tests

    runExamples();

    std::cout << "\nТесты завершены." << std::endl;
    return 0;
}