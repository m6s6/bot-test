

import sqlite3

try:
    conn = sqlite3.connect('dt_bot.db')
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS users(
       userid INT PRIMARY KEY,
       name TEXT,
       category TEXT);
    """)
    conn.commit()
    conn.close()
except:
    pass

def get_name(user_id):
    try:
        conn = sqlite3.connect('dt_bot.db')
        cur = conn.cursor()
        sql_select_query = """select * from users where userid = ?"""
        cur.execute(sql_select_query, (user_id,))
        records = cur.fetchone()
        return records

        cur.close()

    except sqlite3.Error as error:
        pass
    finally:
        if conn:
            conn.close()

def insert_user(user_id, name):
    try:
        conn = sqlite3.connect('dt_bot.db')
        cur = conn.cursor()

        sqlite_insert_with_param = """INSERT INTO users
                              (userid, name, category)
                              VALUES (?, ?, ?);"""

        data_tuple = (user_id, name, 'none')
        cur.execute(sqlite_insert_with_param, data_tuple)
        conn.commit()
        cur.close()

    except sqlite3.Error as error:
        pass
    finally:
        if conn:
            conn.close()

def update_table(user_id, category):
    try:
        conn = sqlite3.connect('dt_bot.db')
        cur = conn.cursor()

        sql_update_query = """Update users set category = ? where userid = ?"""
        data = (category, user_id)
        cur.execute(sql_update_query, data)
        conn.commit()
        cur.close()

    except sqlite3.Error as error:
        pass
    finally:
        if conn:
            conn.close()

# conn = sqlite3.connect('dt_bot.db')
# cur = conn.cursor()
# cur.execute("SELECT * FROM users;")
# all_results = cur.fetchall()
# print(all_results)
# cur.close()
#
# print('1')
# get_name(335137933)