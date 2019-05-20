import socket
import sys
import os
import json
import uuid
import sqlite3
import datetime
import base64
from Queue import *


class Chat:
    def __init__(self):
        self.sessions = {}
        self.users = {}
        self.groups = {}
        self.username = ''

    def proses(self, data):
        j = data.split(" ")
        try:
            command = j[0].strip()
            print 'command is', command
            if (command == 'auth_register'):
                username = j[1].strip()
                password = j[2].strip()
                print "auth_register {}".format(username)
                return self.user_register(username, password)

            elif (command == 'auth_login'):
                username = j[1].strip()
                password = j[2].strip()
                print "auth_login {}".format(username)
                return self.user_login(username, password)

            elif (command == 'auth_logout'):
                sessionid = j[1].strip()
                print "auth_logout {}".format(sessionid)
                return self.user_logout(sessionid)

            elif (command == 'send'):
                sessionid = j[1].strip()
                usernameto = j[2].strip()
                message = ''
                for w in j[3:]:
                    message = "{} {}".format(message, w)
                usernamefrom = self.sessions[sessionid]['username']
                print "send message from {} to {}".format(usernamefrom, usernameto)
                return self.send_message(sessionid, usernamefrom, usernameto, message)

            elif (command == 'send_file'):
                sessionid = j[1].strip()
                usernameto = j[2].strip()
                message = ''
                for w in j[3:]:
                    message = "{} {}".format(message, w)
                usernamefrom = self.sessions[sessionid]['username']
                print 'send file from {} to {}'.format(usernamefrom, usernameto)
                return self.send_file(sessionid, usernamefrom, usernameto, message)

            elif (command == 'download_file'):
                sessionid = j[1].strip()
                file_name = j[2].strip()
                print 'download file command'
                return self.download_file(sessionid, file_name)

            elif (command == 'inbox'):
                sessionid = j[1].strip()
                username = self.sessions[sessionid]['username']
                print "inbox {}".format(sessionid)
                return self.get_inbox(username)

            elif (command == 'mkgr'):
                group = j[1].strip()
                sessionid = j[2].strip()
                username = self.sessions[sessionid]['username']
                print "creating group {}...".format(group)
                return self.mkgr(group, username)

            elif (command == 'join'):
                group = j[1].strip()
                sessionid = j[2].strip()
                username = self.sessions[sessionid]['username']
                print "{} is joining {}...".format(self.sessions[sessionid]['username'], group)
                return self.join(group, username)

            elif (command == 'listgroup'):
                group = j[1].strip()
                sessionid = j[2].strip()
                username = self.sessions[sessionid]['username']
                print "{} {}".format(command, group)
                return self.listgroup(group, username)

            elif (command == 'leave'):
                group = j[1].strip()
                sessionid = j[2].strip()
                username = self.sessions[sessionid]['username']
                print "{} {}".format(command, group)
                return self.leave(group, username)

            elif (command == 'sendgroup'):
                group = j[1].strip()
                sessionid = j[2].strip()
                username = self.sessions[sessionid]['username']
                message = ""
                for w in j[3:]:
                    message = "{} {}".format(message, w)
                print "{} is sending message to group : {}".format(self.sessions[sessionid]['username'], group)
                return self.sendgroup(group, username, message)

            elif (command == 'inboxgroup'):
                group = j[1].strip()
                sessionid = j[2].strip()
                username = self.sessions[sessionid]['username']
                print "inboxgroup {}".format(group)
                return self.inboxgroup(group, username)

            elif (command == 'sendgroup_file'):
                sessionid = j[1].strip()
                group_name = j[2].strip()
                message = ''
                for w in j[3:]:
                    message = "{} {}".format(message, w)
                username = self.sessions[sessionid]['username']
                print 'send file from {} to {}'.format(username, group_name)
                return self.sendgroup_file(sessionid, username, group_name, message)

            elif (command == 'downloadgroup_file'):
                sessionid = j[1].strip()
                group_name = j[2].strip()
                message = j[3].strip()
                username = self.sessions[sessionid]['username']
                print 'send file from {} to {}'.format(username, group_name)
                return self.downloadgroup_file(sessionid, username, group_name, message)

            else:
                return {'status': 'ERROR', 'message': '**Protocol Tidak Benar'}
        except IndexError:
            return {'status': 'ERROR', 'message': '--Protocol Tidak Benar'}

    def user_register(self, username, password):
        credentials = (username, password)
        db_conn = sqlite3.connect('progjar.db')
        db = db_conn.cursor()
        db.execute('SELECT * FROM user where user_name=? AND password=?', credentials)
        auth = db.fetchone()
        if auth != None:
            message = 'Already an account with the provided username. Please use a different username.'
        else:
            db.execute('INSERT INTO user (user_name, password) values(?, ?)', (username, password))
            db_conn.commit()
            return {'status': 'OK'}

    def user_login(self, username, password):
        credentials = (username, password)
        db_conn = sqlite3.connect('progjar.db')
        db = db_conn.cursor()
        db.execute('SELECT * FROM user where user_name=? AND password=?', credentials)
        auth = db.fetchone()
        if auth == None:
            return {'status': 'ERROR', 'message': 'Username/Password salah'}

        tokenid = str(uuid.uuid4())
        user = {'nama': auth[1], 'password': auth[2], 'incoming': {}, 'outgoing': {}}
        self.users[auth[1]] = user
        self.sessions[tokenid] = {'username': username, 'userdetail': user}
        self.username = user['nama']
        return {'status': 'OK', 'tokenid': tokenid}

    def user_logout(self, sessionid):
        if (sessionid == ''):
            return {'status': 'ERROR', 'message': 'Login first to log out!'}
        self.sessions.pop(sessionid, None)
        self.tokenid = ''
        return {'status': 'OK', 'message': 'Session ID Deleted. Logged out!'}

    def get_user(self, username):
        if (username not in self.users):
            return False
        return self.users[username]

    def get_inbox(self, username):
        s_fr = self.get_user(username)
        incoming = s_fr['incoming']

        db_conn = sqlite3.connect('progjar.db')
        db = db_conn.cursor()
        db.execute("SELECT * FROM chat where receiver_id = ?", (username,))
        rows = db.fetchall()

        msgs = {}
        for row in rows:
            print row
            if row[1] in msgs:
                msgs[row[1]].append(row[3])
            else:
                msgs[row[1]] = []
                msgs[row[1]].append(row[3])
        return {'status': 'OK', 'messages': msgs}

    def send_message(self, sessionid, username_from, username_dest, message):
        if (sessionid not in self.sessions):
            return {'status': 'ERROR', 'message': 'Session not found'}

        db_conn = sqlite3.connect('progjar.db')
        db = db_conn.cursor()

        db.execute('SELECT * FROM user where user_name=?', (username_from,))
        sender = db.fetchone()
        user = {'nama': sender[1], 'password': sender[2], 'incoming': {}, 'outgoing': {}}
        self.users[sender[1]] = user

        try:
            db.execute('SELECT * FROM user where user_name=?', (username_dest,))
            dest = db.fetchone()
            user = {'nama': dest[1], 'password': dest[2], 'incoming': {}, 'outgoing': {}}
            self.users[dest[1]] = user
        except TypeError as e:
            return {'status': 'ERROR', 'message': 'User not found'}

        s_fr = self.get_user(username_from)
        s_to = self.get_user(username_dest)

        message = {'msg_from': s_fr['nama'], 'msg_to': s_to['nama'], 'msg': message}
        inqueue_receiver = s_to['incoming']

        try:
            db.execute('INSERT INTO chat (sender_id, receiver_id, message, type, received_time) values(?, ?, ?, ?, ?)',
                       (username_from, username_dest, str(message), 'chat', datetime.datetime.now()))
            db_conn.commit()
        except KeyError:
            inqueue_receiver[username_from] = Queue()
            inqueue_receiver[username_from].put(message)
        return {'status': 'OK', 'message': 'Message Sent'}

    def start_file_socket(self):
        try:
            print('Opening data socket on ', '0.0.0.0:1338')
            self.data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.data_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.data_socket.bind(('0.0.0.0', 1338))
            self.data_socket.listen(10)
            print('Data socket has started. Listening on 1338')
            return self.data_socket.accept()
        except Exception as e:
            print('Error on data socket client')
            print(e)
            self.close_data_socket()

    def send_file(self, sessionid, username_from, username_dest, message):
        if (sessionid not in self.sessions):
            return {'status': 'ERROR', 'message': 'Session not found'}

        client_file_socket, client_data_address = self.start_file_socket()

        message = '.\\' + message.lstrip()
        message = os.path.basename(message)
        message = message.replace(' \r\n', ' ')
        filename = str(datetime.datetime.now())[:19]
        filename = filename.replace(':', '_')
        filename = filename.replace(' ', '_')
        filename = filename.replace('-', '_')
        message = filename + '_' + message

        f = open(os.path.join(os.getcwd(), 'upload', str(message)), 'wb')
        while True:
            bytes = client_file_socket.recv(1024)
            if not bytes:
                break
            f.write(bytes)
        f.close()

        db_conn = sqlite3.connect('progjar.db')
        db = db_conn.cursor()

        db.execute('SELECT * FROM user where user_name=?', (username_from,))
        sender = db.fetchone()
        user = {'nama': sender[1], 'password': sender[2], 'incoming': {}, 'outgoing': {}}
        self.users[sender[1]] = user

        try:
            db.execute('SELECT * FROM user where user_name=?', (username_dest,))
            dest = db.fetchone()
            user = {'nama': dest[1], 'password': dest[2], 'incoming': {}, 'outgoing': {}}
            self.users[dest[1]] = user
        except TypeError as e:
            return {'status': 'ERROR', 'message': 'User not found'}

        s_fr = self.get_user(username_from)
        s_to = self.get_user(username_dest)

        message = {'msg_from': s_fr['nama'], 'msg_to': s_to['nama'], 'msg': message}
        inqueue_receiver = s_to['incoming']

        try:
            db.execute('INSERT INTO chat (sender_id, receiver_id, message, type, received_time) values(?, ?, ?, ?, ?)',
                       (username_from, username_dest, json.dumps(message), 'file', datetime.datetime.now()))
            db_conn.commit()
        except KeyError:
            inqueue_receiver[username_from] = Queue()
            inqueue_receiver[username_from].put(message)

        return {'status': 'OK', 'message': 'File sent'}

    def download_file(self, sessionid, file_name):
        if (sessionid not in self.sessions):
            return {'status': 'ERROR', 'message': 'Session not found'}

        file_name = file_name.lstrip()
        db_conn = sqlite3.connect('progjar.db')
        db = db_conn.cursor()
        db.execute('SELECT * FROM chat where receiver_id=? and type = ?', (self.username, 'file',))
        files = db.fetchall()

        file_to_download = ''

        for file in files:
            json_msg = json.loads(file[3])
            if (file_name == str(json_msg['msg'].rstrip())):
                file_to_download = file_name
                break

        if file_to_download != '':
            client_data_socket, client_data_address = self.start_file_socket()
            f = open(os.path.join(os.getcwd(), 'upload', str(file_to_download)), 'rb')
            bytes = f.read(1024)
            totalsend = len(bytes)
            filesize = os.path.getsize('upload/' + file_to_download)
            while True:
                client_data_socket.send(bytes)
                bytes = f.read(1024)
                print "{0:.2f}".format((totalsend / float(filesize)) * 100) + "% Done"
                totalsend += len(bytes)
                if not bytes:
                    break
            f.close()
            self.data_socket.close()
            return {'status': 'OK', 'message': 'File downloaded'}
        return {'status': 'ERROR', 'message': 'File not found'}

    def mkgr(self, group_name, username):
        credentials = (group_name, username)
        db_conn = sqlite3.connect('progjar.db')
        db = db_conn.cursor()
        db.execute('SELECT * FROM groupchat where group_name=? AND admin_id=?', credentials)
        cek = db.fetchone()
        if cek != None:
            return {'status': 'ERROR', 'message': 'Group does exist'}
        else:
            db.execute('INSERT INTO groupchat (group_name, admin_id) values(?, ?)', (group_name, username))
            db_conn.commit()
            db.execute('INSERT INTO user_group (group_id, user_id) values(?, ?)', (group_name, username))
            db_conn.commit()
            return {'status': 'OK'}

    def join(self, group_name, username):
        credentials = (group_name, username)
        db_conn = sqlite3.connect('progjar.db')
        db = db_conn.cursor()
        db.execute('SELECT * FROM user_group where group_id=? AND user_id=?', credentials)
        cek = db.fetchone()
        db.execute('SELECT * FROM groupchat where group_name=?', (group_name,))
        cek2 = db.fetchone()
        if cek2 != None:
            if cek != None:
                return {'status': 'ERROR', 'message': 'You have already in group'}
            else:
                db.execute('INSERT INTO user_group (group_id, user_id) values(?, ?)', (group_name, username))
                db_conn.commit()
                return {'status': 'OK'}
        elif cek2 == None:
            return {'status': 'ERROR', 'message': 'Group not found'}

    def listgroup(self, group_name, username):
        credentials = (group_name, username)
        db_conn = sqlite3.connect('progjar.db')
        db = db_conn.cursor()
        db.execute('SELECT * FROM user_group where group_id=? AND user_id=?', credentials)
        cek = db.fetchone()
        db.execute('SELECT * FROM groupchat where group_name=?', (group_name,))
        cek2 = db.fetchone()
        if cek2 != None:
            if cek != None:
                db.execute("SELECT * FROM user_group where group_id = ?", (group_name,))
                rows = db.fetchall()
                msgs = {}
                for row in rows:
                    print row
                    if row[1] in msgs:
                        msgs[row[1]].append(row[0])
                    else:
                        msgs[row[1]] = []
                        msgs[row[1]].append(row[0])
                return {'status': 'OK', 'messages': msgs}
            elif cek == None:
                return {'status': 'ERROR', 'message': 'You are not group member'}
        elif cek2 == None:
            return {'status': 'ERROR', 'message': 'Group not found'}

    def leave(self, group_name, username):
        credentials = (group_name, username)
        db_conn = sqlite3.connect('progjar.db')
        db = db_conn.cursor()
        db.execute('SELECT * FROM user_group where group_id=? AND user_id=?', credentials)
        cek = db.fetchone()
        db.execute('SELECT * FROM groupchat where group_name=?', (group_name,))
        cek2 = db.fetchone()
        if cek2 != None:
            if cek != None:
                db.execute("DELETE FROM user_group where group_id=? AND user_id=?", credentials)
                db_conn.commit()
                return {'status': 'OK'}
            elif cek == None:
                return {'status': 'ERROR', 'message': 'You are not group member'}
        elif cek2 == None:
            return {'status': 'ERROR', 'message': 'Group not found'}

    def sendgroup(self, group_name, username, message):
        credentials = (group_name, username)
        db_conn = sqlite3.connect('progjar.db')
        db = db_conn.cursor()
        db.execute('SELECT * FROM user_group where group_id=? AND user_id=?', credentials)
        cek = db.fetchone()
        db.execute('SELECT * FROM groupchat where group_name=?', (group_name,))
        cek2 = db.fetchone()
        if cek2 != None:
            if cek != None:
                db.execute(
                    'INSERT INTO chat_group (sender_id, group_id, message, type, received_time) values(?, ?, ?, ?, ?)',
                    (username, group_name, message, 'chatgroup', datetime.datetime.now()))
                db_conn.commit()
                return {'status': 'OK'}
            elif cek == None:
                return {'status': 'ERROR', 'message': 'You are not group member'}
        elif cek2 == None:
            return {'status': 'ERROR', 'message': 'Group not found'}

    def inboxgroup(self, group_name, username):
        credentials = (group_name, username)
        db_conn = sqlite3.connect('progjar.db')
        db = db_conn.cursor()
        db.execute('SELECT * FROM user_group where group_id=? AND user_id=?', credentials)
        cek = db.fetchone()
        db.execute('SELECT * FROM groupchat where group_name=?', (group_name,))
        cek2 = db.fetchone()
        if cek2 != None:
            if cek != None:
                db.execute("SELECT * FROM chat_group where group_id = ?", (group_name,))
                rows = db.fetchall()
                msgs = {}
                for row in rows:
                    print row
                    if row[1] in msgs:
                        msgs[row[1]].append(row[3])
                    else:
                        msgs[row[1]] = []
                        msgs[row[1]].append(row[3])
                return {'status': 'OK', 'messages': msgs}
            elif cek == None:
                return {'status': 'ERROR', 'message': 'You are not group member'}
        elif cek2 == None:
            return {'status': 'ERROR', 'message': 'Group not found'}

    def sendgroup_file(self, sessionid, username, group_name, message):
        if (sessionid not in self.sessions):
            return {'status': 'ERROR', 'message': 'Session not found'}

        credentials = (group_name, username)
        db_conn = sqlite3.connect('progjar.db')
        db = db_conn.cursor()
        db.execute('SELECT * FROM user_group where group_id=? AND user_id=?', credentials)
        cek = db.fetchone()
        db.execute('SELECT * FROM groupchat where group_name=?', (group_name,))
        cek2 = db.fetchone()
        if cek2 != None:
            if cek != None:
                client_file_socket, client_data_address = self.start_file_socket()

                message = '.\\' + message.lstrip()
                message = os.path.basename(message)
                message = message.replace(' \r\n', ' ')
                filename = str(datetime.datetime.now())[:19]
                filename = filename.replace(':', '_')
                filename = filename.replace(' ', '_')
                filename = filename.replace('-', '_')
                message = filename + '_' + message

                f = open(os.path.join(os.getcwd(), 'upload', str(message)), 'wb')
                while True:
                    bytes = client_file_socket.recv(1024)
                    if not bytes:
                        break
                    f.write(bytes)
                f.close()

                db.execute(
                    'INSERT INTO chat_group (sender_id, group_id, message, type, received_time) values(?, ?, ?, ?, ?)',
                    (username, group_name, message, 'filegroup', datetime.datetime.now()))
                db_conn.commit()
                return {'status': 'OK', 'message': 'File sent'}
            elif cek == None:
                return {'status': 'ERROR', 'message': 'You are not group member'}
        elif cek2 == None:
            return {'status': 'ERROR', 'message': 'Group not found'}

    def downloadgroup_file(self, sessionid, username, group_name, file_name):
        if (sessionid not in self.sessions):
            return {'status': 'ERROR', 'message': 'Session not found'}

        credentials = (group_name, username)
        db_conn = sqlite3.connect('progjar.db')
        db = db_conn.cursor()
        db.execute('SELECT * FROM user_group where group_id=? AND user_id=?', credentials)
        cek = db.fetchone()
        db.execute('SELECT * FROM groupchat where group_name=?', (group_name,))
        cek2 = db.fetchone()
        if cek2 != None:
            if cek != None:
                file_name = file_name.lstrip()
                db.execute('SELECT * FROM chat_group where group_id=? and type = ? and message = ?', (group_name, 'filegroup', file_name,))
                files = db.fetchall()

                if files != None:
                    client_data_socket, client_data_address = self.start_file_socket()
                    f = open(os.path.join(os.getcwd(), 'upload', str(file_name)), 'rb')
                    bytes = f.read(1024)
                    totalsend = len(bytes)
                    filesize = os.path.getsize('upload/' + file_name)
                    while True:
                        client_data_socket.send(bytes)
                        bytes = f.read(1024)
                        print "{0:.2f}".format((totalsend / float(filesize)) * 100) + "% Done"
                        totalsend += len(bytes)
                        if not bytes:
                            break
                    f.close()
                    self.data_socket.close()
                    return {'status': 'OK', 'message': 'File downloaded'}
            elif cek == None:
                return {'status': 'ERROR', 'message': 'You are not group member'}
        elif cek2 == None:
            return {'status': 'ERROR', 'message': 'Group not found'}

if __name__ == "__main__":
    j = Chat()