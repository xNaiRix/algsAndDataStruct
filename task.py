class MyException(Exception):
    pass


data_base = {
    'addresses': ['Рекордов 15', 'Олимпийский проспект 1'],
    'amount_left': 100
}

def valid(bank_account):
    return True

# Add exceptions here
def make_transaction(bank_account):
    # Some request
    if not valid(bank_account):
        pass
    result = False
    if not result:
        pass

# Add exceptions here
def order_items(where, amount, bank_account):
    try:
        if where not in data_base['addresses']:
            pass
        if amount <= 0:
            pass
        if amount > data_base['amount_left']:
            pass
    except:
        pass
    try:
        make_transaction(bank_account)
    except:
        pass


if __name__ == '__main__':
    try:
        order_items('Староохотничья 10', 200, 1204245)
    except MyException:
        pass
    except Exception:
        pass