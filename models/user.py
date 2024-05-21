from .transaction import Transaction


class User():

    @property
    def user_id(self): return self._user_id

    @property
    def username(self): return self._username

    def __init__(self, user_id, username):

        self._user_id = user_id
        self._username = username

    @property
    def name(self): return self._name

    @property
    def transactions(self):

        transactions = []
        a = AccountDAO.transactions(self)
        for entry in AccountDAO.transactions(self):

            #создание обьектов из данных бд
            transactions.append(Transaction(entry[0], entry[1], entry[2]))

        return transactions

    def update(self, transaction): AccountDAO.update(self, transaction)

    def add_link(self): pass

    def remove_transaction(self, transaction_datetime): AccountDAO.remove_transaction(self, transaction_datetime)


