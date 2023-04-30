import sqlite3 as sql

#Подключаю дб
db = sql.connect('DataBase.db')
with db:
    cur = db.cursor()
    cur.execute("""CREATE TABLE if not exists ban_word (
        text TEXT
        )""")
    cur.execute("""CREATE TABLE if not exists users (
        chat_id TEXT,
        rep TEXT,
        last_text TEXT
        )""")
    db.commit() 


class DataBase:
    def select_ban_word() -> dict:
        cur.execute(""" SELECT text FROM ban_word """)
        ban_words = cur.fetchall()
        return {"status" : True, "ban_words" : ban_words}
    
    def insert_ban_word(text) -> dict:
        cur.execute(""" INSERT INTO ban_word (text) VALUES (?) """, (text,))
        db.commit()
        return {"status" : True}

    def insert_user(chat_id, rep = 2, last_text = "pass") -> dict:
        cur.execute(""" INSERT INTO users (chat_id, rep, last_text) VALUES (?,?,?) """, (chat_id, rep, last_text))
        db.commit()
        return {"status" : True}

    def select_user(chat_id : str):
        cur.execute(""" SELECT * FROM users WHERE chat_id = ? """, (chat_id,))
        result = cur.fetchall()
        try: return {"status" : True, "data" : {"rep" : result[0][1], "last_text" : result[0][2]}}
        except: return {}
    
    def update_last_text(chat_id, text):
        cur.execute(""" UPDATE users SET last_text = ? WHERE chat_id = ? """, (text, chat_id))
        db.commit()
        return {"status" : True}
    
    def update_rep(chat_id, rep):
        cur.execute(""" SELECT rep FROM users WHERE chat_id = ? """, (chat_id,))
        result = int(cur.fetchall()[0][0])
        if result + rep != 0:
            cur.execute(""" UPDATE users SET rep = ? WHERE chat_id = ? """, (result + rep, chat_id))
            db.commit()
            return {"status" : True}
        elif result + rep >= 2:
            cur.execute(""" UPDATE users SET rep = ? WHERE chat_id = ? """, (2, chat_id))
            db.commit()
            return {"status" : True}
        else:
            return {"status" : False}