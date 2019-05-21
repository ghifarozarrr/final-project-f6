import socket
import os
import json
import base64
import traceback
import sqlite3
import time
import datetime

TARGET_IP = '127.0.0.1'
TARGET_PORT = 8889

class ChatClient:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (TARGET_IP, TARGET_PORT)
        self.sock.connect(self.server_address)
        self.tokenid = ''
        self.temp = ''

    def proses(self, cmdline):
        j = cmdline.split(' ')
        try:
            command = j[0].strip()
            if (command == 'auth_register'):
                if self.tokenid != '':
                    return 'Logout first to register'
                username = j[1].strip()
                password = j[2].strip()
                return self.register(username, password)

            elif (command == 'auth_login'):
                username = j[1].strip()
                password = j[2].strip()
                self.temp=j[1].strip()
                return self.login(username, password)

            elif (command == 'auth_logout'):
                return self.logout(self.tokenid)

            elif(command == 'ls'):
                return self.ls()

            elif (command == 'inbox'):
                return self.inbox()

            elif (command == 'send'):
                usernameto = j[1].strip()
                message = ""
                for w in j[2:]:
                    message = "{} {}".format(message, w)
                return self.sendmessage(usernameto, message)

            elif (command == 'send_file'):
                usernameto = j[1].strip()
                message = ''
                for w in j[2:]:
                    message = '{} {}'.format(message, w)
                return self.sendfile(usernameto, message)

            elif (command == 'download_file'):
                filename = j[1].strip()
                return self.download_file(filename)

            elif (command == 'mkgr'):
                group = j[1].strip()
                return self.mkgr(group)

            elif (command == 'join'):
                group = j[1].strip()
                return self.join(group)

            elif (command == 'ls_group'):
                return self.ls_group()

            elif (command == 'ls_member'):
                group = j[1].strip()
                return self.ls_member(group)

            elif (command == 'leave'):
                group = j[1].strip()
                return self.leave(group)

            elif (command == 'sendgroup'):
                group = j[1].strip()
                message = ""
                for w in j[2:]:
                    message = "{} {}".format(message, w)
                return self.sendgroup(group, message)

            elif (command == 'inboxgroup'):
                group = j[1].strip()
                return self.inboxgroup(group)

            elif (command == 'sendgroup_file'):
                group = j[1].strip()
                message = ''
                for w in j[2:]:
                    message = '{} {}'.format(message, w)
                return self.sendgroup_file(group, message)

            elif (command == 'downloadgroup_file'):
                group = j[1].strip()
                message = j[2].strip()
                return self.downloadgroup_file(group, message)

            else:
                return '*Command is incorrect'
        except IndexError:
            return '-Command is incorrect'

    def start_file_socket(self):
        try:
            self.file_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.file_socket.settimeout(10)
            self.file_socket.connect((TARGET_IP, 1338))
        except Exception as e:
            print 'Error ' + str(e)
            traceback.print_exc()

    def send_string_without_rcv(self, string):
        try:
            self.sock.sendall(string)
        except:
            self.sock.close()

    def receive_msg_no_loop(self):
        receivemsg = ""
        data = self.sock.recv(4096)
        if (data):
            receivemsg = "{}{}".format(receivemsg, data)
            if receivemsg[-4:] == "\r\n\r\n":
                return json.loads(receivemsg)['message']

    def sendstring(self, string):
        try:
            self.sock.sendall(string)
            receivemsg = ""
            while True:
                data = self.sock.recv(10)
                if (data):
                    receivemsg = "{}{}".format(receivemsg, data)
                    if receivemsg[-4:] == "\r\n\r\n":
                        return json.loads(receivemsg)
        except:
            self.sock.close()

    def register(self, username, password):
        string = "auth_register {} {} \r\n".format(username, password)
        result = self.sendstring(string)
        if result['status'] == 'OK':
            return "username {} registered, please log in".format(username)
        else:
            return "Error, {}".format(result['message'])

    def login(self, username, password):
        string = "auth_login {} {} \r\n".format(username, password)
        result = self.sendstring(string)
        if result['status'] == 'OK':
            self.tokenid = result['tokenid']
            return "username {} logged in, token {} ".format(username, self.tokenid)
        else:
            return "Error, {}".format(result['message'])

    def logout(self, sessionid):
        string = "auth_logout {} \r\n".format(sessionid)
        result = self.sendstring(string)
        if result['status'] == 'OK':
            self.tokenid = ""
            return "{}".format(result['message'])
        else:
            return "Error, {}".format(result['message'])

    def ls(self):
        if (self.tokenid == ""):
            return "Error, not authorized"
        string = "ls {} \r\n".format(self.tokenid)
        result = self.sendstring(string)
        if result['status'] == 'OK':
            return "List user: {}".format(json.dumps(result['messages']))
        else:
            return "No more user"

    def inbox(self):
        if (self.tokenid == ""):
            return "Error, not authorized"
        string = "inbox {} \r\n".format(self.tokenid)
        result = self.sendstring(string)
        if result['status'] == 'OK':
            return "{}".format(json.dumps(result['messages']))
        else:
            return "Error, {}".format(result['message'])

    def sendmessage(self, usernameto, message):
        if (self.tokenid == ''):
            return "Error, not authorized"
        string = "send {} {} {} \r\n".format(self.tokenid, usernameto, message)
        result = self.sendstring(string)
        if result['status'] == 'OK':
            return "message sent to {}".format(usernameto)
        else:
            return "Error, {}".format(result['message'])

    def sendfile(self, usernameto, message):
        if (self.tokenid == ""):
            return "Error, please login first"

        db_conn = sqlite3.connect('progjar.db')
        db = db_conn.cursor()

        db.execute('SELECT * FROM user where user_name=?', (usernameto,))
        cek = db.fetchone()

        if cek != None:
            file_name = message.lstrip()
            if os.path.exists(file_name):
                string = "send_file {} {} {} \r\n".format(self.tokenid, usernameto, file_name)
                self.send_string_without_rcv(string)
                time.sleep(1.1)
                self.start_file_socket()
                f = open(file_name, 'rb')
                bytes = f.read(1024)
                totalsend = len(bytes)
                filesize = os.path.getsize(file_name)
                while True:
                    self.file_socket.send(bytes)
                    bytes = f.read(1024)
                    print "{0:.2f}".format((totalsend / float(filesize)) * 100) + "% Done"
                    totalsend += len(bytes)
                    if not bytes:
                        break
                f.close()
                self.file_socket.close()
                return self.receive_msg_no_loop()
            else:
                return "Error, file not found"
        else:
            return "Error, user not found"

    def download_file(self, message):
        if (self.tokenid == ''):
            return "Error, please login first"

        file_name = message.lstrip()

        if not os.path.exists(os.path.join(os.getcwd(), 'download', self.temp)):
            folder = os.makedirs(os.path.join(os.getcwd(), 'download', self.temp))

        lokasi = "upload" + "/" + file_name
        if os.path.isfile(lokasi):
            print 'its a file!'
            string = "download_file {} {} \r\n".format(self.tokenid, file_name)
            self.send_string_without_rcv(string)
            time.sleep(1.1)
            self.start_file_socket()
            f = open(os.path.join(os.getcwd(), 'download', self.temp, file_name), 'wb')
            while True:
                bytes = self.file_socket.recv(1024)
                if not bytes:
                    break
                f.write(bytes)
            f.close()
            self.file_socket.close()
            return self.receive_msg_no_loop()
        else:
            return "Error, file not found"

    def mkgr(self, group_name):
        if (self.tokenid == ""):
            return "Error, not authorized"
        string = "mkgr {} {} \r\n".format(group_name, self.tokenid)
        result = self.sendstring(string)
        if result['status'] == 'OK':
            return "Group {} successfully created".format(group_name)
        else:
            return "Error, {}".format(result['message'])

    def join(self, group_name):
        if (self.tokenid == ""):
            return "Error, not authorized"
        string = "join {} {} \r\n".format(group_name, self.tokenid)
        result = self.sendstring(string)
        if result['status'] == 'OK':
            return "You're successfully join {}".format(group_name)
        else:
            return "Error, {}".format(result['message'])

    def ls_group(self):
        if (self.tokenid == ""):
            return "Error, not authorized"
        string = "ls_group {} \r\n".format(self.tokenid)
        result = self.sendstring(string)
        if result['status'] == 'OK':
            return "List group: {}".format(json.dumps(result['messages']))
        else:
            return "No more group"

    def ls_member(self, group_name):
        if (self.tokenid == ""):
            return "Error, not authorized"
        string = "ls_member {} {} \r\n".format(group_name, self.tokenid)
        result = self.sendstring(string)
        if result['status'] == 'OK':
            return "Member group {}".format(json.dumps(result['messages']))
        else:
            return "Error, {}".format(result['message'])

    def leave(self, group_name):
        if (self.tokenid == ""):
            return "Error, not authorized"
        string = "leave {} {} \r\n".format(group_name, self.tokenid)
        result = self.sendstring(string)
        if result['status'] == 'OK':
            return "You're successfully left the group."
        else:
            return "Error, {}".format(result['message'])

    def sendgroup(self, group_name, message):
        if (self.tokenid == ""):
            return "Error, not authorized"
        string = "sendgroup {} {} {} \r\n".format(group_name, self.tokenid, message)
        result = self.sendstring(string)
        if result['status'] == 'OK':
            return "Message sent."
        else:
            return "Error, {}".format(result['message'])

    def inboxgroup(self, group_name):
        if (self.tokenid == ""):
            return "Error, not authorized"
        string = "inboxgroup {} {} \r\n".format(group_name, self.tokenid)
        result = self.sendstring(string)
        if result['status'] == 'OK':
            return "{}".format(json.dumps(result['messages']))
        else:
            return "Error, {}".format(result['message'])

    def sendgroup_file(self, group_name, message):
        if (self.tokenid == ""):
            return "Error, please login first"

        db_conn = sqlite3.connect('progjar.db')
        db = db_conn.cursor()
        db.execute('SELECT * FROM groupchat where group_name=?', (group_name,))
        cek2 = db.fetchone()
        if cek2 != None:
            file_name = message.lstrip()
            if os.path.exists(file_name):
                string = "sendgroup_file {} {} {} \r\n".format(self.tokenid, group_name, file_name)
                self.send_string_without_rcv(string)
                time.sleep(1.1)
                self.start_file_socket()
                f = open(file_name, 'rb')
                bytes = f.read(1024)
                totalsend = len(bytes)
                filesize = os.path.getsize(file_name)
                while True:
                    self.file_socket.send(bytes)
                    bytes = f.read(1024)
                    print "{0:.2f}".format((totalsend / float(filesize)) * 100) + "% Done"
                    totalsend += len(bytes)
                    if not bytes:
                        break
                f.close()
                self.file_socket.close()
                return self.receive_msg_no_loop()
            else:
                return "Error, file not found"
        else:
            return "Error, group not found"

    def downloadgroup_file(self, group_name, message):
        if (self.tokenid == ''):
            return "Error, please login first"

        file_name = message.lstrip()
        if not os.path.exists(os.path.join(os.getcwd(), 'downloadgroup', self.temp)):
            folder = os.makedirs(os.path.join(os.getcwd(), 'downloadgroup', self.temp))

        db_conn = sqlite3.connect('progjar.db')
        db = db_conn.cursor()
        db.execute('SELECT * FROM groupchat where group_name=?', (group_name,))
        cek2 = db.fetchone()
        if cek2 != None:
            lokasi = "upload" + "/" + file_name
            if os.path.isfile(lokasi):
                string = "downloadgroup_file {} {} {} \r\n".format(self.tokenid, group_name, file_name)
                self.send_string_without_rcv(string)

                self.start_file_socket()
                f = open(os.path.join(os.getcwd(), 'downloadgroup', self.temp, file_name), 'wb')
                while True:
                    bytes = self.file_socket.recv(1024)
                    if not bytes:
                        break
                    f.write(bytes)
                f.close()
                self.file_socket.close()
                return self.receive_msg_no_loop()
            else:
                return "Error, file not found"
        else:
            return "Error, group not found"

if __name__ == "__main__":
    cc = ChatClient()
    while True:
        cmdline = raw_input("Command {}:".format(cc.tokenid))
        print cc.proses(cmdline)