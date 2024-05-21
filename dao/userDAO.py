





class UserDAO():

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

    