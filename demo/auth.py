"""
Copyright (C) 2016, Blackboard Inc.
All rights reserved.
Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
Neither the name of Blackboard Inc. nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY BLACKBOARD INC ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL BLACKBOARD INC. BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

"""
PYTHON and Self-signed certificates:
    To enable code to recognize the DVM self signed certificate you have to provide Python
    with the public Key 

    1. Start the DVM and ssh into it...
    $ vagrant up
    $ vagrant ssh
    2. Copy the keystore password from the config file
    $ cd /usr/local/blackboard/config
    $ more /usr/local/blackboard/config/bb-config.properties
        find the keystore password and copy it - you will use this in step 3 for 
        exporting the pem file
    3. Export the cert and keys 
    $ cd /usr/local/blackboard/config/keystores
    $ keytool -exportcert -alias tomcat -keystore tomcat.keystore -rfc -file /vagrant/keytool_crt.pem
    4. Make sure you can read the file:
    $ openssl x509 -in /vagrant/keytool_crt.pem -inform pem -noout -text
    4. copy the .pem file to a location your project can access it.
    5. update config.py to point to your .pem file
    6. add dev.bbdn.local to your hosts file and save:
        127.0.0.1	localhost dev.bbdn.local
    7. test access to to your DVM using dev.bbdn.local, if it doesn't work restart and retry

    now for all requests against your DVM the pem will be used to verify the server
    NOTE: that for production code you should change 'verify=CERTPATH' to 'verify=False' if 
    not using the server derived .pem file, or remove 'verify=...' completely if using 
    commercial certificates.
    see http://docs.python-requests.org/en/master/user/advanced/ for more information on 
    SSL sessions in Python.
"""

import json
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
import datetime
import time
#from datetime import now
import ssl
import sys
from constants import *

#Tls1Adapter allows for connection to sites with non-CA/self-signed
#  certificates e.g.: Learn Dev VM
# May be removed if you migrated the cert as outlined in auth.py
class Tls1Adapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=ssl.PROTOCOL_TLSv1)

class AuthToken():
    target_url = ''

    def __init__(self, URL):
        
        self.KEY = "insert_your_application_key_here"
        self.SECRET = "insert_your_application_secret_here"

        #self.SECRET = "biExBJNI1IXiBBXpV8g01JJJjmXKHSg7" #Example Only. Change to your secret
        #self.KEY = "9cb9384a-3662-410d-9953-fe73cc374b81"#Example Only. Change to your key

        self.CREDENTIALS = 'client_credentials'
        self.PAYLOAD = {
            'grant_type':'client_credentials'
        }
        self.TOKEN = None
        self.target_url = URL
        self.EXPIRES_AT = ''
        self.cert_path='./trusted/keytool_crt.pem'

    def getKey(self):
        return self.KEY

    def getSecret(self):
        return self.SECRET

    def setToken(self):
        oauth_path = '/learn/api/public/v1/oauth2/token'
        OAUTH_URL = 'https://' + self.target_url + oauth_path

        if self.TOKEN is None:
            session = requests.session()
            #session.mount('https://', Tls1Adapter()) # remove for production

        # Authenticate
            print("[auth:setToken] POST Request URL: " + OAUTH_URL)
            print("[auth:setToken] JSON Payload: \n" + json.dumps(self.PAYLOAD, indent=4, separators=(',', ': ')))
            #r = requests.post(url, data=data, verify='/path/to/public_key.pem')
            r = session.post(OAUTH_URL, data=self.PAYLOAD, auth=(self.KEY, self.SECRET), verify=False)
#            r = session.post(OAUTH_URL, data=self.PAYLOAD, auth=(self.KEY, self.SECRET), verify=CERTPATH)

            print("[auth:setToken()] STATUS CODE: " + str(r.status_code) )
            #strip quotes from result for better dumps
            res = json.loads(r.text)
            print("[auth:setToken()] RESPONSE: \n" + json.dumps(res,indent=4, separators=(',', ': ')))

            if r.status_code == 200:
                parsed_json = json.loads(r.text)
                self.TOKEN = parsed_json['access_token']
                self.EXPIRES = parsed_json['expires_in']
                m, s = divmod(self.EXPIRES, 60)
                #h, m = divmod(m, 60)
                #print "%d:%02d:%02d" % (h, m, s)
                self.NOW = datetime.datetime.now()
                self.EXPIRES_AT = self.NOW + datetime.timedelta(seconds = s, minutes = m)
                print ("[auth:setToken()] Token Expires at " + self.EXPIRES_AT.strftime("%H:%M:%S"))

                print ("[auth:setToken()] TOKEN: " + self.TOKEN)

                #there is the possibility the reaquired token may expire
                #before we are done so perform expiration sanity check...
                if self.isExpired(self.EXPIRES_AT):
                    self.setToken()

            else:
                print("[auth:setToken()] ERROR")
        else:
            print ("[auth:setToken()] TOKEN set")

    def getToken(self):
        #if token time is less than a one second then
        # print that we are pausing to clear
        # re-auth and return the new token
        if self.isExpired(self.EXPIRES_AT):
            self.setToken()

        return self.TOKEN

    def revokeToken(self):
        revoke_path = '/learn/api/public/v1/oauth2/revoke'
        revoke_URL = 'https://' + self.target_url + revoke_path

        print("[auth:revokeToken()] KEY: " + self.KEY)
        print("[auth:revokeToken()] SECRET: " + self.SECRET)
        print("[auth:revokeToken()] TOKEN: " + self.TOKEN)
        print("[auth:revokeToken()] revoke_URL: " + revoke_URL)
        self.PAYLOAD = {
            'token':self.TOKEN
        }

        if self.TOKEN != '':
            print("[auth:revokeToken()] TOKEN not empty...able to revoke")
            print("[auth:revokeToken()] POST PAYLOAD: ")
            for keys,values in self.PAYLOAD.items():
                print("\t\t\t" + keys + ":" + values)
            session = requests.session()
            session.mount('https://', Tls1Adapter()) # remove for production

        # revoke token
            print("[auth:revokeToken] Request URL: " + revoke_URL)
            print("[auth:revokeToken] JSON Payload: \n " + json.dumps(self.PAYLOAD, indent=4, separators=(',', ': ')))
            r = session.post(revoke_URL, data=self.PAYLOAD, auth=(self.KEY, self.SECRET), verify=CERTPATH)

            print("[auth:revokeToken()] STATUS CODE: " + str(r.status_code) )
            print("[auth:revokeToken()] RESPONSE: " + r.text)

            if r.status_code == 200:
                print("[auth:revokeToken()] Token Revoked")
            else:
                print("[auth] ERROR on token revoke")
        else:
            print ("[auth:revokeToken()] Must have set a token to revoke a token...")


    def isExpired(self, expiration_datetime):
        expired = False
        print ("[auth:isExpired()] Token Expires at " + expiration_datetime.strftime("%H:%M:%S"))

        time_left = (expiration_datetime - datetime.datetime.now()).total_seconds()
        print ("[auth:isExpired()] Time Left on Token (in seconds): " + str(time_left))
        if time_left < 1:
            print ("[auth:isExpired()] Token almost expired retrieving new token in two seconds.")
            time.sleep( 1 )
            expired = True

        return expired
