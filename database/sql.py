import sqlite3
from misc.settings import Settings



def run(query, values = ()):


    connection = sqlite3.connect(Settings().DB.connection)
    cursor = connection.cursor()
    
    cursor.execute(query, values)

    result = cursor.fetchall()

    connection.commit()
    connection.close()

    return result




