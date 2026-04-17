#include "bank.hpp"
#include "actors.hpp"
#include "economy.hpp"
#include <iostream>
#include <cassert>
#include <sstream>
#include <iomanip>

// Test counters
int testsRun = 0;
int testsPassed = 0;
int testsFailed = 0;

// Helper function to print test results
void PrintTestResult(const std::string& testName, bool passed)
{
    testsRun++;
    if (passed)
    {
        testsPassed++;
        std::cout << "✓ PASS: " << testName << std::endl;
    }
    else
    {
        testsFailed++;
        std::cout << "✗ FAIL: " << testName << std::endl;
    }
}

// ===== BANK TESTS =====

void TestBankInitialization()
{
    std::cout << "\n========== BANK INITIALIZATION TESTS ==========" << std::endl;

    // Test valid initialization
    Bank bank(1000);
    PrintTestResult("Bank initialized with positive cash", bank.GetCash() == 1000);

    // Test invalid initialization
    try
    {
        Bank negativeBank(-100);
        PrintTestResult("Bank initialization with negative cash throws", false);
    }
    catch (const BankOperationError& e)
    {
        PrintTestResult("Bank initialization with negative cash throws", true);
    }
}

void TestAccountManagement()
{
    std::cout << "\n========== ACCOUNT MANAGEMENT TESTS ==========" << std::endl;
    Bank bank(1000);

    // Test account opening
    AccountId acc1 = bank.OpenAccount();
    PrintTestResult("Account opens successfully", acc1 > 0);

    // Test initial balance is zero
    PrintTestResult("New account has zero balance", bank.GetAccountBalance(acc1) == 0);

    // Test multiple accounts
    AccountId acc2 = bank.OpenAccount();
    AccountId acc3 = bank.OpenAccount();
    PrintTestResult("Multiple accounts have unique IDs", acc1 != acc2 && acc2 != acc3);

    // Test getting non-existent account balance
    try
    {
        bank.GetAccountBalance(99999);
        PrintTestResult("Getting non-existent account throws", false);
    }
    catch (const BankOperationError&)
    {
        PrintTestResult("Getting non-existent account throws", true);
    }
}

void TestDepositAndWithdraw()
{
    std::cout << "\n========== DEPOSIT AND WITHDRAW TESTS ==========" << std::endl;
    Bank bank(1000);
    AccountId acc = bank.OpenAccount();

    // Test deposit
    bank.DepositMoney(acc, 500);
    PrintTestResult("Deposit reduces cash", bank.GetCash() == 500);
    PrintTestResult("Deposit increases account balance", bank.GetAccountBalance(acc) == 500);

    // Test withdraw
    bank.WithdrawMoney(acc, 300);
    PrintTestResult("Withdraw increases cash", bank.GetCash() == 800);
    PrintTestResult("Withdraw reduces account balance", bank.GetAccountBalance(acc) == 200);

    // Test withdraw more than available
    try
    {
        bank.WithdrawMoney(acc, 300);
        PrintTestResult("Withdraw more than balance throws", false);
    }
    catch (const BankOperationError&)
    {
        PrintTestResult("Withdraw more than balance throws", true);
    }

    // Test deposit more than cash available
    try
    {
        bank.DepositMoney(acc, 1000);
        PrintTestResult("Deposit more than cash available throws", false);
    }
    catch (const BankOperationError&)
    {
        PrintTestResult("Deposit more than cash available throws", true);
    }

    // Test negative deposit
    try
    {
        bank.DepositMoney(acc, -100);
        PrintTestResult("Negative deposit throws", false);
    }
    catch (const std::out_of_range&)
    {
        PrintTestResult("Negative deposit throws", true);
    }

    // Test negative withdraw
    try
    {
        bank.WithdrawMoney(acc, -100);
        PrintTestResult("Negative withdraw throws", false);
    }
    catch (const std::out_of_range&)
    {
        PrintTestResult("Negative withdraw throws", true);
    }
}

