#ifndef ACTORS_HPP
#define ACTORS_HPP

#include "bank.hpp"
#include <string>
#include <random>

class Apu;

// Base actor class
class Actor
{
protected:
    std::string name_;
    AccountId accountId_;
    Bank* bank_;

public:
    Money cashHeld_;  // Public for easy access during simulation

    Actor(const std::string& name, Bank* bank, Money initialCash = 0);
    virtual ~Actor() = default;

    // Simulate one step of the actor's behavior
    virtual void Step() = 0;

    // Get actor's name
    const std::string& GetName() const;

    // Get actor's cash on hand
    Money GetCash() const;

    // Get actor's account ID
    AccountId GetAccountId() const;

    // Get total money (cash + bank account)
    Money GetTotalMoney() const;

    // Receive cash payment (public for economy simulation)
    virtual void ReceiveCashPayment(Money amount);

    // Print status
    virtual void PrintStatus() const;
};

// Homer Simpson - father of the family
class Homer : public Actor
{
private:
    Money salaryPerStep_;
    Money transferToMargePerStep_;
    Money electricityBillPerStep_;
    Money cashToChildrenPerStep_;
    Actor* bart_;
    Actor* lisa_;

public:
    Homer(Bank* bank);
    void SetChildren(Actor* bart, Actor* lisa);
    void Step() override;
};

// Marge Simpson - housewife
class Marge : public Actor
{
private:
    Money groceryExpensePerStep_;
    AccountId apuAccountId_;

public:
    Marge(Bank* bank, AccountId apuAccountId);
    void Step() override;
};

// Bart Simpson - son
class Bart : public Actor
{
private:
    Money spendingPerStep_;
    Apu* apu_;
    std::mt19937 rng_;

public:
    Bart(Bank* bank, Apu* apu);
    void Step() override;
};

// Lisa Simpson - daughter
class Lisa : public Actor
{
private:
    Money spendingPerStep_;
    Apu* apu_;
    std::mt19937 rng_;

public:
    Lisa(Bank* bank, Apu* apu);
    void Step() override;
};

// Apu Nahasapeemapetilon - market owner
class Apu : public Actor
{
private:
    Money electricityBillPerStep_;
    AccountId burnsAccountId_;
    Money depositThresholdCash_;  // Deposit to bank when cash exceeds this

public:
    Apu(Bank* bank, AccountId burnsAccountId);
    void Step() override;

    // Receive payment from customers
    void ReceiveCashPayment(Money amount);
};

// Mr. Burns - power plant owner
class Burns : public Actor
{
private:
    Money revenuePerStep_;  // Revenue from electricity sales
    AccountId homerAccountId_;
    Money salaryForHomer_;

public:
    Burns(Bank* bank, AccountId homerAccountId);
    void Step() override;

    // Receive payment for electricity
    void ReceiveElectricityPayment(Money amount);
};

// ===== BONUS CHARACTERS =====

// Nelson - bully, steals cash
class Nelson : public Actor
{
public:
    Money stealAttemptChance_;  // 0.0 to 1.0
    Money maxStealAmount_;
    AccountId bartAccountId_;  // Actually we steal cash, not account
    AccountId apuAccountId_;

private:
    Apu* apu_;
    std::mt19937 rng_;

public:
    Nelson(Bank* bank, Apu* apu, Money maxStealAmount = 50);
    void Step() override;
};

// Snake - criminal, hacks accounts
class Snake : public Actor
{
public:
    Money hackChance_;  // 0.0 to 1.0
    Money maxHackAmount_;
    AccountId homerAccountId_;
    AccountId apuAccountId_;

private:
    Apu* apu_;
    std::mt19937 rng_;

public:
    Snake(Bank* bank, Apu* apu, Money maxHackAmount = 100);
    void Step() override;
};

// Waylon Smithers - Burns' assistant, paranoid about banking
class Smithers : public Actor
{
private:
    Money salaryPerStep_;
    AccountId burnsAccountId_;
    AccountId apuAccountId_;
    Money groceryExpensePerStep_;
    Money reopenAccountChance_;  // How often to close and reopen account
    std::mt19937 rng_;

public:
    Smithers(Bank* bank, AccountId burnsAccountId, AccountId apuAccountId);
    void Step() override;
};

#endif  // ACTORS_HPP
