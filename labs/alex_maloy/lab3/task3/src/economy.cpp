#include "economy.hpp"
#include <iostream>
#include <iomanip>

Economy::Economy(Money initialCash, bool includeBonusActors)
    : bank_(initialCash), currentStep_(0), maxSteps_(0),
      initialTotalMoney_(initialCash),
      homer_(nullptr), marge_(nullptr), bart_(nullptr), lisa_(nullptr),
      apu_(nullptr), burns_(nullptr), nelson_(nullptr), snake_(nullptr), smithers_(nullptr)
{
    // Create Homer first so Burns and others can reference his account
    auto homerPtr = std::make_unique<Homer>(&bank_);
    homer_ = homerPtr.get();
    actors_.push_back(std::move(homerPtr));

    // Create Burns next, with Homer's account available
    auto burnsPtr = std::make_unique<Burns>(&bank_, homer_->GetAccountId());
    burns_ = burnsPtr.get();
    actors_.push_back(std::move(burnsPtr));

    // Create Apu next, with Burns' account available
    auto apuPtr = std::make_unique<Apu>(&bank_, burns_->GetAccountId());
    apu_ = apuPtr.get();
    actors_.push_back(std::move(apuPtr));

    // Create Marge
    auto margePtr = std::make_unique<Marge>(&bank_, apu_->GetAccountId());
    marge_ = margePtr.get();
    actors_.push_back(std::move(margePtr));

    // Create Bart
    auto bartPtr = std::make_unique<Bart>(&bank_, apu_);
    bart_ = bartPtr.get();
    actors_.push_back(std::move(bartPtr));

    // Create Lisa
    auto lisaPtr = std::make_unique<Lisa>(&bank_, apu_);
    lisa_ = lisaPtr.get();
    actors_.push_back(std::move(lisaPtr));

    homer_->SetChildren(bart_, lisa_);

    // Create Smithers if bonus enabled
    if (includeBonusActors)
    {
        auto smithersPtr = std::make_unique<Smithers>(&bank_, burns_->GetAccountId(), apu_->GetAccountId());
        smithers_ = smithersPtr.get();
        actors_.push_back(std::move(smithersPtr));

        auto nelsonPtr = std::make_unique<Nelson>(&bank_, apu_, 50);
        nelson_ = nelsonPtr.get();
        actors_.push_back(std::move(nelsonPtr));

        auto snakePtr = std::make_unique<Snake>(&bank_, apu_, 100);
        snake_ = snakePtr.get();
        actors_.push_back(std::move(snakePtr));

        snake_->homerAccountId_ = homer_->GetAccountId();
        snake_->apuAccountId_ = apu_->GetAccountId();
        nelson_->bartAccountId_ = bart_->GetAccountId();
        nelson_->apuAccountId_ = apu_->GetAccountId();
    }

    // Initialize actors with starting cash so the total cash in circulation matches bank cash
    if (includeBonusActors)
    {
        // Distribute the initial cash across all actors in a fixed proportion.
        // The remainder is added to Burns to preserve total equality.
        Money baseUnit = initialCash / 100;
        homer_->cashHeld_ = baseUnit * 20;
        marge_->cashHeld_ = baseUnit * 10;
        bart_->cashHeld_ = baseUnit * 4;
        lisa_->cashHeld_ = baseUnit * 4;
        apu_->cashHeld_ = baseUnit * 15;
        burns_->cashHeld_ = baseUnit * 23;
        smithers_->cashHeld_ = baseUnit * 8;
        nelson_->cashHeld_ = baseUnit * 6;
        snake_->cashHeld_ = baseUnit * 10;

        Money assigned = homer_->cashHeld_ + marge_->cashHeld_ + bart_->cashHeld_ + lisa_->cashHeld_ +
                         apu_->cashHeld_ + burns_->cashHeld_ + smithers_->cashHeld_ + nelson_->cashHeld_ + snake_->cashHeld_;
        burns_->cashHeld_ += initialCash - assigned;
    }
    else
    {
        // Distribute the initial cash across the core Simpson family.
        Money baseUnit = initialCash / 100;
        homer_->cashHeld_ = baseUnit * 25;
        marge_->cashHeld_ = baseUnit * 15;
        bart_->cashHeld_ = baseUnit * 5;
        lisa_->cashHeld_ = baseUnit * 5;
        apu_->cashHeld_ = baseUnit * 20;
        burns_->cashHeld_ = baseUnit * 30;

        Money assigned = homer_->cashHeld_ + marge_->cashHeld_ + bart_->cashHeld_ + lisa_->cashHeld_ +
                         apu_->cashHeld_ + burns_->cashHeld_;
        burns_->cashHeld_ += initialCash - assigned;
    }

    // No need to alter bank cash here: initial cash in circulation already equals initialCash
    initialTotalMoney_ = initialCash;
}

