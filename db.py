import sqlite3 as sql

#Подключаю дб
db = sql.connect('DataBase.db')
with db:
    cur = db.cursor()
    cur.execute("""CREATE TABLE if not exists chats (
        chat_id TEXT,
        owner_id TEXT,
        local_name TEXT
        )""")
    cur.execute("""CREATE TABLE if not exists chats_settings (
        chat_id TEXT,
        min_token TEXT,
        ban_words TEXT
        )""")
    cur.execute("""CREATE TABLE if not exists users_in_chat (
        user_id TEXT,
        chat_id TEXT
        )""")
    cur.execute("""CREATE TABLE if not exists ban_word (
        text TEXT
        )""")
    cur.execute("""CREATE TABLE if not exists users (
        chat_id TEXT,
        rep TEXT,
        last_text TEXT,
        global_reputation TEXT,
        name TEXT
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

    def insert_user(chat_id, rep = 2, last_text = "pass", global_reputation = 100, name="None") -> dict:
        cur.execute(""" INSERT INTO users (chat_id, rep, last_text, global_reputation, name) VALUES (?,?,?,?,?) """, (chat_id, rep, last_text, global_reputation, name))
        db.commit()
        return {"status" : True}

    def insert_chat(chat_id, owner_id):
        cur.execute(""" INSERT INTO chats (chat_id, owner_id, local_name) VALUES (?,?,?) """, (chat_id, owner_id, chat_id))
        cur.execute(""" INSERT INTO chats_settings (chat_id, min_token, ban_words) VALUES (?,?,?) """, (chat_id, "0", "0"))
        db.commit()
        return {"status" : True}

    def select_user(chat_id : str):
        cur.execute(""" SELECT * FROM users WHERE chat_id = ? """, (chat_id,))
        result = cur.fetchall()
        try: return {"status" : True, "data" : {"rep" : result[0][1], "last_text" : result[0][2]}}
        except: return {}
    
    def select_chat(chat_id) -> dict:
        cur.execute(""" SELECT * FROM chats """)
        chat = cur.fetchall()
        if len(chat) >= 1:
            return {"status" : True,
                    "chat_id" : chat[0][0],
                    "owner_id" : chat[0][1],
                    "local_name" : chat[0][2]}
        else:
            return {"status" : False}

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