void TestTryOperations()
{
    std::cout << "\n========== TRY OPERATIONS TESTS ==========" << std::endl;
    Bank bank(1000);
    AccountId acc = bank.OpenAccount();

    // Test TryWithdrawMoney - success case
    bank.DepositMoney(acc, 500);
    bool result = bank.TryWithdrawMoney(acc, 200);
    PrintTestResult("TryWithdrawMoney returns true on success", result);
    PrintTestResult("TryWithdrawMoney succeeds", bank.GetAccountBalance(acc) == 300);

    // Test TryWithdrawMoney - failure case
    result = bank.TryWithdrawMoney(acc, 500);
    PrintTestResult("TryWithdrawMoney returns false on insufficient funds", !result);
    PrintTestResult("TryWithdrawMoney doesn't modify balance on failure", bank.GetAccountBalance(acc) == 300);

    // Test TryWithdrawMoney - invalid account
    try
    {
        bank.TryWithdrawMoney(99999, 100);
        PrintTestResult("TryWithdrawMoney with invalid account throws", false);
    }
    catch (const BankOperationError&)
    {
        PrintTestResult("TryWithdrawMoney with invalid account throws", true);
    }
}

void TestMoneyTransfer()
{
    std::cout << "\n========== MONEY TRANSFER TESTS ==========" << std::endl;
    Bank bank(1000);
    AccountId acc1 = bank.OpenAccount();
    AccountId acc2 = bank.OpenAccount();

    bank.DepositMoney(acc1, 500);

    // Test basic transfer
    bank.SendMoney(acc1, acc2, 200);
    PrintTestResult("SendMoney reduces source account", bank.GetAccountBalance(acc1) == 300);
    PrintTestResult("SendMoney increases destination account", bank.GetAccountBalance(acc2) == 200);

    // Test transfer more than available
    try
    {
        bank.SendMoney(acc1, acc2, 500);
        PrintTestResult("SendMoney with insufficient funds throws", false);
    }
    catch (const BankOperationError&)
    {
        PrintTestResult("SendMoney with insufficient funds throws", true);
    }

    // Test transfer with invalid source
    try
    {
        bank.SendMoney(99999, acc2, 100);
        PrintTestResult("SendMoney with invalid source throws", false);
    }
    catch (const BankOperationError&)
    {
        PrintTestResult("SendMoney with invalid source throws", true);
    }

    // Test transfer with invalid destination
    try
    {
        bank.SendMoney(acc1, 99999, 100);
        PrintTestResult("SendMoney with invalid destination throws", false);
    }
    catch (const BankOperationError&)
    {
        PrintTestResult("SendMoney with invalid destination throws", true);
    }

    // Test transfer negative amount
    try
    {
        bank.SendMoney(acc1, acc2, -100);
        PrintTestResult("SendMoney with negative amount throws", false);
    }
    catch (const std::out_of_range&)
    {
        PrintTestResult("SendMoney with negative amount throws", true);
    }

    // Test TrySendMoney
    Money originalAcc1 = bank.GetAccountBalance(acc1);
    Money originalAcc2 = bank.GetAccountBalance(acc2);
    bool success = bank.TrySendMoney(acc1, acc2, 100);
    PrintTestResult("TrySendMoney succeeds", success);
    PrintTestResult("TrySendMoney transfers on success", 
        bank.GetAccountBalance(acc1) == originalAcc1 - 100 && 
        bank.GetAccountBalance(acc2) == originalAcc2 + 100);

    success = bank.TrySendMoney(acc1, acc2, 500);
    PrintTestResult("TrySendMoney returns false on insufficient funds", !success);
}