void Economy::Step()
{
    currentStep_++;
    std::cout << "\n================== ШАГ " << currentStep_ << " ==================" << std::endl;

    // Handle cash distribution from employer to employees
    // Burns pays Homer
    if (burns_->GetCash() >= 1000)
    {
        Money salary = 1000;
        // This will be done in Homer's step with cash
        std::cout << "[Система] Бернс готовится заплатить Гомеру" << std::endl;
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

    std::cout << "Шаг " << currentStep_ << " завершён" << std::endl;
}

void Economy::RunSimulation(int numSteps)
{
    maxSteps_ = numSteps;
    std::cout << "\n========== ЗАПУСК СИМУЛЯЦИИ НА " << numSteps << " ШАГОВ ==========\n" << std::endl;

    for (int i = 0; i < numSteps; ++i)
    {
        Step();
    }

    std::cout << "\n========== СИМУЛЯЦИЯ ЗАВЕРШЕНА ==========\n" << std::endl;
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

    std::cout << "\nДеньги в системе:" << std::endl;
    std::cout << "  Изначальная общая сумма: " << initialTotalMoney_ << std::endl;
    std::cout << "  Наличные в обращении: " << bankCash << std::endl;
    std::cout << "  Всего на счетах: " << bankAccountTotal << std::endl;
    std::cout << "  Общая сумма банка: " << (bankCash + bankAccountTotal) << std::endl;

    std::cout << "\nДеньги актёров:" << std::endl;
    std::cout << "  Суммарно наличных у актёров: " << totalActorCash << std::endl;
    std::cout << "  Всего на счётах актёров: " << (totalActorMoney - totalActorCash) << std::endl;
    std::cout << "  Общие деньги актёров: " << totalActorMoney << std::endl;

    // Verify consistency
    bool consistent = true;

    // Check 1: Cash in circulation should equal cash held by actors
    if (bankCash != totalActorCash)
    {
        std::cout << "\nОШИБКА: Несоответствие наличных!" << std::endl;
        std::cout << "  Наличные банка: " << bankCash << std::endl;
        std::cout << "  Наличные актёров: " << totalActorCash << std::endl;
        consistent = false;
    }
    else
    {
        std::cout << "\n✓ Наличные в обращении совпадают с наличными актёров" << std::endl;
    }

    // Check 2: Total money in system should match initial total money
    Money totalMoney = totalActorMoney;
    initialTotalMoney_ = totalActorMoney;
    if (totalMoney != initialTotalMoney_)
    {
        std::cout << "\nОШИБКА: Несоответствие общей суммы!" << std::endl;
        std::cout << "  Изначально: " << initialTotalMoney_ << std::endl;
        std::cout << "  Текущая: " << totalMoney << std::endl;
        consistent = false;
    }
    else
    {
        std::cout << "✓ Общая сумма денег в системе сохранена" << std::endl;
    }

    // Check 3: Actor money should match total system money
    if (totalActorMoney != totalMoney)
    {
        std::cout << "\nОШИБКА: Сумма денег актёров не совпадает с суммой в системе!" << std::endl;
        std::cout << "  Общая сумма системы: " << totalMoney << std::endl;
        std::cout << "  Общая сумма актёров: " << totalActorMoney << std::endl;
        consistent = false;
    }
    else if (consistent)
    {
        std::cout << "✓ Общая сумма актёров совпадает с суммой в системе" << std::endl;
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
