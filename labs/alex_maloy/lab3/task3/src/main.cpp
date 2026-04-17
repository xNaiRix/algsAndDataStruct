#include "economy.hpp"
#include <iostream>
#include <string>

int main(int argc, char* argv[])
{
    int numIterations = -1;

    // Check command line arguments
    if (argc > 1)
    {
        try
        {
            numIterations = std::stoi(argv[1]);
            if (numIterations < 0)
            {
                std::cerr << "Error: Number of iterations cannot be negative" << std::endl;
                return 1;
            }
        }
        catch (const std::exception& e)
        {
            std::cerr << "Error: Invalid number of iterations: " << argv[1] << std::endl;
            return 1;
        }
    }

    // If not provided via command line, read from stdin
    if (numIterations < 0)
    {
        std::cout << "Enter the number of simulation iterations: ";
        std::cin >> numIterations;

        if (std::cin.fail() || numIterations < 0)
        {
            std::cerr << "Error: Invalid input" << std::endl;
            return 1;
        }
    }

    std::cout << "\n========== ECONOMY SIMULATION ==========" << std::endl;
    std::cout << "Iterations: " << numIterations << std::endl;

    // Create economy with initial money
    Economy economy(10000, true);  // 10000 initial cash, include bonus actors

    // Run simulation
    try
    {
        economy.RunSimulation(numIterations);
    }
    catch (const std::exception& e)
    {
        std::cerr << "Simulation error: " << e.what() << std::endl;
        return 1;
    }

    return 0;
}
