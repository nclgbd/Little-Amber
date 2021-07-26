import sqlite3

def initialize_db():
    dbase = sqlite3.connect('db.db') # Open a database File
    print('Database connected')
    dbase.execute(''' CREATE TABLE IF NOT EXISTS users_commands(
        NAME TEXT PRIMARY KEY NOT NULL,
        COMMAND TEXT NOT NULL
        ) ''')
    print('tables created')
    dbase.close()