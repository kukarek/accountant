from database import sql


class AccountDAO:

    #создание таблицы для нового пользователя
    def create_table(account):  

        sql.run(f'''CREATE TABLE IF NOT EXISTS {account.name}  (date DATETIME PRIMARY KEY, transaction_amount, category TEXT)''')

        

    def update(account, transaction):

        query = f'''
        INSERT INTO {account.name} (date, transaction_amount, category)
        VALUES (?, ?, ?);
        '''

        values = (transaction.datetime, transaction.amount, transaction.category)

        sql.run(query, values)


    def add_link(user_id): pass

    def remove_transaction(account, transaction_datetime): 
        
        query = f'''
        DELETE FROM {account.name} 
        WHERE date = ?
        '''

        values = (transaction_datetime,)

        sql.run(query, values)


    def transactions(account): 

        query = f'''
        SELECT * FROM {account.name}
        '''

        return sql.run(query)





