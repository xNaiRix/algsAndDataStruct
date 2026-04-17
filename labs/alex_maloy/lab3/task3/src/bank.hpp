#ifndef BANK_HPP
#define BANK_HPP

#include <unordered_map>
#include <stdexcept>

using AccountId = unsigned long long;
using Money = long long;

// Exception for bank operation errors
class BankOperationError : public std::runtime_error
{
public:
    using std::runtime_error::runtime_error;
};

// Main bank class that manages all money (cash and account-based)
class Bank
{
private:
    Money cash_;  // Cash in circulation
    std::unordered_map<AccountId, Money> accounts_;  // Bank accounts
    AccountId nextAccountId_;  // Counter for generating unique account IDs

public:
    // Constructor: initializes monetary system with initial cash
    // Throws BankOperationError if cash is negative
    explicit Bank(Money cash);

    // Non-copyable
    Bank(const Bank&) = delete;
    Bank& operator=(const Bank&) = delete;

    // Send money from source account to destination account
    // Throws BankOperationError if accounts don't exist or insufficient funds
    // Throws std::out_of_range if amount is negative
    // Provides strong exception guarantee
    void SendMoney(AccountId srcAccountId, AccountId dstAccountId, Money amount);

    // Try to send money (non-throwing variant)
    // Returns false if insufficient funds or invalid accounts
    // Throws BankOperationError if account IDs are invalid
    // Throws std::out_of_range if amount is negative
    // Provides strong exception guarantee
    [[nodiscard]] bool TrySendMoney(AccountId srcAccountId, AccountId dstAccountId, Money amount);

    // Get current cash in circulation
    [[nodiscard]] Money GetCash() const;

    // Get balance of an account
    // Throws BankOperationError if account doesn't exist
    [[nodiscard]] Money GetAccountBalance(AccountId accountId) const;

    // Withdraw money from account to cash
    // Throws BankOperationError if account doesn't exist or insufficient funds
    // Throws std::out_of_range if amount is negative
    // Provides strong exception guarantee
    void WithdrawMoney(AccountId account, Money amount);

    // Try to withdraw money (non-throwing variant for insufficient funds)
    // Returns false if insufficient funds
    // Throws BankOperationError if account ID is invalid
    // Throws std::out_of_range if amount is negative
    // Provides strong exception guarantee
    [[nodiscard]] bool TryWithdrawMoney(AccountId account, Money amount);

    // Deposit cash to account
    // Throws BankOperationError if account doesn't exist or insufficient cash
    // Throws std::out_of_range if amount is negative
    // Provides strong exception guarantee
    void DepositMoney(AccountId account, Money amount);

    // Open a new account with zero balance
    // Returns the account ID
    [[nodiscard]] AccountId OpenAccount();

    // Close an account and return its balance to cash
    // Returns the amount that was on the account
    // Throws BankOperationError if account doesn't exist
    [[nodiscard]] Money CloseAccount(AccountId accountId);

    // Helper method to get total money in system (for verification)
    [[nodiscard]] Money GetTotalMoney() const;

    // Helper method to get total account money (for verification)
    [[nodiscard]] Money GetTotalAccountBalance() const;
};

#endif  // BANK_HPP
