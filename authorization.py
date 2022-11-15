import sqlite3


con = sqlite3.connect(r"database\users_database.sqlite3")
cur = con.cursor()


def find_in_db(username, password):
    res = cur.execute("""SELECT * FROM passwords WHERE
                   user_id = (SELECT id from usernames WHERE username = ?) AND
                   password = ?""", (username, password)).fetchall()
    if len(res) != 0:
        return True
    return False


def add_in_db(username, password):
    res = cur.execute("""SELECT * FROM usernames WHERE
                   username = ?""", (username,)).fetchall()
    if len(res) != 0:
        return False
    cur.execute("""INSERT INTO usernames(username) VALUES(?)""", (username,))
    cur.execute("""INSERT INTO passwords(password) VALUES(?)""", (password,))
    con.commit()
    return True
