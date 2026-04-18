#ifndef ECONOMY_HPP
#define ECONOMY_HPP

#include "bank.hpp"
#include "actors.hpp"
#include <vector>
#include <memory>

// Economy simulation manager
class Economy
{
private:
    Bank bank_;
    std::vector<std::unique_ptr<Actor>> actors_;
    int currentStep_;
    int maxSteps_;
    mutable Money initialTotalMoney_;

    // Actor pointers for special interactions
    Homer* homer_;
    Marge* marge_;
    Bart* bart_;
    Lisa* lisa_;
    Apu* apu_;
    Burns* burns_;

    // Bonus actors
    Nelson* nelson_;
    Snake* snake_;
    Smithers* smithers_;

public:
    // Initialize economy with initial cash and actors
    // incudeBonusActors: include Nelson, Snake, and Smithers
    Economy(Money initialCash, bool includeBonusActors = true);

    // Run one step of simulation
    void Step();

    // Run full simulation for numSteps iterations
    void RunSimulation(int numSteps);

    // Verify economy consistency
    bool VerifyConsistency() const;

    // Print detailed status of all actors and bank
    void PrintStatus() const;

    // Get bank
    Bank& GetBank();
    const Bank& GetBank() const;

    // Get current step number
    int GetCurrentStep() const;
};

#endif  // ECONOMY_HPP
