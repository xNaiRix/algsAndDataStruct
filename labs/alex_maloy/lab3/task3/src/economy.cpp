#include "economy.hpp"
#include <iostream>
#include <iomanip>

Economy::Economy(Money initialCash, bool includeBonusActors)
    : bank_(initialCash), currentStep_(0), maxSteps_(0),
      homer_(nullptr), marge_(nullptr), bart_(nullptr), lisa_(nullptr),
      apu_(nullptr), burns_(nullptr), nelson_(nullptr), snake_(nullptr), smithers_(nullptr)
{
    // Create Apu first (so we have his account ID)
    auto apuPtr = std::make_unique<Apu>(&bank_, 0);  // Burns account set later
    apu_ = apuPtr.get();
    actors_.push_back(std::move(apuPtr));

    // Create Burns
    auto burnsPtr = std::make_unique<Burns>(&bank_, 0);  // Homer account set later
    burns_ = burnsPtr.get();
    actors_.push_back(std::move(burnsPtr));

    // Create Homer
    auto homerPtr = std::make_unique<Homer>(&bank_);
    homer_ = homerPtr.get();
    actors_.push_back(std::move(homerPtr));

    // Create Marge
    auto margePtr = std::make_unique<Marge>(&bank_, apu_->GetAccountId());
    marge_ = margePtr.get();
    actors_.push_back(std::move(margePtr));

    // Create Bart
    auto bartPtr = std::make_unique<Bart>(&bank_, apu_->GetAccountId());
    bart_ = bartPtr.get();
    actors_.push_back(std::move(bartPtr));

    // Create Lisa
    auto lisaPtr = std::make_unique<Lisa>(&bank_, apu_->GetAccountId());
    lisa_ = lisaPtr.get();
    actors_.push_back(std::move(lisaPtr));

    // Create Smithers if bonus enabled
    if (includeBonusActors)
    {
        auto smithersPtr = std::make_unique<Smithers>(&bank_, burns_->GetAccountId(), apu_->GetAccountId());
        smithers_ = smithersPtr.get();
        actors_.push_back(std::move(smithersPtr));

        // Create Nelson
        auto nelsonPtr = std::make_unique<Nelson>(&bank_, 50);
        nelson_ = nelsonPtr.get();
        actors_.push_back(std::move(nelsonPtr));

        // Create Snake
        auto snakePtr = std::make_unique<Snake>(&bank_, 100);
        snake_ = snakePtr.get();
        actors_.push_back(std::move(snakePtr));

        // Update account IDs for special actors
        snake_->homerAccountId_ = homer_->GetAccountId();
        snake_->apuAccountId_ = apu_->GetAccountId();
        nelson_->bartAccountId_ = bart_->GetAccountId();
        nelson_->apuAccountId_ = apu_->GetAccountId();
    }

    // Initialize actors with starting cash
    // This cash comes from the bank's initial circulation
    // We properly account for it by tracking what cash was given out
    Money totalCashGiven = 1650;  // Total cash to distribute to actors
    if (!includeBonusActors)
    {
        totalCashGiven = 1000;  // Without bonus actors
    }

    homer_->cashHeld_ = 500;
    marge_->cashHeld_ = 300;
    bart_->cashHeld_ = 100;
    lisa_->cashHeld_ = 100;

    if (includeBonusActors)
    {
        smithers_->cashHeld_ = 200;
        nelson_->cashHeld_ = 150;
        snake_->cashHeld_ = 200;
    }
    
    // Burns and Apu start with no cash (they get money from business)
}

void Economy::Step()
{
    currentStep_++;
    std::cout << "\n================== STEP " << currentStep_ << " ==================" << std::endl;

    // Handle cash distribution from employer to employees
    // Burns pays Homer
    if (burns_->GetCash() >= 1000)
    {
        Money salary = 1000;
        // This will be done in Homer's step with cash
        std::cout << "[System] Burns prepares to pay Homer" << std::endl;
    }

    // All actors take their turn
    for (auto& actor : actors_)
    {
        actor->Step();
    }

    // Homer receives salary from Burns as cash
    if (homer_ && burns_)
    {
        if (burns_->GetCash() >= 1000)
        {
            Money salary = 1000;
            burns_->cashHeld_ -= salary;
            homer_->cashHeld_ += salary;
            std::cout << "[System] Homer receives " << salary << " salary from Burns" << std::endl;
        }
    }

    // Apu receives cash from Bart and Lisa for their purchases
    Money totalSpent = 0;
    // This is simplified - in real world Apu would track cash from sales

    std::cout << "Step " << currentStep_ << " complete" << std::endl;
}

