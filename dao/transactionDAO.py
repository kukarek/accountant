


class TransactionDAO():

    def remove_transaction(transaction_datetime): 
        
        query = f'''
        DELETE FROM Transaction 
        WHERE date = ?
        '''

        values = (transaction_datetime,)

        sql.run(query, values)

    def save(transaction):

        query = f'''
        INSERT INTO Transaction (date, transaction_amount, category)
        VALUES (?, ?, ?);
        '''

        values = (transaction.datetime, transaction.amount, transaction.category)

        sql.run(query, values)