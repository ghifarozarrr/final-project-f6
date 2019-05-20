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

            elif (command == 'inbox'):
                sessionid = j[1].strip()
                username = self.sessions[sessionid]['username']
                print "inbox {}".format(sessionid)
                return self.get_inbox(username)
        
            elif (command == 'mkgr'):
                group = j[1].strip()
                sessionid = j[2].strip()
                print "creating group {}...".format(group)
                return self.mkgr(group, sessionid)
            elif (command == 'join'):
                group = j[1].strip()
                sessionid = j[2].strip()
                print "{} is joining {}...".format(self.sessions[sessionid]['username'], group)
                return self.join(group, sessionid)
            elif (command == 'listgroup'):
                group = j[1].strip()
                sessionid = j[2].strip()
                print "{} {}".format(command, group)
                return self.listgroup(group, sessionid)
            elif (command == 'leave'):
                group = j[1].strip()
                sessionid = j[2].strip()
                print "{} {}".format(command, group)
                return self.leave(group, sessionid)
            elif (command == 'sendgroup'):
                group = j[1].strip()
                sessionid = j[2].strip()
                message = ""
                for w in j[3:]:
                    message = "{} {}".format(message, w)
                print "{} is sending message to group : {}".format(self.sessions[sessionid]['username'], group)
                return self.sendgroup(group, sessionid, message)
            elif (command == 'inboxgroup'):
                group = j[1].strip()
                sessionid = j[2].strip()
                print "inboxgroup {}".format(group)
                return self.inboxgroup(group, sessionid)
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

        db.execute('SELECT * FROM user where user_name=?', (username_dest,))
        dest = db.fetchone()
        user = {'nama': dest[1], 'password': dest[2], 'incoming': {}, 'outgoing': {}}
        self.users[dest[1]] = user

        s_fr = self.get_user(username_from)
        s_to = self.get_user(username_dest)

        if (s_fr == False or s_to == False):
            return {'status': 'ERROR', 'message': 'User not found'}

        message = {'msg_from': s_fr['nama'], 'msg_to': s_to['nama'], 'msg': message}
        inqueue_receiver = s_to['incoming']
        try:
            db.execute('INSERT INTO chat (sender_id, receiver_id, message, type, received_time) values(?, ?, ?, ?, ?)', (username_from, username_dest, str(message), 'chat', datetime.datetime.now()))
            db_conn.commit()
        except KeyError:
            inqueue_receiver[username_from] = Queue()
            inqueue_receiver[username_from].put(message)
        return {'status': 'OK', 'message': 'Message Sent'}

    def mkgr(self, group_name, sessionid):
        if (group_name in self.groups):
            return {'status': 'ERROR', 'message': 'Group does exist'}
        self.groups[group_name] = {'group_name': group_name, 'log': [], 'users': []}
        creator = self.sessions[sessionid]['username']
        self.groups[group_name]['users'].append(creator)
        return {'status': 'OK', 'message': self.groups[group_name]}

    def join(self, group_name, sessionid):
        if (group_name not in self.groups):
            return {'status': 'ERROR', 'message': 'Group not found'}
        username = self.sessions[sessionid]['username']
        if (username in self.groups[group_name]['users']):
            return {'status': 'ERROR', 'message': 'You have already in group'}
        self.groups[group_name]['users'].append(username)
        return {'status': 'OK', 'message': 'Group joined successfully'}

    def listgroup(self, group_name, sessionid):
        if (group_name not in self.groups):
            return {'status': 'ERROR', 'message': 'Group not found'}
        username = self.sessions[sessionid]['username']
        if (username not in self.groups[group_name]['users']):
            return {'status': 'ERROR', 'message': 'You are not group member'}
        return {'status': 'OK', 'message': self.groups[group_name]['users']}

    def leave(self, group_name, sessionid):
        if (group_name not in self.groups):
            return {'status': 'ERROR', 'message': 'Group not found'}
        username = self.sessions[sessionid]['username']
        if username in self.groups[group_name]['users']:
            self.groups[group_name]['users'].remove(username)
            return {'status': 'OK', 'message': 'You left the [{}] group'.format(group_name)}
        return {'status': 'ERROR', 'message': 'You are not group member'}

    def sendgroup(self, group_name, sessionid, message):
        if group_name not in self.groups:
            return {'status': 'ERROR', 'message': 'Group not found'}
        username = self.sessions[sessionid]['username']
        if username not in self.groups[group_name]['users']:
            return {'status': 'ERROR', 'message': 'You are not group member'}
        self.groups[group_name]['log'].append({'from': username, 'message': message})
        return {'status': 'OK', 'message': 'Message sent'}

    def inboxgroup(self, group_name, sessionid):
        if group_name not in self.groups:
            return {'status': 'ERROR', 'message': 'Group not found'}
        username = self.sessions[sessionid]['username']
        if username not in self.groups[group_name]['users']:
            return {'status': 'ERROR', 'message': 'You are not group member'}
        return {'status': 'OK', 'messages': self.groups[group_name]['log']}

if __name__ == "__main__":
    j = Chat()