import sqlite3

with sqlite3.connect("sample.db") as connection:
    c = connection.cursor()
    c.execute("DROP TABLE posts")
    c.execute("""CREATE TABLE posts(title TEXT, description, TEXT)
              """)
    c.execute('INSERT INFO posts VALUES("GOOD", "I\'m good.") ')
    c.execute('INSERT INFO posts VALUES("Well", "I\'m Well.") ')
