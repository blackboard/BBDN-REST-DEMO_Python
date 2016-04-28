"""
Copyright (C) 2016, Blackboard Inc.
All rights reserved.
Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
Neither the name of Blackboard Inc. nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY BLACKBOARD INC ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL BLACKBOARD INC. BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from constants import *
import json
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
import ssl
import sys

requests.packages.urllib3.disable_warnings()

#Tls1Adapter allows for connection to sites with non-CA/self-signed
#  certificates e.g.: Learn Dev VM
class Tls1Adapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=ssl.PROTOCOL_TLSv1)

class DataSource():


    def __init__(self, target_url, token):
        self.target_url = target_url
        self.token = token
        self.datasource_PK1 = None
        self.DATASOURCES_PATH = '/learn/api/public/v1/dataSources' #create(POST)/get(GET)
        self.DATASOURCE_PATH = '/learn/api/public/v1/dataSources/externalId:'

    def execute(self, command, token):

        if "create" in command:
            print('[DataSource:execute] : ' + command)
            self.createDataSource(token)
        elif "read" in command:
            print('[DataSource:execute] : ' + command)
            self.getDataSource(token)
        elif "read_all" in command:
            print('[DataSource:execute] : ' + command)
            self.getDataSources(token)
        elif "update" in command:
            print('[DataSource:execute] : ' + command)
            self.updateDataSource(token)
        elif "delete" in command:
            print('[DataSource:execute] : ' + command)
            self.deleteDataSource(token)


    def getDataSources(self, token):
        print('[DataSource:getDataSources] token: ' + token)
        #"Authorization: Bearer $token"
        authStr = 'Bearer ' + token
        print('[DataSource:getDataSources] authStr: ' + authStr)
        session = requests.session()
        session.mount('https://', Tls1Adapter()) # remove for production with commercial cert
        print("[DataSource:getDataSources()] GET Request URL: https://" + self.target_url + self.DATASOURCES_PATH)
        print("[DataSource:getDataSources()] JSON Payload: NONE REQUIRED")
        r = session.get("https://" + self.target_url + self.DATASOURCES_PATH, headers={'Authorization':authStr}, verify=False)
        print("[DataSource:getDataSources()] STATUS CODE: " + str(r.status_code) )
        res = json.loads(r.text)
        print("[DataSource:getDataSources()] RESPONSE: \n" + json.dumps(res,indent=4, separators=(',', ': ')))


    def createDataSource(self, token):
        #"Authorization: Bearer $token"
        authStr = 'Bearer ' + token
        self.PAYLOAD = {
            "externalId":DSKEXTERNALID,
            "description":"Data Source used for REST demo"
        }

        session = requests.session()
        session.mount('https://', Tls1Adapter()) # remove for production with commercial cert

        print("[DataSource:createDataSource()] POST Request URL: https://" + self.target_url + self.DATASOURCES_PATH)
        print("[DataSource:createDataSource()] JSON Payload: \n" + json.dumps(self.PAYLOAD,indent=4, separators=(',', ': ')))
        r = session.post("https://" + self.target_url + self.DATASOURCES_PATH, data=json.dumps(self.PAYLOAD), headers={'Authorization':authStr, 'Content-Type':'application/json'}, verify=False)

        print("[DataSource:createDataSource()] STATUS CODE: " + str(r.status_code) )
        res = json.loads(r.text)
        print("[DataSource:createDataSource()] RESPONSE: \n" + json.dumps(res,indent=4, separators=(',', ': ')))

        if r.status_code == 201:
            parsed_json = json.loads(r.text)
            self.datasource_PK1 = parsed_json['id']
            print ("[DataSource:createDataSource()] datasource_PK1:" + self.datasource_PK1)

    def getDataSource(self, token):
        print('[DataSource:getDataSource()] token: ' + token)
        #"Authorization: Bearer $token"
        authStr = 'Bearer ' + token
        print('[DataSource:getDataSource()] authStr: ' + authStr)
        session = requests.session()
        session.mount('https://', Tls1Adapter()) # remove for production with commercial cert

        print("[DataSource:getDataSource()] GET Request URL: https://" + self.target_url + self.DATASOURCE_PATH+DSKEXTERNALID)
        print("[DataSource:getDataSource()] JSON Payload: NONE REQUIRED")
        r = session.get("https://" + self.target_url + self.DATASOURCE_PATH+DSKEXTERNALID, headers={'Authorization':authStr, 'Content-Type':'application/json'}, verify=False)

        print("[DataSource:getDataSource()] STATUS CODE: " + str(r.status_code) )
        res = json.loads(r.text)
        print("[DataSource:updateDataSource()] RESPONSE: \n" + json.dumps(res,indent=4, separators=(',', ': ')))


        if r.status_code == 200:
            parsed_json = json.loads(r.text)
            self.datasource_PK1 = parsed_json['id']
            print ("[DataSource:getDataSource()] datasource_PK1:" + self.datasource_PK1)



    def updateDataSource(self, token):
        #"Authorization: Bearer $token"
        authStr = 'Bearer ' + token
        print("[DataSource:updateDataSource()] DSKEXTERNALID: " + DSKEXTERNALID)

        self.PAYLOAD = {"description":"Demo Data Source used for REST Python Demo"}

        session = requests.session()
        session.mount('https://', Tls1Adapter()) # remove for production with commercial cert

        print("[DataSource:updateDataSource()] PATCH Request URL: https://" + self.target_url + self.DATASOURCE_PATH + DSKEXTERNALID)
        print("[DataSource:updateDataSource()] JSON Payload: \n" + json.dumps(self.PAYLOAD, indent=4, separators=(',', ': ')))
        r = session.patch("https://" + self.target_url + self.DATASOURCE_PATH+DSKEXTERNALID, data=json.dumps(self.PAYLOAD), headers={'Authorization':authStr, 'Content-Type':'application/json'}, verify=False)

        print("[DataSource:updateDataSource()] STATUS CODE: " + str(r.status_code) )
        res = json.loads(r.text)
        print("[DataSource:updateDataSource()] RESPONSE: \n" + json.dumps(res,indent=4, separators=(',', ': ')))


    def deleteDataSource(self, token):
        #"Authorization: Bearer $token"
        authStr = 'Bearer ' + token
        print("[DataSource:deleteDataSource()] DSKEXTERNALID: " + DSKEXTERNALID)

        session = requests.session()
        session.mount('https://', Tls1Adapter()) # remove for production with commercial cert

        print("[DataSource:deleteDataSource()] DELETE Request URL: https://" + self.target_url + self.DATASOURCE_PATH + DSKEXTERNALID)
        print("[DataSource:deleteDataSource()] JSON Payload: NONE REQUIRED")
        r = session.delete("https://" + self.target_url + self.DATASOURCE_PATH+DSKEXTERNALID, headers={'Authorization':authStr, 'Content-Type':'application/json'}, verify=False)

        print("[DataSource:deleteDataSource()] STATUS CODE: " + str(r.status_code) )
        res = json.loads(r.text)
        print("[DataSource:deleteDataSource()] RESPONSE: \n" + json.dumps(res,indent=4, separators=(',', ': ')))
