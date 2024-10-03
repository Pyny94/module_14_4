import sqlite3

connection = sqlite3.connect("database.db")
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Products(
id INT PRIMARY KEY, 
title TEXT IF NO NULL,
description TEXT,
price INT IF NO NULL
)
''')

cursor.execute("INSERT INTO Products (id,title, description, price) VALUES (1,'Product 1', 'Описание продукта 1', 100)")
cursor.execute("INSERT INTO Products (id,title, description, price) VALUES (2,'Product 2', 'Описание продукта 2', 200)")
cursor.execute("INSERT INTO Products (id,title, description, price) VALUES (3,'Product 3', 'Описание продукта 3', 300)")
cursor.execute("INSERT INTO Products (id, title, description, price) VALUES (4, 'Product 4', 'Описание продукта 4', 400)")


def initiate_db(title,description,price):
    check_title = cursor.execute("SELECT * FROM Products WHERE id = ?", (title,))
    if check_title.fetchone() is None:
        cursor.execute(f'''
    INSERT INTO Products VALUES('{title},'{description}, '{price}')
''')
    connection.commit()

def get_all_products(db_name = 'database.db'):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Products")
    products = cursor.fetchall()
    connection.close()
    return products


connection.commit()
connection.close()
