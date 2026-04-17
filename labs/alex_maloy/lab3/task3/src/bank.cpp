#include "bank.hpp"
#include <iostream>

Bank::Bank(Money cash)
    : cash_(cash), nextAccountId_(1)
{
    if (cash < 0)
    {
        throw BankOperationError("Initial cash cannot be negative");
    }
}

void Bank::SendMoney(AccountId srcAccountId, AccountId dstAccountId, Money amount)
{
    // Check for negative amount
    if (amount < 0)
    {
        throw std::out_of_range("Cannot send negative amount of money");
    }

    // Check if accounts exist
    auto srcIt = accounts_.find(srcAccountId);
    auto dstIt = accounts_.find(dstAccountId);
    
    if (srcIt == accounts_.end())
    {
        throw BankOperationError("Source account does not exist");
    }
    if (dstIt == accounts_.end())
    {
        throw BankOperationError("Destination account does not exist");
    }

    // Check if source has enough funds
    if (srcIt->second < amount)
    {
        throw BankOperationError("Insufficient funds in source account");
    }

    // Perform transaction (strong guarantee: withdraw happens before deposit)
    // If deposit fails for some reason, we haven't modified source account yet
    dstIt->second += amount;
    try
    {
        srcIt->second -= amount;
    }
    catch (...)
    {
        // Rollback: restore destination account to original state
        dstIt->second -= amount;
        throw;
    }
}

bool Bank::TrySendMoney(AccountId srcAccountId, AccountId dstAccountId, Money amount)
{
    // Check for negative amount
    if (amount < 0)
    {
        throw std::out_of_range("Cannot send negative amount of money");
    }

    // Check if accounts exist
    auto srcIt = accounts_.find(srcAccountId);
    auto dstIt = accounts_.find(dstAccountId);
    
    if (srcIt == accounts_.end())
    {
        throw BankOperationError("Source account does not exist");
    }
    if (dstIt == accounts_.end())
    {
        throw BankOperationError("Destination account does not exist");
    }

    // Check if source has enough funds
    if (srcIt->second < amount)
    {
        return false;
    }

    // Perform transaction
    dstIt->second += amount;
    try
    {
        srcIt->second -= amount;
    }
    catch (...)
    {
        // Rollback
        dstIt->second -= amount;
        throw;
    }

    return true;
}

Money Bank::GetCash() const
{
    return cash_;
}

Money Bank::GetAccountBalance(AccountId accountId) const
{
    auto it = accounts_.find(accountId);
    if (it == accounts_.end())
    {
        throw BankOperationError("Account does not exist");
    }
    return it->second;
}

void Bank::WithdrawMoney(AccountId account, Money amount)
{
    // Check for negative amount
    if (amount < 0)
    {
        throw std::out_of_range("Cannot withdraw negative amount of money");
    }

    // Check if account exists
    auto it = accounts_.find(account);
    if (it == accounts_.end())
    {
        throw BankOperationError("Account does not exist");
    }

    // Check if account has enough funds
    if (it->second < amount)
    {
        throw BankOperationError("Insufficient funds in account");
    }

    // Perform withdrawal (strong guarantee: we first check everything, then modify)
    it->second -= amount;
    try
    {
        cash_ += amount;
    }
    catch (...)
    {
        // Rollback
        it->second += amount;
        throw;
    }
}

bool Bank::TryWithdrawMoney(AccountId account, Money amount)
{
    // Check for negative amount
    if (amount < 0)
    {
        throw std::out_of_range("Cannot withdraw negative amount of money");
    }

    // Check if account exists
    auto it = accounts_.find(account);
    if (it == accounts_.end())
    {
        throw BankOperationError("Account does not exist");
    }

    // Check if account has enough funds
    if (it->second < amount)
    {
        return false;
    }

    // Perform withdrawal
    it->second -= amount;
    try
    {
        cash_ += amount;
    }
    catch (...)
    {
        // Rollback
        it->second += amount;
        throw;
    }

    return true;
}

void Bank::DepositMoney(AccountId account, Money amount)
{
    // Check for negative amount
    if (amount < 0)
    {
        throw std::out_of_range("Cannot deposit negative amount of money");
    }

    // Check if account exists
    auto it = accounts_.find(account);
    if (it == accounts_.end())
    {
        throw BankOperationError("Account does not exist");
    }

    // Check if there is enough cash
    if (cash_ < amount)
    {
        throw BankOperationError("Insufficient cash in circulation");
    }

    // Perform deposit (strong guarantee: we first check everything, then modify)
    cash_ -= amount;
    try
    {
        it->second += amount;
    }
    catch (...)
    {
        // Rollback
        cash_ += amount;
        throw;
    }
}

AccountId Bank::OpenAccount()
{
    AccountId newId = nextAccountId_++;
    accounts_[newId] = 0;  // New account has zero balance
    return newId;
}

Money Bank::CloseAccount(AccountId accountId)
{
    auto it = accounts_.find(accountId);
    if (it == accounts_.end())
    {
        throw BankOperationError("Account does not exist");
    }

    Money balance = it->second;
    accounts_.erase(it);
    
    try
    {
        cash_ += balance;
    }
    catch (...)
    {
        // If cash_ += fails (unlikely with integers), we need to restore the account
        accounts_[accountId] = balance;
        throw;
    }

    return balance;
}

Money Bank::GetTotalMoney() const
{
    Money total = cash_;
    for (const auto& account : accounts_)
    {
        total += account.second;
    }
    return total;
}

Money Bank::GetTotalAccountBalance() const
{
    Money total = 0;
    for (const auto& account : accounts_)
    {
        total += account.second;
    }
    return total;
}
