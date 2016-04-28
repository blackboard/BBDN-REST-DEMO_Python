"""
Copyright (C) 2016, Blackboard Inc.
All rights reserved.
Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
Neither the name of Blackboard Inc. nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY BLACKBOARD INC ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL BLACKBOARD INC. BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import json
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
import ssl
import sys
from constants import *

requests.packages.urllib3.disable_warnings()

#Tls1Adapter allows for connection to sites with non-CA/self-signed
#  certificates e.g.: Learn Dev VM
class Tls1Adapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=ssl.PROTOCOL_TLSv1)

class User():

    def __init__(self, target_url, token):
        self.target_url = target_url
        self.token = token
        self.users_Path = '/learn/api/public/v1/users' #create(POST)/get(GET)
        self.user_Path = '/learn/api/public/v1/users/externalId:'



    def execute(self, command, dsk, token):
        if "create" in command:
            print('[User:execute] : ' + command)
            self.createUser(dsk, token)
        elif "read" in command:
            print('[User:execute] : ' + command)
            self.getUser(token)
        elif "read_all" in command:
            print('[User:execute] : ' + command + "not implemented on server")
            #self.getUsers(token)
        elif "update" in command:
            print('[User:execute] : ' + command)
            self.updateUser(dsk, token)
        elif "delete" in command:
            print('[User:execute] : ' + command)
            self.deleteUser(token)


    def getUsers(self, token):
        print('[User:getUsers] token: ' + token)
        #"Authorization: Bearer $token"
        authStr = 'Bearer ' + token
        print('[User:getUsers] authStr: ' + authStr)
        session = requests.session()
        session.mount('https://', Tls1Adapter()) # remove for production
        print("[User:getUsers()] GET Request URL: https://" + self.target_url + self.users_Path)
        print("[User:getUsers()] JSON Payload: NONE REQUIRED")
        r = session.get("https://" + self.target_url + self.users_Path, headers={'Authorization':authStr}, verify=False)
        print("[User:getUsers()] STATUS CODE: " + str(r.status_code) )
        print("[User:getUsers()] RESPONSE: \n" + json.dumps(self.PAYLOAD, indent=4, separators=(',', ': ')))


    def createUser(self, dsk, token):
        #"Authorization: Bearer $token"
        authStr = 'Bearer ' + token

        self.PAYLOAD = {
            "externalId":USEREXTERNALID,
            "dataSourceId": dsk, #self.dskExternalId, Supported soon.
            "userName":"python_demo",
            "password":"python61",
            "availability": {
                "available": "Yes"
            },
            "name": {
                "given": "Python",
                "family": "Demo",
            },
            "contact": {
                "email": "no.one@ereh.won",
            }
        }

        session = requests.session()
        session.mount('https://', Tls1Adapter()) # remove for production with commercial cert

        print("[User:createUser()] POST Request URL: https://" + self.target_url + self.users_Path)
        print("[User:createUser()] JSON Payload: " + json.dumps(self.PAYLOAD, indent=4, separators=(',', ': ')))
        r = session.post("https://" + self.target_url + self.users_Path, data=json.dumps(self.PAYLOAD), headers={'Authorization':authStr, 'Content-Type':'application/json'}, verify=False)
        print("[User:createUser()] STATUS CODE: " + str(r.status_code) )
        print("[User:createUser()] RESPONSE: \n" + json.dumps(self.PAYLOAD, indent=4, separators=(',', ': ')))


    def getUser(self, token):
        print('[User:getUser()] token: ' + token)
        #"Authorization: Bearer $token"
        authStr = 'Bearer ' + token
        print('[User:getUser()] authStr: ' + authStr)
        session = requests.session()
        session.mount('https://', Tls1Adapter()) # remove for production

        print("[User:getUser()] GET Request URL: https://" + self.target_url + self.user_Path+USEREXTERNALID)
        print("[User:getUser()] JSON Payload: NONE REQUIRED")
        r = session.get("https://" + self.target_url + self.user_Path+USEREXTERNALID, headers={'Authorization':authStr},  verify=False)

        print("[User:getUser()] STATUS CODE: " + str(r.status_code) )
        print("[User:getUser()] RESPONSE: \n" + json.dumps(self.PAYLOAD, indent=4, separators=(',', ': ')))


    def updateUser(self, dsk, token):
        #"Authorization: Bearer $token"
        authStr = 'Bearer ' + token
        print("[User:updateUser()] USEREXTERNALID: " + USEREXTERNALID)

        self.PAYLOAD = {
            "externalId": USEREXTERNALID,
            "dataSourceId": dsk, #self.dskExternalId, Supported soon.
            "userName":"python_demo",
            "password": "python16",
            "availability": {
                "available": "Yes"
            },
            "name": {
                "given": "Python",
                "family": "BbDN",
                "middle": "Demo",
            },
            "contact": {
                "email": "no.one@ereh.won",
            }
        }
        session = requests.session()
        session.mount('https://', Tls1Adapter()) # remove for production with commercial cert

        print("[User:updateUser()] PATCH Request URL: https://" + self.target_url + self.user_Path+USEREXTERNALID)
        print("[User:updateUser()] JSON Payload: " + json.dumps(self.PAYLOAD, indent=4, separators=(',', ': ')))
        r = session.patch("https://" + self.target_url + self.user_Path+USEREXTERNALID, data=json.dumps(self.PAYLOAD), headers={'Authorization':authStr, 'Content-Type':'application/json'}, verify=False)

        print("[User:updateUser()] STATUS CODE: " + str(r.status_code) )
        res = json.loads(r.text)
        print("[User:updateUser()] RESPONSE: \n" + json.dumps(res,indent=4, separators=(',', ': ')))


    def deleteUser(self, token):
        #"Authorization: Bearer $token"
        authStr = 'Bearer ' + token
        print("[User:deleteUser()] USEREXTERNALID: " + USEREXTERNALID)

        session = requests.session()
        session.mount('https://', Tls1Adapter()) # remove for production with commercial cert

        print("[User:deleteUser()] DELETE Request URL: https://" + self.target_url + self.user_Path+USEREXTERNALID)
        print("[User:deleteUser()] JSON Payload: NONE REQUIRED")
        r = session.delete("https://" + self.target_url + self.user_Path+USEREXTERNALID, headers={'Authorization':authStr}, verify=False)

        print("[User:deleteUser()] STATUS CODE: " + str(r.status_code) )
        res = json.loads(r.text)
        print("[User:deleteUser()] RESPONSE: \n" + json.dumps(res,indent=4, separators=(',', ': ')))
