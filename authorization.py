import sqlite3


con = sqlite3.connect(r"database\users_database.sqlite3")
cur = con.cursor()


def login_in_db(username, password):
    res = cur.execute("""SELECT * FROM passwords WHERE
                   user_id = (SELECT id from usernames WHERE username = ?) AND
                   password = ?""", (username, password)).fetchall()
    if len(res) != 0:
        return True
    return False


def add_in_db(username, password):
    if not find_in_db(username):
        cur.execute("""INSERT INTO usernames(username) VALUES(?)""", (username,))
        cur.execute("""INSERT INTO passwords(password) VALUES(?)""", (password,))
        con.commit()
        return True
    return False


def find_in_db(username):
    res = cur.execute("""SELECT * FROM usernames WHERE username = ?""", (username,)).fetchall()
    if len(res) == 0:
        return False
    return True


def is_ok_passwd(p):
    if (len(p) < 6) or ((p.isdigit() or p.isalpha()) and p.lower() == p) or \
            ((p.isalnum() and (p.islower() or p.isupper())) or (p.isalpha() and not p.islower())):
        return False
    return True
