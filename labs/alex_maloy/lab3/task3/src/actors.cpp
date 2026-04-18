#include "actors.hpp"
#include <iostream>
#include <iomanip>
#include <cmath>

// ===== BASE ACTOR =====

Actor::Actor(const std::string& name, Bank* bank, Money initialCash)
    : name_(name), bank_(bank), cashHeld_(initialCash)
{
    accountId_ = bank->OpenAccount();
}

const std::string& Actor::GetName() const
{
    return name_;
}

Money Actor::GetCash() const
{
    return cashHeld_;
}

AccountId Actor::GetAccountId() const
{
    return accountId_;
}

Money Actor::GetTotalMoney() const
{
    try
    {
        return cashHeld_ + bank_->GetAccountBalance(accountId_);
    }
    catch (const BankOperationError&)
    {
        return cashHeld_;  // Account might be closed
    }
}

void Actor::ReceiveCashPayment(Money amount)
{
    cashHeld_ += amount;
}

void Actor::PrintStatus() const
{
    std::cout << "  " << name_ << ": Наличные=" << cashHeld_;
    try
    {
        std::cout << ", Баланс счета=" << bank_->GetAccountBalance(accountId_);
    }
    catch (const BankOperationError&)
    {
        std::cout << ", Счет=ЗАКРЫТ";
    }
    std::cout << ", Всего=" << GetTotalMoney() << std::endl;
}

// ===== HOMER SIMPSON =====

Homer::Homer(Bank* bank)
    : Actor("Homer", bank, 0),
      salaryPerStep_(1000),
      transferToMargePerStep_(300),
      electricityBillPerStep_(200),
      cashToChildrenPerStep_(100),
      bart_(nullptr),
      lisa_(nullptr)
{
}

void Homer::SetChildren(Actor* bart, Actor* lisa)
{
    bart_ = bart;
    lisa_ = lisa;
}

void Homer::Step()
{
    std::cout << "\n--- Ход " << name_ << " ---" << std::endl;

    try
    {
        if (cashHeld_ >= transferToMargePerStep_)
        {
            bank_->DepositMoney(accountId_, transferToMargePerStep_);
            cashHeld_ -= transferToMargePerStep_;
            std::cout << "  Гомер переводит " << transferToMargePerStep_
                      << " на счет Мардж" << std::endl;
        }
        else
        {
            std::cout << "  Гомер: Недостаточно наличных для перевода Мардж" << std::endl;
        }
    }
    catch (const std::exception& e)
    {
        std::cout << "  Гомер: Перевод Мардж не удался: " << e.what() << std::endl;
    }

    try
    {
        if (cashHeld_ >= electricityBillPerStep_)
        {
            bank_->DepositMoney(accountId_, electricityBillPerStep_);
            cashHeld_ -= electricityBillPerStep_;
            std::cout << "  Гомер платит " << electricityBillPerStep_
                      << " за электричество" << std::endl;
        }
        else
        {
            std::cout << "  Гомер: Недостаточно наличных для оплаты электричества" << std::endl;
        }
    }
    catch (const std::exception& e)
    {
        std::cout << "  Гомер: Оплата электричества не удалась: " << e.what() << std::endl;
    }

    try
    {
        if (cashHeld_ >= cashToChildrenPerStep_)
        {
            Money childShare = cashToChildrenPerStep_ / 2;
            cashHeld_ -= cashToChildrenPerStep_;
            if (bart_)
            {
                bart_->ReceiveCashPayment(childShare);
            }
            if (lisa_)
            {
                lisa_->ReceiveCashPayment(cashToChildrenPerStep_ - childShare);
            }
            std::cout << "  Гомер дает " << cashToChildrenPerStep_
                      << " наличными детям" << std::endl;
        }
        else
        {
            std::cout << "  Гомер: Недостаточно наличных для детей" << std::endl;
        }
    }
    catch (const std::exception& e)
    {
        std::cout << "  Гомер: Не удалось дать наличные детям: " << e.what() << std::endl;
    }
}

// ===== MARGE SIMPSON =====

Marge::Marge(Bank* bank, AccountId apuAccountId)
    : Actor("Marge", bank, 0),
      groceryExpensePerStep_(150),
      apuAccountId_(apuAccountId)
{
}

void Marge::Step()
{
    std::cout << "\n--- Ход " << name_ << " ---" << std::endl;

    // Buy groceries from Apu via bank transfer
    try
    {
        if (bank_->GetAccountBalance(accountId_) >= groceryExpensePerStep_)
        {
            bank_->SendMoney(accountId_, apuAccountId_, groceryExpensePerStep_);
            std::cout << "  Мардж покупает продукты у Апу за " << groceryExpensePerStep_
                      << " через перевод" << std::endl;
        }
        else
        {
            std::cout << "  Мардж: Недостаточно средств на счете для продуктов" << std::endl;
        }
    }
    catch (const std::exception& e)
    {
        std::cout << "  Мардж: Покупка продуктов не удалась: " << e.what() << std::endl;
    }
}

