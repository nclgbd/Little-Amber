import sqlite3
def upsert_command(NAME,COMMAND):
    dbase = sqlite3.connect('db.db') # Open a database File
    dbase.execute(''' INSERT OR REPLACE INTO users_commands(NAME,COMMAND)
            VALUES(?,?)''',(NAME,COMMAND)) 
    dbase.commit()
    dbase.close()
def delete_command(NAME):
    dbase = sqlite3.connect('db.db') # Open a database File
    dbase.execute(''' DELETE FROM users_commands WHERE NAME=?''',(NAME,))
    dbase.commit()
    dbase.close()
def query_command(NAME):
    command = ''
    dbase = sqlite3.connect('db.db') # Open a database File
    data = dbase.execute(''' SELECT * FROM users_commands WHERE NAME=?''',(NAME,))
    dbase.commit()
    for record in data:
        command = str(record[1])
    dbase.close()
    return command