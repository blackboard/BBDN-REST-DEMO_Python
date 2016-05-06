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

class Term():

    def __init__(self, target_url, token):
        self.target_url = target_url
        self.token = token
        self.terms_Path = '/learn/api/public/v1/terms' #create(POST)/get(GET)
        self.term_Path = '/learn/api/public/v1/terms/externalId:'


    def execute(self, command, dsk, token):
        if "create" in command:
            print('[Term:execute] : ' + command)
            self.createTerm(dsk, token)
        elif "read_all" in command:
            print('[Term:execute] : ' + command)
            self.getTerms(token)
        elif "read" in command:
            print('[Term:execute] : ' + command)
            self.getTerm(token)
        elif "update" in command:
            print('[Term:execute] : ' + command)
            self.updateTerm(dsk, token)
        elif "delete" in command:
            print('[Term:execute] : ' + command)
            self.deleteTerm(token)


    def getTerms(self, token):
        print('[Term:getTerms] token: ' + token)
        #"Authorization: Bearer $token"
        authStr = 'Bearer ' + token
        print('[Term:getTerms] authStr: ' + authStr)
        session = requests.session()
        session.mount('https://', Tls1Adapter()) # remove for production
        print("[Term:getTerms()] GET Request URL: https://" + self.target_url + self.terms_Path)
        print("[Term:getTerms()] JSON Payload: NONE REQUIRED")
        r = session.get("https://" + self.target_url + self.terms_Path, headers={'Authorization':authStr}, verify=False)
        print("[Term:getTerms()] STATUS CODE: " + str(r.status_code) )
        print("[Term:getTerms()] RESPONSE:")
        if r.text:
            res = json.loads(r.text)
            print(json.dumps(res,indent=4, separators=(',', ': ')))
        else:
            print("NONE")


    def createTerm(self, dsk, token):
        #"Authorization: Bearer $token"
        authStr = 'Bearer ' + token
        self.PAYLOAD = {
            "externalId":TERMEXTERNALID,
            "dataSourceId": "externalId:%s" % DSKEXTERNALID,  
            "name":"REST Demo Term",
            "description": "Term used for REST demo",
            "availability": {
                "duration":"Continuous"
            }
        }

        session = requests.session()
        session.mount('https://', Tls1Adapter()) # remove for production with commercial cert

        print("[Term:createTerm()] POST Request URL: https://" + self.target_url + self.terms_Path)
        print("[Term:createTerm()] JSON Payload: " + json.dumps(self.PAYLOAD, indent=4, separators=(',', ': ')))
        r = session.post("https://" + self.target_url + self.terms_Path, data=json.dumps(self.PAYLOAD), headers={'Authorization':authStr, 'Content-Type':'application/json'}, verify=False)

        print("[Term:createTerm()] STATUS CODE: " + str(r.status_code) )
        print("[Term:createTerm()] RESPONSE:")
        if r.text:
            res = json.loads(r.text)
            print(json.dumps(res,indent=4, separators=(',', ': ')))
        else:
            print("NONE")

    def getTerm(self, token):
        print('[Term:getTerm()] token: ' + token)
        #"Authorization: Bearer $token"
        authStr = 'Bearer ' + token
        print('[Term:getTerm()] authStr: ' + authStr)
        session = requests.session()
        session.mount('https://', Tls1Adapter()) # remove for production

        print("[Term:getTerm()] GET Request URL: https://" + self.target_url + self.term_Path+TERMEXTERNALID)
        print("[Term:getTerm()] JSON Payload: NONE REQUIRED")
        r = session.get("https://" + self.target_url + self.term_Path+TERMEXTERNALID, headers={'Authorization':authStr},  verify=False)

        print("[Term:getTerm()] STATUS CODE: " + str(r.status_code) )
        print("[Term:getTerm()] RESPONSE:")
        if r.text:
            res = json.loads(r.text)
            print(json.dumps(res,indent=4, separators=(',', ': ')))
        else:
            print("NONE")

    def updateTerm(self, dsk, token):
        #"Authorization: Bearer $token"
        authStr = 'Bearer ' + token
        print("[Term:updateTerm()] Term ExternalId: " + TERMEXTERNALID)

        self.PAYLOAD = {
            "externalId":TERMEXTERNALID,
            "dataSourceId": "externalId:%s" % DSKEXTERNALID, 
            "name":"REST Python Demo Term",
            "description": "Term used for REST Python demo",
            "availability": {
                "duration":"continuous"
            }
        }
        session = requests.session()
        session.mount('https://', Tls1Adapter()) # remove for production with commercial cert

        print("[Term:updateTerm()] PATCH Request URL: https://" + self.target_url + self.term_Path+TERMEXTERNALID)
        print("[Term:updateTerm()] JSON Payload: " + json.dumps(self.PAYLOAD, indent=4, separators=(',', ': ')))
        r = session.patch("https://" + self.target_url + self.term_Path+TERMEXTERNALID, data=json.dumps(self.PAYLOAD), headers={'Authorization':authStr, 'Content-Type':'application/json'}, verify=False)

        print("[Term:updateTerm()] STATUS CODE: " + str(r.status_code) )
        print("[Term:updateTerm()] RESPONSE:")
        if r.text:
            res = json.loads(r.text)
            print(json.dumps(res,indent=4, separators=(',', ': ')))
        else:
            print("NONE")

    def deleteTerm(self, token):
        #"Authorization: Bearer $token"
        authStr = 'Bearer ' + token
        print("[Term:deleteTerm()] Term ExternalId: " + TERMEXTERNALID)

        session = requests.session()
        session.mount('https://', Tls1Adapter()) # remove for production with commercial cert

        print("[Term:getTerms()] DELETE Request URL: https://" + self.target_url + self.term_Path+TERMEXTERNALID)
        print("[Term:getTerms()] JSON Payload: NONE REQUIRED")
        #r = session.delete("https://" + self.target_url + self.term_Path+self.termExternalId, headers={'Authorization':authStr}, verify=False)
        r = session.delete("https://" + self.target_url+self.term_Path+TERMEXTERNALID, headers={'Authorization':authStr}, verify=False)
        print("[Term:deleteTerm()] STATUS CODE: " + str(r.status_code) )
        print("[Term:deleteTerm()] RESPONSE:")
        if r.text:
            res = json.loads(r.text)
            print(json.dumps(res,indent=4, separators=(',', ': ')))
        else:
            print("NONE")