// ===== BART SIMPSON =====

Bart::Bart(Bank* bank, Apu* apu)
    : Actor("Bart", bank, 0),
      spendingPerStep_(30),
      apu_(apu),
      rng_(std::random_device{}())
{
}

void Bart::Step()
{
    std::cout << "\n--- Ход " << name_ << " ---" << std::endl;

    std::uniform_int_distribution<int> spend_dist(0, 100);
    if (spend_dist(rng_) < 60)  // 60% chance to buy something
    {
        Money amount = 5 + (spend_dist(rng_) % 20);  // Random amount 5-25
        if (cashHeld_ >= amount)
        {
            cashHeld_ -= amount;
            if (apu_)
            {
                apu_->ReceiveCashPayment(amount);
            }
            std::cout << "  Барт покупает что-то у Апу за " << amount
                      << " наличными" << std::endl;
        }
    }
}

// ===== LISA SIMPSON =====

Lisa::Lisa(Bank* bank, Apu* apu)
    : Actor("Lisa", bank, 0),
      spendingPerStep_(20),
      apu_(apu),
      rng_(std::random_device{}())
{
}

void Lisa::Step()
{
    std::cout << "\n--- Ход " << name_ << " ---" << std::endl;

    std::uniform_int_distribution<int> spend_dist(0, 100);
    if (spend_dist(rng_) < 40)  // 40% chance to buy something
    {
        Money amount = 5 + (spend_dist(rng_) % 15);  // Random amount 5-20
        if (cashHeld_ >= amount)
        {
            cashHeld_ -= amount;
            if (apu_)
            {
                apu_->ReceiveCashPayment(amount);
            }
            std::cout << "  Лиза покупает что-то у Апу за " << amount
                      << " наличными" << std::endl;
        }
    }
}

// ===== APU NAHASAPEEMAPETILON =====

Apu::Apu(Bank* bank, AccountId burnsAccountId)
    : Actor("Apu", bank, 0),
      electricityBillPerStep_(150),
      burnsAccountId_(burnsAccountId),
      depositThresholdCash_(500)
{
}

void Apu::Step()
{
    std::cout << "\n--- Ход " << name_ << " ---" << std::endl;

    // Try to pay electricity bill to Burns
    try
    {
        if (bank_->GetAccountBalance(accountId_) >= electricityBillPerStep_)
        {
            bank_->SendMoney(accountId_, burnsAccountId_, electricityBillPerStep_);
            std::cout << "  Апу платит " << electricityBillPerStep_
                      << " за электричество Бернсу" << std::endl;
        }
        else if (cashHeld_ >= electricityBillPerStep_)
        {
            // Can pay with cash from customer sales
            bank_->DepositMoney(accountId_, electricityBillPerStep_);
            cashHeld_ -= electricityBillPerStep_;
            bank_->SendMoney(accountId_, burnsAccountId_, electricityBillPerStep_);
            std::cout << "  Апу вносит и платит за электричество" << std::endl;
        }
        else
        {
            std::cout << "  Апу: Недостаточно средств для оплаты электричества" << std::endl;
        }
    }
    catch (const std::exception& e)
    {
        std::cout << "  Апу: Оплата электричества не удалась: " << e.what() << std::endl;
    }

    // Deposit cash to account if it exceeds threshold
    if (cashHeld_ > depositThresholdCash_)
    {
        try
        {
            Money depositAmount = cashHeld_ - (depositThresholdCash_ / 2);
            bank_->DepositMoney(accountId_, depositAmount);
            cashHeld_ -= depositAmount;
            std::cout << "  Апу вносит " << depositAmount << " наличными в банк" << std::endl;
        }
        catch (const std::exception& e)
        {
            std::cout << "  Апу: Внесение не удалось: " << e.what() << std::endl;
        }
    }
}

void Apu::ReceiveCashPayment(Money amount)
{
    cashHeld_ += amount;
}

// ===== MR. BURNS =====

Burns::Burns(Bank* bank, AccountId homerAccountId)
    : Actor("Mr. Burns", bank, 0),
      revenuePerStep_(1500),
      homerAccountId_(homerAccountId),
      salaryForHomer_(1000)
{
}

void Burns::Step()
{
    std::cout << "\n--- Ход " << name_ << " ---" << std::endl;

    try
    {
        if (bank_->TryWithdrawMoney(accountId_, salaryForHomer_))
        {
            cashHeld_ += salaryForHomer_;
            std::cout << "  Бернс снимает " << salaryForHomer_
                      << " со своего счета для оплаты Гомеру" << std::endl;
        }
        else
        {
            std::cout << "  Бернс: Недостаточно средств на счете для оплаты зарплаты" << std::endl;
        }
    }
    catch (const std::exception& e)
    {
        std::cout << "  Бернс: Снятие зарплаты не удалось: " << e.what() << std::endl;
    }
}

void Burns::ReceiveElectricityPayment(Money amount)
{
    cashHeld_ += amount;
}

// ===== NELSON (BONUS) =====

