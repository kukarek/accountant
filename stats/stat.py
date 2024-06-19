from database import sql
from datetime import datetime, timedelta
from misc import Settings
from models.transaction import Transaction

class Stats():


    def per_month(user_id):
        
        #отматываем в начало месяца
        d1 = (datetime.now() - timedelta(days=(datetime.now().day - 1), hours=datetime.now().hour, minutes=datetime.now().minute)).strftime(Settings().format.datetime)
    
        d2 = (datetime.now()).strftime(Settings().format.datetime)

        result = sql.run("""SELECT * FROM Transactions WHERE user_id = ? AND datetime BETWEEN ? AND ?;""", (user_id, d1, d2))

        #инициализация списка транзакций
        transactions = [Transaction(t[0], t[2], t[3]) for t in result] if result else []

        return Output.print("СТАТИСТИКА ЗА МЕСЯЦ", transactions)

    def all_time(user_id):

        result = sql.run("""SELECT * FROM Transactions WHERE user_id = ?;""", (user_id,))

        #инициализация списка транзакций
        transactions = [Transaction(t[0], t[2], t[3]) for t in result] if result else []

        return Output.print("СТАТИСТИКА ЗА ВСЕ ВРЕМЯ", transactions)

    def for_the_period(user_id, date1, date2):

        result = sql.run("""SELECT * FROM Transactions WHERE user_id = ? AND datetime BETWEEN ? AND ?;""", (user_id, date1, date2))

        #инициализация списка транзакций
        transactions = [Transaction(t[0], t[2], t[3]) for t in result] if result else []

        return Output.print("СТАТИСТИКА ЗА ПЕРИОД", transactions)

class Output():

    def print(title, transactions):

        if not transactions:
            return "Нет данных"

        message = f"""
{title}

Зарплата: {sum(t.amount for t in transactions if t.category == "Зарплата")}р

Чаевые: {sum(t.amount for t in transactions if t.category == "Чаевые")}р

Прочее: {sum(t.amount for t in transactions if t.category == "Прочее")}р

Всего: {sum(t.amount for t in transactions)}р
Зачислений: {len(transactions)}
"""
        
        return message