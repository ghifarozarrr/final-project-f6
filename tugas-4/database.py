import sqlite3
conn = sqlite3.connect('progjar.db')

c = conn.cursor()
print 'Migrating tables.'
c.execute('''CREATE TABLE user(id integer PRIMARY KEY AUTOINCREMENT, user_name text, password text)''')
c.execute('''CREATE TABLE groupchat(id integer PRIMARY KEY AUTOINCREMENT, group_name text, admin_id integer, FOREIGN KEY(admin_id) REFERENCES user(id))''')
c.execute('''CREATE TABLE user_group(user_id integer, group_id integer, FOREIGN KEY(user_id) REFERENCES user(id), FOREIGN KEY(group_id) REFERENCES groupchat(id))''')
c.execute('''CREATE TABLE chat(id integer PRIMARY KEY AUTOINCREMENT, sender_id integer, receiver_id integer, message text, type text, received_time timestamp, FOREIGN KEY(sender_id) REFERENCES user(id), FOREIGN KEY(receiver_id) REFERENCES user(id))''')
c.execute('''CREATE TABLE chat_group(id integer PRIMARY KEY AUTOINCREMENT, sender_id integer, group_id integer, message text, type text, received_time timestamp, FOREIGN KEY(sender_id) REFERENCES user(id), FOREIGN KEY(group_id) REFERENCES groupchat(id))''')
print 'Tables migrated.'
conn.commit()

conn.close()