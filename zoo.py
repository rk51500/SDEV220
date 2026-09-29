def hours():
    print('Open 9-5 daily')


import sqlite3

conn = sqlite3.connect('books.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE books (
        title TEXT,
        author TEXT,
        year INTEGER
    )
''')

conn.commit()
conn.close()

import sqlite3
import csv

conn = sqlite3.connect('books.db')
cursor = conn.cursor()

with open('books2.csv', 'r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)  

    for row in reader:
        cursor.execute(
            'INSERT INTO books (title, author, year) VALUES (?, ?, ?)',
            (row[0], row[1], int(row[2]))
        )

conn.commit()
conn.close()