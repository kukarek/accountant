import sqlite3
from misc.settings import Settings



def run(query, values = ()):

    try:

        connection = sqlite3.connect(Settings().DB.connection)
        cursor = connection.cursor()
        
        cursor.execute(query, values)

        result = cursor.fetchall()

        connection.commit()
        connection.close()

        return result
    
    except Exception as e:

        print(f"Произошла ошибка в запросе sql: {e}")

def init():

    connection = sqlite3.connect(Settings().DB.connection)
    cursor = connection.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Users (
        user_id INTEGER PRIMARY KEY, 
        username TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Transactions (
        datetime DATETIME PRIMARY KEY, 
        user_id INTEGER, 
        amount INTEGER, 
        category TEXT, 
        FOREIGN KEY (user_id) REFERENCES Users(user_id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS AccountLinks (
        link_id INTEGER PRIMARY KEY AUTOINCREMENT, 
        first_user_id INTEGER, 
        second_user_id INTEGER,
        FOREIGN KEY (first_user_id) REFERENCES Users(user_id)
    );
    """)

    connection.commit()
    connection.close()



