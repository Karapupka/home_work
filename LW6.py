import sqlite3
from contextlib import suppress
from random import choice

from flask import Flask

example_names = (
    'John', 'Robert', 'Alexander', 'Emma', 'Carla', 'Eugene', 'Daniel', 'Jessica', 'Roberto', 'Enzo'
)

con = sqlite3.connect('birthyears.db', check_same_thread=False)
cur = con.cursor()

# create data if doesn't exist
with suppress(sqlite3.OperationalError):
    cur.execute('CREATE TABLE birthyears(name text PRIMARY KEY, year integer)')
with suppress(sqlite3.IntegrityError):
    cur.executemany(
        'INSERT INTO birthyears VALUES(?, ?)',
        ((name, choice(range(1950, 2000))) for name in example_names)
    )
    con.commit()

# check data consistency
assert len(cur.execute('SELECT * FROM birthyears').fetchall()) == 10

app = Flask('birthyears')

@app.route('/')
def default():
    data = cur.execute('SELECT * FROM birthyears').fetchall()
    return (
        '''<table>
           <tr>
               <th>Name</th>
               <th>Year</th>
           </tr>
        ''' +
        '\n'.join(
            f''' 
            <tr>
                <td>{name}</td>
                <td>{birthyear}</td>
            </tr>
            '''
            for name, birthyear in data
        ) +
        '</table>'
    )