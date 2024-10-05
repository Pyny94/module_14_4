import sqlite3


def initiate_db():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INT NOT NULL
    );
    ''')

   # cursor.execute('INSERT INTO Products (title, description, price) VALUES (?, ?, ?)',
   #                 ('Продукт1', 'Описание1', '100'))
  #  cursor.execute('INSERT INTO Products (title, description, price) VALUES (?, ?, ?)',
  #                  ('Продукт2', 'Описание2', '200'))
  #  cursor.execute('INSERT INTO Products (title, description, price) VALUES (?, ?, ?)',
   #                 ('Продукт3', 'Описание3', '300'))
   # cursor.execute('INSERT INTO Products (title, description, price) VALUES (?, ?, ?)',
  #                  ('Продукт4', 'Описание4', '400'))

    connection.commit()
    connection.close()

def add_product(product_data):
    conn = sqlite3.connect('products')
    c = conn.cursor()
    c.execute('''INSERT INTO Products (title, description, price) VALUES (?, ?, ?)''', product_data)
    conn.commit()
    conn.close()

def get_all_products():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM Products')
    result = cursor.fetchall()

    connection.commit()
    connection.close()

    return result
