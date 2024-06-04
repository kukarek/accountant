from database import sql
from datetime import datetime, timedelta
from misc import Settings

class Stats():


    def per_month(user_id):
        
        #отматываем в начало месяца
        d1 = (datetime.now() - timedelta(days=(datetime.now().day - 1), hours=datetime.now().hour, minutes=datetime.now().minute)).strftime(Settings().format.datetime)
    
        d2 = (datetime.now()).strftime(Settings().format.datetime)

        result = sql.run("""SELECT * FROM Transactions WHERE user_id = ? AND datetime BETWEEN ? AND ?;""", (user_id, d1, d2))

        return "ы"

    def all_time(user_id):

        result = sql.run("""SELECT * FROM Transactions WHERE user_id = ?;""", (user_id,))

        return "ы"

    def for_the_period(user_id, date1, date2):

        result = sql.run("""SELECT * FROM Transactions WHERE user_id = ? AND datetime BETWEEN ? AND ?;""", (user_id, date1, date2))

        return "ы"