from database import sql



class UserDAO():

    def init(user_id, username):

        query = f'''
        INSERT OR IGNORE INTO Users (user_id, username)
        VALUES (?, ?);
        '''
        values = (user_id, username)
   
        sql.run(query, values)

    def transactions(user): 

        query = f'''
        SELECT * FROM Transactions
        WHERE user_id = ?
        '''
        values = (user.user_id)
        return sql.run(query, values)   

    def joint_transactions(user):

        query = f'''
        SELECT second_user_id FROM AccontLinks 
        WHERE first_user_id = ?
        '''
        values = (user.user_id)

        linked_users = sql.run(query, values)


        #остановимся на двух пользователях
        query = f'''
        SELECT * 
        FROM Transactions
        WHERE user_id = ?
        UNION
        SELECT * 
        FROM Transactions
        WHERE user_id = ?;
        '''

    def add_link(first_user, second_user): 

        query = f'''
        INSERT INTO AccountLinks (first_user_id, second_user_id)
        VALUES (?, ?);
        '''
        values = (first_user.user_id, second_user.user_id)
   
        sql.run(query, values)

    def update(user, transaction):

        query = f'''
        INSERT INTO Transactions (datetime, user_id, amount, category)
        VALUES (?, ?, ?, ?);
        '''
        values = (transaction.datetime, user.user_id, transaction.amount, transaction.category)
   
        sql.run(query, values)

    