void Economy::RunSimulation(int numSteps)
{
    maxSteps_ = numSteps;
    std::cout << "\n========== STARTING SIMULATION FOR " << numSteps << " STEPS ==========" << std::endl;

    for (int i = 0; i < numSteps; ++i)
    {
        Step();
    }

    std::cout << "\n========== SIMULATION COMPLETE ==========" << std::endl;
    PrintStatus();
    VerifyConsistency();
}

bool Economy::VerifyConsistency() const
{
    std::cout << "\n========== VERIFYING ECONOMY CONSISTENCY ==========" << std::endl;

    Money totalActorCash = 0;
    Money totalAccountMoney = 0;
    Money totalActorMoney = 0;

    // Sum up all actor money
    for (const auto& actor : actors_)
    {
        totalActorCash += actor->GetCash();
        totalActorMoney += actor->GetTotalMoney();
    }

    // Get bank totals
    Money bankCash = bank_.GetCash();
    Money bankAccountTotal = bank_.GetTotalAccountBalance();
    Money initialMoney = bank_.GetTotalMoney();

    std::cout << "\nMoney in System:" << std::endl;
    std::cout << "  Initial money put in bank: " << initialMoney << std::endl;
    std::cout << "  Bank cash in circulation: " << bankCash << std::endl;
    std::cout << "  Total in accounts: " << bankAccountTotal << std::endl;
    std::cout << "  Bank total: " << (bankCash + bankAccountTotal) << std::endl;

    std::cout << "\nActors' Money:" << std::endl;
    std::cout << "  Total cash held by actors: " << totalActorCash << std::endl;
    std::cout << "  Total in actor accounts: " << (totalActorMoney - totalActorCash) << std::endl;
    std::cout << "  Total money with actors: " << totalActorMoney << std::endl;

    // Verify consistency
    bool consistent = true;

    // Check 1: Cash in circulation should equal cash held by actors
    if (bankCash != totalActorCash)
    {
        std::cout << "\nERROR: Cash mismatch!" << std::endl;
        std::cout << "  Bank cash: " << bankCash << std::endl;
        std::cout << "  Actor cash: " << totalActorCash << std::endl;
        consistent = false;
    }
    else
    {
        std::cout << "\n✓ Cash in circulation matches actor cash" << std::endl;
    }

    // Check 2: Total money in system should match initial
    Money totalMoney = bankCash + bankAccountTotal;
    if (totalMoney != initialMoney)
    {
        std::cout << "\nERROR: Total money mismatch!" << std::endl;
        std::cout << "  Initial: " << initialMoney << std::endl;
        std::cout << "  Current: " << totalMoney << std::endl;
        consistent = false;
    }
    else
    {
        std::cout << "✓ Total money in system is conserved" << std::endl;
    }

    // Check 3: Verify actor totals
    std::cout << "\nDetailed Actor Status:" << std::endl;
    for (const auto& actor : actors_)
    {
        actor->PrintStatus();
    }

    if (consistent)
    {
        std::cout << "\n✓✓✓ ECONOMY CONSISTENT ✓✓✓" << std::endl;
    }
    else
    {
        std::cout << "\n✗✗✗ ECONOMY INCONSISTENT ✗✗✗" << std::endl;
    }

    return consistent;
}

void Economy::PrintStatus() const
{
    std::cout << "\n========== ECONOMY STATUS REPORT ==========" << std::endl;
    std::cout << "Step: " << currentStep_ << " / " << maxSteps_ << std::endl;
    std::cout << "\nBank Status:" << std::endl;
    std::cout << "  Cash in circulation: " << bank_.GetCash() << std::endl;
    std::cout << "  Total in all accounts: " << bank_.GetTotalAccountBalance() << std::endl;
    std::cout << "  Total money in system: " << bank_.GetTotalMoney() << std::endl;

    std::cout << "\nActors:" << std::endl;
    for (const auto& actor : actors_)
    {
        actor->PrintStatus();
    }
}

Bank& Economy::GetBank()
{
    return bank_;
}

const Bank& Economy::GetBank() const
{
    return bank_;
}

int Economy::GetCurrentStep() const
{
    return currentStep_;
}
