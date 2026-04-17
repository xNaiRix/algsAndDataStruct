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
    std::cout << "  " << name_ << ": Cash=" << cashHeld_;
    try
    {
        std::cout << ", Account Balance=" << bank_->GetAccountBalance(accountId_);
    }
    catch (const BankOperationError&)
    {
        std::cout << ", Account=CLOSED";
    }
    std::cout << ", Total=" << GetTotalMoney() << std::endl;
}

// ===== HOMER SIMPSON =====

Homer::Homer(Bank* bank)
    : Actor("Homer", bank, 0),
      salaryPerStep_(1000),
      transferToMargePerStep_(300),
      electricityBillPerStep_(200),
      cashToChildrenPerStep_(100)
{
}

void Homer::Step()
{
    std::cout << "\n--- " << name_ << "'s turn ---" << std::endl;

    // Receive salary from Burns (happens in Burns' step)
    // So we just have cash here

    // Try to transfer money to Marge via bank
    try
    {
        if (cashHeld_ >= transferToMargePerStep_)
        {
            bank_->DepositMoney(accountId_, transferToMargePerStep_);
            cashHeld_ -= transferToMargePerStep_;
            std::cout << "  Homer transfers " << transferToMargePerStep_
                      << " to Marge's account" << std::endl;
        }
        else
        {
            std::cout << "  Homer: Not enough cash to transfer to Marge" << std::endl;
        }
    }
    catch (const std::exception& e)
    {
        std::cout << "  Homer: Transfer to Marge failed: " << e.what() << std::endl;
    }

    // Pay electricity bill
    try
    {
        if (cashHeld_ >= electricityBillPerStep_)
        {
            bank_->DepositMoney(accountId_, electricityBillPerStep_);
            cashHeld_ -= electricityBillPerStep_;
            std::cout << "  Homer pays " << electricityBillPerStep_
                      << " for electricity" << std::endl;
        }
        else
        {
            std::cout << "  Homer: Not enough cash to pay electricity" << std::endl;
        }
    }
    catch (const std::exception& e)
    {
        std::cout << "  Homer: Electricity payment failed: " << e.what() << std::endl;
    }

    // Give cash to children
    try
    {
        if (cashHeld_ >= cashToChildrenPerStep_)
        {
            cashHeld_ -= cashToChildrenPerStep_;
            std::cout << "  Homer gives " << cashToChildrenPerStep_
                      << " cash to children" << std::endl;
        }
        else
        {
            std::cout << "  Homer: Not enough cash for children" << std::endl;
        }
    }
    catch (const std::exception& e)
    {
        std::cout << "  Homer: Failed to give cash to children: " << e.what() << std::endl;
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
    std::cout << "\n--- " << name_ << "'s turn ---" << std::endl;

    // Buy groceries from Apu via bank transfer
    try
    {
        if (bank_->GetAccountBalance(accountId_) >= groceryExpensePerStep_)
        {
            bank_->SendMoney(accountId_, apuAccountId_, groceryExpensePerStep_);
            std::cout << "  Marge buys groceries from Apu for " << groceryExpensePerStep_
                      << " via transfer" << std::endl;
        }
        else
        {
            std::cout << "  Marge: Not enough funds in account for groceries" << std::endl;
        }
    }
    catch (const std::exception& e)
    {
        std::cout << "  Marge: Grocery purchase failed: " << e.what() << std::endl;
    }
}

// ===== BART SIMPSON =====

Bart::Bart(Bank* bank, AccountId apuAccountId)
    : Actor("Bart", bank, 0),
      spendingPerStep_(30),
      apuAccountId_(apuAccountId),
      rng_(std::random_device{}())
{
}

void Bart::Step()
{
    std::cout << "\n--- " << name_ << "'s turn ---" << std::endl;

    // Randomly decide to spend some cash on Apu's store
    std::uniform_int_distribution<int> spend_dist(0, 100);
    if (spend_dist(rng_) < 60)  // 60% chance to buy something
    {
        Money amount = 5 + (spend_dist(rng_) % 20);  // Random amount 5-25
        if (cashHeld_ >= amount)
        {
            cashHeld_ -= amount;
            std::cout << "  Bart buys something from Apu for " << amount
                      << " cash" << std::endl;
        }
    }
}

// ===== LISA SIMPSON =====

Lisa::Lisa(Bank* bank, AccountId apuAccountId)
    : Actor("Lisa", bank, 0),
      spendingPerStep_(20),
      apuAccountId_(apuAccountId),
      rng_(std::random_device{}())
{
}

void Lisa::Step()
{
    std::cout << "\n--- " << name_ << "'s turn ---" << std::endl;

    // Randomly decide to spend some cash on Apu's store (less often than Bart)
    std::uniform_int_distribution<int> spend_dist(0, 100);
    if (spend_dist(rng_) < 40)  // 40% chance to buy something
    {
        Money amount = 5 + (spend_dist(rng_) % 15);  // Random amount 5-20
        if (cashHeld_ >= amount)
        {
            cashHeld_ -= amount;
            std::cout << "  Lisa buys something from Apu for " << amount
                      << " cash" << std::endl;
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
    std::cout << "\n--- " << name_ << "'s turn ---" << std::endl;

    // Try to pay electricity bill to Burns
    try
    {
        if (bank_->GetAccountBalance(accountId_) >= electricityBillPerStep_)
        {
            bank_->SendMoney(accountId_, burnsAccountId_, electricityBillPerStep_);
            std::cout << "  Apu pays " << electricityBillPerStep_
                      << " for electricity to Burns" << std::endl;
        }
        else if (cashHeld_ >= electricityBillPerStep_)
        {
            // Can pay with cash from customer sales
            bank_->DepositMoney(accountId_, electricityBillPerStep_);
            cashHeld_ -= electricityBillPerStep_;
            bank_->SendMoney(accountId_, burnsAccountId_, electricityBillPerStep_);
            std::cout << "  Apu deposits and pays electricity bill" << std::endl;
        }
        else
        {
            std::cout << "  Apu: Not enough funds to pay electricity" << std::endl;
        }
    }
    catch (const std::exception& e)
    {
        std::cout << "  Apu: Electricity payment failed: " << e.what() << std::endl;
    }

    // Deposit cash to account if it exceeds threshold
    if (cashHeld_ > depositThresholdCash_)
    {
        try
        {
            Money depositAmount = cashHeld_ - (depositThresholdCash_ / 2);
            bank_->DepositMoney(accountId_, depositAmount);
            cashHeld_ -= depositAmount;
            std::cout << "  Apu deposits " << depositAmount << " cash to bank" << std::endl;
        }
        catch (const std::exception& e)
        {
            std::cout << "  Apu: Deposit failed: " << e.what() << std::endl;
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
    std::cout << "\n--- " << name_ << "'s turn ---" << std::endl;

    // Receive revenue from electricity sales (just add to account)
    try
    {
        bank_->DepositMoney(accountId_, revenuePerStep_);
        cashHeld_ += revenuePerStep_;  // Actually get cash, not deposit
        std::cout << "  Burns receives " << revenuePerStep_
                  << " from electricity sales" << std::endl;
    }
    catch (const std::exception& e)
    {
        std::cout << "  Burns: Revenue collection failed: " << e.what() << std::endl;
    }

    // Pay Homer's salary
    try
    {
        if (cashHeld_ >= salaryForHomer_)
        {
            cashHeld_ -= salaryForHomer_;
            // Give Homer cash directly (not via bank)
            // This will be handled in a separate step
            std::cout << "  Burns gives " << salaryForHomer_
                      << " salary to Homer (as cash)" << std::endl;
        }
    }
    catch (const std::exception& e)
    {
        std::cout << "  Burns: Salary payment failed: " << e.what() << std::endl;
    }
}

void Burns::ReceiveElectricityPayment(Money amount)
{
    cashHeld_ += amount;
}

// ===== NELSON (BONUS) =====

Nelson::Nelson(Bank* bank, Money maxStealAmount)
    : Actor("Nelson", bank, 0),
      stealAttemptChance_(0.4),
      maxStealAmount_(maxStealAmount),
      apuAccountId_(0),
      rng_(std::random_device{}())
{
}

void Nelson::Step()
{
    std::cout << "\n--- " << name_ << "'s turn ---" << std::endl;

    // Try to steal from Bart (random chance)
    std::uniform_real_distribution<double> chance_dist(0.0, 1.0);
    if (chance_dist(rng_) < stealAttemptChance_)
    {
        std::uniform_int_distribution<Money> steal_dist(10, maxStealAmount_);
        Money stealAmount = steal_dist(rng_);
        std::cout << "  Nelson tries to steal " << stealAmount
                  << " from Bart (but this is a simulation!)" << std::endl;
    }

    // Buy cigarettes from Apu with whatever cash Nelson has
    if (cashHeld_ >= 20)
    {
        Money spent = 20;
        cashHeld_ -= spent;
        std::cout << "  Nelson buys cigarettes from Apu for " << spent << std::endl;
    }
}

// ===== SNAKE (BONUS) =====

Snake::Snake(Bank* bank, Money maxHackAmount)
    : Actor("Snake", bank, 0),
      hackChance_(0.3),
      maxHackAmount_(maxHackAmount),
      homerAccountId_(0),
      apuAccountId_(0),
      rng_(std::random_device{}())
{
}

void Snake::Step()
{
    std::cout << "\n--- " << name_ << "'s turn ---" << std::endl;

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
                    std::cout << "  Snake hacks Homer's account and steals "
                              << hackAmount << std::endl;
                }
            }
        }
        catch (const std::exception& e)
        {
            // Hack attempt failed
            std::cout << "  Snake's hack failed" << std::endl;
        }
    }

    // Buy from Apu with cash
    if (cashHeld_ >= 30 && apuAccountId_ != 0)
    {
        try
        {
            Money spent = 30;
            cashHeld_ -= spent;
            std::cout << "  Snake buys from Apu for " << spent << " cash" << std::endl;
        }
        catch (const std::exception& e)
        {
            std::cout << "  Snake: Purchase failed: " << e.what() << std::endl;
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
