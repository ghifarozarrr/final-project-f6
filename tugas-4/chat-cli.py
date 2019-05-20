import socket
import os
import json
import base64
import traceback
import time

TARGET_IP = "127.0.0.1"
TARGET_PORT = 8889


class ChatClient:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (TARGET_IP,TARGET_PORT)
        self.sock.connect(self.server_address)
        self.tokenid=""

    def proses(self,cmdline):
        j=cmdline.split(" ")
        try:
            command=j[0].strip()
            if (command=='auth_register'):
                if self.tokenid != '':
                    return 'Logout first to register'
                username=j[1].strip()
                password=j[2].strip()
                return self.register(username,password)

            elif (command=='auth_login'):
                username=j[1].strip()
                password=j[2].strip()
                return self.login(username,password)

            elif (command=='auth_logout'):
                return self.logout(self.tokenid)

            elif (command=='send'):
                usernameto = j[1].strip()
                message=""
                for w in j[2:]:
                    message="{} {}" . format(message,w)
                return self.sendmessage(usernameto,message)
            elif (command=='inbox'):
                return self.inbox()
            
            elif (command == 'mkgr'):
                group = j[1].strip()
                return self.mkgr(group)
            elif (command == 'join'):
                group = j[1].strip()
                return self.join(group)
            elif (command == 'listgroup'):
                group = j[1].strip()
                return self.listgroup(group)
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
            else:
                return "*Maaf, command tidak benar"
        except IndexError:
            return "-Maaf, command tidak benar"

    def sendstring(self,string):
        try:
            self.sock.sendall(string)
            receivemsg = ""
            while True:
                data = self.sock.recv(10)
                if (data):
                    receivemsg = "{}{}" . format(receivemsg,data)
                    if receivemsg[-4:]=="\r\n\r\n":
                        return json.loads(receivemsg)
        except:
            self.sock.close()

    def register(self,username,password):
        string="auth_register {} {} \r\n" . format(username,password)
        result = self.sendstring(string)
        if result['status']=='OK':
            return "username {} registered, please log in" .format(username)
        else:
            return "Error, {}" . format(result['message'])

    def login(self,username,password):
        string="auth_login {} {} \r\n" . format(username,password)
        result = self.sendstring(string)
        if result['status']=='OK':
            self.tokenid=result['tokenid']
            return "username {} logged in, token {} " .format(username,self.tokenid)
        else:
            return "Error, {}" . format(result['message'])

    def logout(self, sessionid):
        string="auth_logout {} \r\n" . format(sessionid)
        result = self.sendstring(string)
        if result['status'] == 'OK':
            self.tokenid = ""
            return "{}" . format(result['message'])
        else:
            return "Error, {}" . format(result['message'])

    def sendmessage(self,usernameto="xxx",message="xxx"):
        if (self.tokenid==""):
            return "Error, not authorized"
        string="send {} {} {} \r\n" . format(self.tokenid,usernameto,message)
        result = self.sendstring(string)
        if result['status']=='OK':
            return "message sent to {}" . format(usernameto)
        else:
            return "Error, {}" . format(result['message'])

    def mkgr(self, group_name):
        if (self.tokenid == ""):
            return "Error, not authorized"
        string = "mkgr {} {} \r\n".format(group_name, self.tokenid)
        result = self.sendstring(string)
        if result['status'] == 'OK':
            return "{}".format(json.dumps(result['message']))
        else:
            return "Error, {}".format(result['message'])

    def join(self, group_name):
        if (self.tokenid == ""):
            return "Error, not authorized"
        string = "join {} {} \r\n".format(group_name, self.tokenid)
        result = self.sendstring(string)
        if result['status'] == 'OK':
            return "{}".format(json.dumps(result['message']))
        else:
            return "Error, {}".format(result['message'])

    def listgroup(self, group_name):
        if (self.tokenid == ""):
            return "Error, not authorized"
        string = "listgroup {} {} \r\n".format(group_name, self.tokenid)
        result = self.sendstring(string)
        if result['status'] == 'OK':
            return "{}".format(json.dumps(result['message']))
        else:
            return "Error, {}".format(result['message'])

    def leave(self, group_name):
        if (self.tokenid == ""):
            return "Error, not authorized"
        string = "leave {} {} \r\n".format(group_name, self.tokenid)
        result = self.sendstring(string)
        if result['status'] == 'OK':
            return "{}".format(result['message'])
        else:
            return "Error, {}".format(result['message'])

    def sendgroup(self, group_name, message):
        if (self.tokenid == ""):
            return "Error, not authorized"
        string = "sendgroup {} {} {} \r\n".format(group_name, self.tokenid, message)
        result = self.sendstring(string)
        if result['status'] == 'OK':
            return "{}".format(json.dumps(result['message']))
        else:
            return "Error, {}".format(result['message'])

    def inboxgroup(self, group_name):
        if (self.tokenid == ""):
            return "Error, not authorized"
        string = "inboxgroup {} {} \r\n".format(group_name, self.tokenid)
        result = self.sendstring(string)
        if result['status'] == 'OK':
            return "{}".format(json.dumps(result['messages']))

    def inbox(self):
        if (self.tokenid==""):
            return "Error, not authorized"
        string="inbox {} \r\n" . format(self.tokenid)
        result = self.sendstring(string)
        if result['status']=='OK':
            return "{}" . format(json.dumps(result['messages']))
        else:
            return "Error, {}" . format(result['message'])

if __name__=="__main__":
    cc = ChatClient()
    while True:
        cmdline = raw_input("Command {}:" . format(cc.tokenid))
        print cc.proses(cmdline)