void TestCloseAccount()
{
    std::cout << "\n========== CLOSE ACCOUNT TESTS ==========" << std::endl;
    Bank bank(1000);
    AccountId acc = bank.OpenAccount();

    // Test close empty account
    Money returned = bank.CloseAccount(acc);
    PrintTestResult("CloseAccount returns zero for empty account", returned == 0);
    PrintTestResult("CloseAccount increases cash", bank.GetCash() == 1000);

    // Test close account with balance
    acc = bank.OpenAccount();
    bank.DepositMoney(acc, 300);
    Money previousCash = bank.GetCash();
    returned = bank.CloseAccount(acc);
    PrintTestResult("CloseAccount returns correct balance", returned == 300);
    PrintTestResult("CloseAccount adds balance to cash", bank.GetCash() == previousCash + 300);

    // Test close non-existent account
    try
    {
        bank.CloseAccount(99999);
        PrintTestResult("CloseAccount with non-existent account throws", false);
    }
    catch (const BankOperationError&)
    {
        PrintTestResult("CloseAccount with non-existent account throws", true);
    }

    // Test that closed account can't be accessed
    try
    {
        bank.GetAccountBalance(acc);
        PrintTestResult("Accessing closed account throws", false);
    }
    catch (const BankOperationError&)
    {
        PrintTestResult("Accessing closed account throws", true);
    }
}

void TestMoneyConservation()
{
    std::cout << "\n========== MONEY CONSERVATION TESTS ==========" << std::endl;
    Money initialCash = 5000;
    Bank bank(initialCash);

    AccountId acc1 = bank.OpenAccount();
    AccountId acc2 = bank.OpenAccount();
    AccountId acc3 = bank.OpenAccount();

    // Perform various operations
    bank.DepositMoney(acc1, 1000);
    bank.DepositMoney(acc2, 1500);
    bank.SendMoney(acc1, acc3, 500);
    bank.WithdrawMoney(acc2, 500);
    bank.DepositMoney(acc3, 200);

    // Check total money
    Money totalMoney = bank.GetTotalMoney();
    PrintTestResult("Money is conserved through operations", totalMoney == initialCash);

    // Close accounts and verify
    bank.CloseAccount(acc1);
    bank.CloseAccount(acc2);
    bank.CloseAccount(acc3);
    PrintTestResult("Money conserved after closing accounts", bank.GetTotalMoney() == initialCash);
}

// ===== ACTOR TESTS =====

void TestActorBasics()
{
    std::cout << "\n========== ACTOR BASIC TESTS ==========" << std::endl;
    Bank bank(10000);

    Homer homer(&bank);
    PrintTestResult("Homer created with account", homer.GetAccountId() > 0);
    
    Marge marge(&bank, 0);
    PrintTestResult("Marge created with account", marge.GetAccountId() > 0);

    std::string name = homer.GetName();
    PrintTestResult("Actor has correct name", name == "Homer");
}

void TestActorMoneyTracking()
{
    std::cout << "\n========== ACTOR MONEY TRACKING TESTS ==========" << std::endl;
    Bank bank(10000);

    Homer homer(&bank);
    Money initialCash = 100;
    homer.cashHeld_ = initialCash;

    PrintTestResult("Actor cash tracking works", homer.GetCash() == initialCash);
    
    // Deposit some to bank
    bank.DepositMoney(homer.GetAccountId(), 50);
    homer.cashHeld_ -= 50;

    Money totalMoney = homer.GetTotalMoney();
    PrintTestResult("Actor total money includes cash and account", 
        totalMoney == initialCash);
}

// ===== ECONOMY TESTS =====

void TestEconomyInitialization()
{
    std::cout << "\n========== ECONOMY INITIALIZATION TESTS ==========" << std::endl;

    Economy economy(10000, false);  // Without bonus actors
    PrintTestResult("Economy created successfully", true);
    PrintTestResult("Economy has correct initial money", 
        economy.GetBank().GetTotalMoney() == 10000);
}

void TestEconomyWithBonusActors()
{
    std::cout << "\n========== ECONOMY WITH BONUS ACTORS TESTS ==========" << std::endl;

    Economy economy(15000, true);  // With bonus actors
    PrintTestResult("Economy created with bonus actors", true);
    PrintTestResult("All money conserved with bonus actors", 
        economy.GetBank().GetTotalMoney() == 15000);
}

