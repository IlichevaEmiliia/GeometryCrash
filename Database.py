import sqlite3
import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "GeometryCrash.sqlite")

def createTable():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(""" CREATE TABLE IF NOT EXISTS users (
                                            id integer PRIMARY KEY,
                                            login text NOT NULL UNIQUE,
                                            lvl1_percentage integer NOT NULL,
                                            lvl2_percentage integer NOT NULL,
                                            lvl3_percentage integer NOT NULL,
                                            lost_coins integer NOT NULL
                                        ); """)
    conn.commit()
    conn.close()

def insertUser(user):
    sql = """INSERT INTO users (login, lvl1_percentage, lvl2_percentage, lvl3_percentage, lost_coins) VALUES (?, 0, 0, 0, 0)"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(sql, user)
    data = cursor.fetchall()
    conn.commit()
    conn.close()
    return data

def findUser(login):
    sql = """SELECT * FROM users WHERE login = ?"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(sql, login)
    data = cursor.fetchall()
    conn.close()
    return data

def updateUser(user):
    sql = """UPDATE users SET lvl1_percentage = ?, lvl2_percentage = ?, lvl3_percentage = ?, lost_coins = ? WHERE login = ?"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(sql, user)
    conn.commit()
    conn.close()


def createTable_shop():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(""" CREATE TABLE IF NOT EXISTS shop (
                                            id integer PRIMARY KEY,
                                            lvl text NOT NULL,
                                            product text NOT NULL UNIQUE,
                                            price integer NOT NULL,
                                            image text NOT NULL
                                        ); """)
    conn.commit()
    conn.close()

def insertProduct(shop):
    sql = """INSERT INTO shop (lvl, product, price, image) VALUES (?, ?, ?, ?)"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(sql, shop)
    data = cursor.fetchall()
    conn.commit()
    conn.close()
    return data

def findallProducts():
    sql = """SELECT * FROM shop"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    conn.close()
    return data


def createTable_userProducts():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(""" CREATE TABLE IF NOT EXISTS user_products (
                                            id integer PRIMARY KEY,
                                            id_user text NOT NULL,
                                            id_product text NOT NULL,
                                            status integer NOT NULL,
                                            FOREIGN KEY (id_user) references users(login),
                                            FOREIGN KEY (id_product) references shop(product)
                                        ); """)
    conn.commit()
    conn.close()

def insertUserProduct(user_products):
    sql = """INSERT INTO user_products (id_user, id_product, status) VALUES (?, ?, ?)"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(sql, user_products)
    data = cursor.fetchall()
    conn.commit()
    conn.close()
    return data

def findallUserProducts(id_user):
    sql = """SELECT * FROM user_products WHERE id_user = ?"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(sql, id_user)
    data = cursor.fetchall()
    conn.close()
    return data

def findUserProduct(id):
    sql = """SELECT * FROM user_products WHERE id_user = ? AND id_product = ?"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(sql, id)
    data = cursor.fetchall()
    conn.close()
    return data

def updateUserProducts(user_products):
    sql = """UPDATE user_products SET status = ? WHERE id_user = ? AND id_product = ?"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(sql, user_products)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    pass