Nelson::Nelson(Bank* bank, Apu* apu, Money maxStealAmount)
    : Actor("Nelson", bank, 0),
      stealAttemptChance_(0.4),
      maxStealAmount_(maxStealAmount),
      bartAccountId_(0),
      apuAccountId_(0),
      apu_(apu),
      rng_(std::random_device{}())
{
}

void Nelson::Step()
{
    std::cout << "\n--- Ход " << name_ << " ---" << std::endl;

    // Try to steal from Bart (random chance)
    std::uniform_real_distribution<double> chance_dist(0.0, 1.0);
    if (chance_dist(rng_) < stealAttemptChance_)
    {
        std::uniform_int_distribution<Money> steal_dist(10, maxStealAmount_);
        Money stealAmount = steal_dist(rng_);
        std::cout << "  Нельсон пытается украсть " << stealAmount
                  << " у Барта (но это симуляция!)" << std::endl;
    }

    // Buy cigarettes from Apu with whatever cash Nelson has
    if (cashHeld_ >= 20)
    {
        Money spent = 20;
        cashHeld_ -= spent;
        if (apu_)
        {
            apu_->ReceiveCashPayment(spent);
        }
        std::cout << "  Нельсон покупает сигареты у Апу за " << spent << std::endl;
    }
}

// ===== SNAKE (BONUS) =====

Snake::Snake(Bank* bank, Apu* apu, Money maxHackAmount)
    : Actor("Snake", bank, 0),
      hackChance_(0.3),
      maxHackAmount_(maxHackAmount),
      homerAccountId_(0),
      apuAccountId_(0),
      apu_(apu),
      rng_(std::random_device{}())
{
}

void Snake::Step()
{
    std::cout << "\n--- Ход " << name_ << " ---" << std::endl;

    // Try to hack Homer's account (random chance)
    std::uniform_real_distribution<double> chance_dist(0.0, 1.0);
    if (chance_dist(rng_) < hackChance_ && homerAccountId_ != 0)
    {
        try
        {
            Money homerBalance = bank_->GetAccountBalance(homerAccountId_);
            if (homerBalance > 0)
            {
                std::uniform_int_distribution<Money> hack_dist(10, 
                    std::min(maxHackAmount_, homerBalance / 2));
                Money hackAmount = hack_dist(rng_);
                
                if (bank_->TrySendMoney(homerAccountId_, accountId_, hackAmount))
                {
                    cashHeld_ += hackAmount;
                    std::cout << "  Снейк взламывает счет Гомера и крадет "
                              << hackAmount << std::endl;
                }
            }
        }
        catch (const std::exception& e)
        {
            // Hack attempt failed
            std::cout << "  Взлом Снейка не удался" << std::endl;
        }
    }

    // Buy from Apu with cash
    if (cashHeld_ >= 30 && apu_)
    {
        try
        {
            Money spent = 30;
            cashHeld_ -= spent;
            apu_->ReceiveCashPayment(spent);
            std::cout << "  Снейк покупает у Апу за " << spent << " наличными" << std::endl;
        }
        catch (const std::exception& e)
        {
            std::cout << "  Снейк: Покупка не удалась: " << e.what() << std::endl;
        }
    }
}

// ===== SMITHERS (BONUS) =====

Smithers::Smithers(Bank* bank, AccountId burnsAccountId, AccountId apuAccountId)
    : Actor("Smithers", bank, 0),
      salaryPerStep_(500),
      burnsAccountId_(burnsAccountId),
      apuAccountId_(apuAccountId),
      groceryExpensePerStep_(80),
      reopenAccountChance_(0.1),
      rng_(std::random_device{}())
{
}

void Smithers::Step()
{
    std::cout << "\n--- " << name_ << "'s turn ---" << std::endl;

    // Randomly close and reopen account (paranoia)
    std::uniform_real_distribution<double> chance_dist(0.0, 1.0);
    if (chance_dist(rng_) < reopenAccountChance_)
    {
        try
        {
            Money balance = bank_->CloseAccount(accountId_);
            accountId_ = bank_->OpenAccount();
            if (balance > 0)
            {
                bank_->DepositMoney(accountId_, balance);
            }
            std::cout << "  Smithers closes and reopens account (paranoia)" << std::endl;
        }
        catch (const std::exception& e)
        {
            std::cout << "  Smithers: Account manipulation failed: " << e.what() << std::endl;
        }
    }

    // Try to buy groceries from Apu
    try
    {
        if (bank_->GetAccountBalance(accountId_) >= groceryExpensePerStep_)
        {
            bank_->SendMoney(accountId_, apuAccountId_, groceryExpensePerStep_);
            std::cout << "  Smithers buys groceries from Apu for "
                      << groceryExpensePerStep_ << std::endl;
        }
        else
        {
            std::cout << "  Smithers: Not enough funds for groceries" << std::endl;
        }
    }
    catch (const std::exception& e)
    {
        std::cout << "  Smithers: Purchase failed: " << e.what() << std::endl;
    }
}