void TestEconomySimulation()
{
    std::cout << "\n========== ECONOMY SIMULATION TESTS ==========" << std::endl;

    Economy economy(10000, false);  // Simpler test without bonusactors
    
    try
    {
        economy.Step();
        PrintTestResult("Economy step executes without error", true);
    }
    catch (const std::exception& e)
    {
        PrintTestResult("Economy step executes without error", false);
        std::cout << "  Exception: " << e.what() << std::endl;
    }

    PrintTestResult("Money conserved after one step", 
        economy.GetBank().GetTotalMoney() == 10000);
}

void TestEconomyConsistency()
{
    std::cout << "\n========== ECONOMY CONSISTENCY TESTS ==========" << std::endl;

    Economy economy(10000, false);
    
    // Run several steps
    try
    {
        for (int i = 0; i < 5; ++i)
        {
            economy.Step();
        }
        PrintTestResult("Economy runs multiple steps", true);
    }
    catch (const std::exception& e)
    {
        PrintTestResult("Economy runs multiple steps", false);
        std::cout << "  Exception: " << e.what() << std::endl;
    }

    bool consistent = economy.VerifyConsistency();
    PrintTestResult("Economy remains consistent after steps", consistent);
}

void TestExceptionSafety()
{
    std::cout << "\n========== EXCEPTION SAFETY TESTS ==========" << std::endl;
    Bank bank(1000);
    AccountId acc1 = bank.OpenAccount();
    AccountId acc2 = bank.OpenAccount();

    bank.DepositMoney(acc1, 500);
    Money acc1BalanceBefore = bank.GetAccountBalance(acc1);
    Money acc2BalanceBefore = bank.GetAccountBalance(acc2);

    // Try invalid transfer that should fail and rollback
    try
    {
        bank.SendMoney(acc1, 99999, 200);  // Invalid destination
    }
    catch (const BankOperationError&)
    {
        // Expected
    }

    Money acc1BalanceAfter = bank.GetAccountBalance(acc1);
    Money acc2BalanceAfter = bank.GetAccountBalance(acc2);

    PrintTestResult("Failed transfer doesn't modify source (strong guarantee)", 
        acc1BalanceBefore == acc1BalanceAfter);
    PrintTestResult("Failed transfer doesn't modify destination", 
        acc2BalanceBefore == acc2BalanceAfter);
}

// ===== MAIN TEST RUNNER =====

int main()
{
    std::cout << "======================================" << std::endl;
    std::cout << "    ECONOMY SIMULATION TEST SUITE    " << std::endl;
    std::cout << "======================================" << std::endl;

    // Bank tests
    TestBankInitialization();
    TestAccountManagement();
    TestDepositAndWithdraw();
    TestTryOperations();
    TestMoneyTransfer();
    TestCloseAccount();
    TestMoneyConservation();

    // Actor tests
    TestActorBasics();
    TestActorMoneyTracking();

    // Economy tests
    TestEconomyInitialization();
    TestEconomyWithBonusActors();
    TestEconomySimulation();
    TestEconomyConsistency();

    // Exception safety tests
    TestExceptionSafety();

    // Final summary
    std::cout << "\n======================================" << std::endl;
    std::cout << "         TEST RESULTS SUMMARY        " << std::endl;
    std::cout << "======================================" << std::endl;
    std::cout << "Total tests: " << testsRun << std::endl;
    std::cout << "Passed: " << testsPassed << " (" << (100 * testsPassed / testsRun) << "%)" << std::endl;
    std::cout << "Failed: " << testsFailed << std::endl;

    if (testsFailed == 0)
    {
        std::cout << "\n✓✓✓ ALL TESTS PASSED ✓✓✓" << std::endl;
        return 0;
    }
    else
    {
        std::cout << "\n✗✗✗ SOME TESTS FAILED ✗✗✗" << std::endl;
        return 1;
    }
}
