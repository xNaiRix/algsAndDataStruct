import logging

def get_logger():
    logger = logging.getLogger("logs")
    logger.setLevel(logging.DEBUG)

    detailed_format = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")
    simple_format = logging.Formatter("%(levelname)s: %(message)s")
    
    file_handler = logging.FileHandler("Transactions.logs", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_format)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(simple_format)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


class MyException(Exception):
    pass


class TransactionException(MyException):
    pass


class NotValidBankAccountError(TransactionException):
    def __init__(self, bank_account):
        super().__init__()
        self.bank_account = bank_account
    def __str__(self):
        return f"Bank account \'{self.bank_account}\' is invalid"


class NoResultError(TransactionException):
    def __str__(self):
        return "Transaction failed"


class IncorrectAddressError(TransactionException):
    def __init__(self,where):
        super().__init__()
        self.where=where
    def __str__(self):
        return f"cannot find address \'{self.where}\' in database"


class NegativeAmountError(TransactionException):
    def __init__(self,amount):
        super().__init__()
        self.amount = amount
    def __str__(self):
        return f"amount \'{self.amount}'\ cannot be negative"


class NotEnoughMoneyError(TransactionException):
    def __init__(self, amount, amount_left):
        super().__init__()
        self.amount=amount
        self.amount_left=amount_left

    def __str__(self):
        return f"You tried to make a transaction for {self.amount} when you have only {self.amount_left}"


data_base = {
    'addresses': ['Рекордов 15', 'Олимпийский проспект 1'],
    'amount_left': 100
}
logger = get_logger()

def valid(bank_account):
    return True


# Add exceptions here
def make_transaction(bank_account):
    # Some request
    if not valid(bank_account):
        raise NotValidBankAccountError(bank_account=bank_account)

    result = False
    if not result:
        raise NoResultError()


# Add exceptions here
def order_items(where, amount, bank_account):
    try:
        if where not in data_base['addresses']:
            raise IncorrectAddressError(where=where)
        if amount <= 0:
            raise NegativeAmountError(amount=amount)
        amount_left = data_base['amount_left']
        if amount > amount_left:
            raise NotEnoughMoneyError(amount=amount, amount_left=amount_left)
    except TransactionException as e:
        logger.error(f"Transaction exception {e}")
        raise e
    except Exception as e:
        logger.error(f"Internal error: {e}")
        raise e
    
    try:
        make_transaction(bank_account)
    except NotValidBankAccountError as e:
        logger.error(f"bank account not valid: {e}")
        raise e
    except NoResultError as e:
        logger.error(f"transaction failed: {e}")
        raise e
    except ValueError as e:
        logger.error(f"Incorrect data type of bank account: {e}")
        raise e
    except Exception as e:
        logger.error(f"Internal error: {e}")
        raise e


if __name__ == '__main__':
    try:
        order_items('Староохотничья 10', 200, 1204245)
    except TransactionException as e:
        logger.error(e)
    except MyException as e:
        logger.error(e)
    except Exception as e:
        logger.error(e)
