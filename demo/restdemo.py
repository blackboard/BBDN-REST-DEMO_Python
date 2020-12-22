"""
Copyright (C) 2016, Blackboard Inc.
All rights reserved.
Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
Neither the name of Blackboard Inc. nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY BLACKBOARD INC ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL BLACKBOARD INC. BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from auth import AuthToken
from datasource import DataSource
from term import Term
from course import Course
from user import User
from membership import Membership
from constants import *

import sys
import getopt



def main(argv):
    target_url = ''
    COMMAND = ''
    ALL = False
    AUTH = False
    DATASOURCE = False
    TERM = False
    COURSE = False
    USER = False
    MEMBERSHIP = False
    CLEANUP = False

    datasource_PK1 = None
    datasource_session = None

    usageStr = "\nrestdemo.py -t|--target <target root URL> -c|--command <command>\n"
    usageStr += "e.g restdemo.py -t www.myschool.edu -c create_course\n"
    usageStr += "command: <command>_<object> where <command> is one of the following:\n"
    usageStr += "\tcreate, read, read_all_, read_all_course_memberships, read_all_user_memberships, update, delete\n"
    usageStr += "and <object> is one of the following:\n"
    usageStr += "\tdatasource, term, course, user\n"
    usageStr += "-t is required; No -c args will run demo in predetermined order.\n"
    usageStr += "'-c authorize' demomonstrates the authorization process and does not create objects."
    usageStr += "-c commands require a valid datasource PK1 - \n"
    usageStr += "\ta datasource get will be run in these cases, defaulting to create\n"
    usageStr += "\tif the demo datasource does not exist."

    if len(sys.argv) > 1: #there are command line arguments
        try:
            opts, args = getopt.getopt(argv,"ht:c:",["target=","command="])
        except getopt.GetoptError:
            print (usageStr)
            sys.exit(2)
        for opt, arg in opts:
            if opt == '-h':
                print (usageStr)
                sys.exit()
            elif opt == '-d':
                print ("Deleting at end of run.")
                CLEANUP = True
            elif opt in ("-t", "--target"):
                target_url = arg.lstrip()
            elif opt in ("-c", "--command"):
                COMMAND = arg
            else:
                COMMAND = "Run All"
        print ('[main] Target is:', target_url)
        print ('[main] Command is:', COMMAND)


    else:
        print(usageStr)
        sys.exit(2)


    #Set up some booleans for processing flags and order of processing
    if "course" in COMMAND:
        print("[main] Run course command")
        COURSE = True
    elif "membership" in COMMAND:
        print("[main] Run membership command")
        MEMBERSHIP = True
    elif "user" in COMMAND:
        print("[main] Run user command")
        USER = True
    elif "term" in COMMAND:
        print("[main] Run term command")
        TERM = True
    elif "datasource" in COMMAND:
        print("[main] Run datasource command")
        DATASOURCE = True
    elif "authorize" in COMMAND:
        print("[main] Run authorization command")
        AUTH = True
    else:
        print("[main] Empty Command: Run All\n")
        ALL = True

    print ('\n[main] Acquiring auth token...\n')
    authorized_session = AuthToken(target_url)
    authorized_session.setToken()
    print ('\n[main] Returned token: ' + authorized_session.getToken() + '\n')

    if not AUTH:
        #run commands in required order if running ALL
        if DATASOURCE or ALL:
            #process Datasource command
            print("\n[main] Run datasource command: " + ('ALL' if ALL else COMMAND) + '...')
            datasource_session = DataSource(target_url, authorized_session.getToken())
            if 'datasource' in COMMAND:
                datasource_session.execute(COMMAND, authorized_session.getToken())
            else:
                if not datasource_PK1 or datasource_PK1 is None:
                    datasource_session.createDataSource(authorized_session.getToken())
                    datasource_session.getDataSource(authorized_session.getToken())
                    datasource_session.getDataSources(authorized_session.getToken())
                    datasource_session.updateDataSource(authorized_session.getToken())

        if TERM or ALL:
            term_session = Term(target_url, authorized_session.getToken())
            #process term command
            print("\n[main] Run term command: " + ('ALL' if ALL else COMMAND) + '...')
            if 'term' in COMMAND:
                if (('delete' in COMMAND) or ('read' in COMMAND)):
                    print ("[main] Deleting or getting does not require a datasource.")
                else:
                    if not datasource_PK1:
                        print("[main] confirm datasource.")
                        datasource_session = DataSource(target_url, authorized_session.getToken())
                        datasource_session.checkDataSource(authorized_session.getToken())

                term_session.execute(COMMAND, "externalId:"+TERMEXTERNALID, authorized_session.getToken())
            else:
                term_session.getTerms(authorized_session.getToken())
                term_session.createTerm("externalId:"+DSKEXTERNALID, authorized_session.getToken())
                term_session.getTerm(authorized_session.getToken())
                term_session.updateTerm("externalId:"+DSKEXTERNALID, authorized_session.getToken())

        if COURSE or ALL:
            course_session = Course(target_url, authorized_session.getToken())
            #process course command
            print("\n[main] Run course command: " + ('ALL' if ALL else COMMAND) + '...')
            if 'course' in COMMAND:
                if (('delete' in COMMAND) or ('read' in COMMAND)):
                    print ("[main] Deleting or getting does not require a datasource.")
                else:
                    if not datasource_PK1:
                        print("[main] confirm datasource.")
                        datasource_session = DataSource(target_url, authorized_session.getToken())
                        datasource_session.checkDataSource(authorized_session.getToken())

                course_session.execute(COMMAND, "externalId:"+DSKEXTERNALID, authorized_session.getToken())
            else:
                course_session.getCourses(authorized_session.getToken())
                course_session.createCourse("externalId:"+DSKEXTERNALID, authorized_session.getToken())
                course_session.getCourse(authorized_session.getToken())
                course_session.updateCourse("externalId:"+DSKEXTERNALID, authorized_session.getToken())

        if USER or ALL:
            user_session = User(target_url, authorized_session.getToken())
            #process user command
            print("\n[main] Run user command: " + ('ALL' if ALL else COMMAND) + '...')
            if 'user' in COMMAND:
                if (('delete' in COMMAND) or ('read' in COMMAND)):
                    print ("[main] Deleting or getting does not require a datasource.")
                else:
                    if not datasource_PK1:
                        print("[main] confirm datasource.")
                        datasource_session = DataSource(target_url, authorized_session.getToken())
                        datasource_session.checkDataSource(authorized_session.getToken())

                user_session.execute(COMMAND, "externalId:"+DSKEXTERNALID, authorized_session.getToken())
            else:
                user_session.getUsers(authorized_session.getToken())
                user_session.createUser("externalId:"+DSKEXTERNALID, authorized_session.getToken())
                user_session.getUser(authorized_session.getToken())
                user_session.updateUser("externalId:"+DSKEXTERNALID, authorized_session.getToken())

        if MEMBERSHIP or ALL:
            membership_session = Membership(target_url, authorized_session.getToken())

            #process membership command
            print("\n[main] Run membership command: " + ('ALL' if ALL else COMMAND) + '...')
            if 'membership' in COMMAND:
                if (('delete' in COMMAND) or ('read' in COMMAND)):
                    print ("[main] Deleting or getting does not require a datasource.")
                else:
                    if not datasource_PK1:
                        print("[main] confirm datasource.")
                        datasource_session = DataSource(target_url, authorized_session.getToken())
                        datasource_session.checkDataSource(authorized_session.getToken())

                membership_session.execute(COMMAND, "externalId:"+DSKEXTERNALID, authorized_session.getToken())
            else:
                membership_session.getCourseMemberships(authorized_session.getToken())
                membership_session.createMembership("externalId:"+DSKEXTERNALID, authorized_session.getToken())
                membership_session.getUserMemberships(authorized_session.getToken())
                membership_session.updateMembership("externalId:"+DSKEXTERNALID, authorized_session.getToken())
                membership_session.readUserMemberships(authorized_session.getToken())
    #clean up if not using individual commands
    if ALL:
        print('\n[main] Completing Demo and deleting created objects...')
        print ("[main] Deleting membership")
        membership_session.deleteMembership(authorized_session.getToken())
        print ("[main] Deleting Course")
        user_session.deleteUser(authorized_session.getToken())
        print ("[main] Deleting Course")
        course_session.deleteCourse(authorized_session.getToken())
        print ("[main] Deleting Term")
        term_session.deleteTerm(authorized_session.getToken())
        print ("[main] Deleting DataSource")
        datasource_session.deleteDataSource(authorized_session.getToken())
    else:
        print("\nRemember to delete created demo objects!")


    print("[main] Processing Complete")

    #revoke issued Token
    #authorized_session.revokeToken()

if __name__ == '__main__':
    main(sys.argv[1:])
