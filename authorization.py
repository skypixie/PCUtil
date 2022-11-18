import sqlite3
import sys


try:
    con = sqlite3.connect(r"database\users_database.sqlite3")
    cur = con.cursor()
except sqlite3.OperationalError:
    print("[!] Отсутствует файл базы данных [!]")
    sys.exit()


def login_in_db(username, password):  # Посмотреть совпадает ли логин с паролем
    # True если да и наоборот
    res = cur.execute("""SELECT * FROM passwords WHERE
                   user_id = (SELECT id from usernames WHERE username = ?) AND
                   password = ?""", (username, password)).fetchall()
    if len(res) != 0:
        return True
    return False


def add_in_db(username, password):  # Добавление в базу данных
    # True если такого username еще нет
    if not find_in_db(username):
        cur.execute("""INSERT INTO usernames(username) VALUES(?)""", (username,))
        cur.execute("""INSERT INTO passwords(password) VALUES(?)""", (password,))
        con.commit()
        return True
    return False


def find_in_db(username):  # Найти в базе данных по логину
    # False если такого имени еще нет
    res = cur.execute("""SELECT * FROM usernames WHERE username = ?""", (username,)).fetchall()
    if len(res) == 0:
        return False
    return True


def is_ok_passwd(p):  # Проверка пароля
    if (len(p) < 6) or ((p.isdigit() or p.isalpha()) and p.lower() == p) or \
            ((p.isalnum() and (p.islower() or p.isupper())) or
             (p.isalpha() and not p.islower())):
        return False
    return True
