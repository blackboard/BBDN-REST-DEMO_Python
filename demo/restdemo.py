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

import sys
import getopt



def main(argv):
    target_url = ''
    COMMAND = ''
    ALL = False
    DATASOURCE = False
    TERM = False
    COURSE = False
    USER = False
    MEMBERSHIP = False
    CLEANUP = False

    datasource_PK1 = None

    usageStr = "\nrestdemo.py -t|--target <target root URL> -c|--command <command>\n"
    usageStr += "e.g restdemo.py -t www.myschool.edu -c create_course\n"
    usageStr += "command: <command>_<object> where <command> is one of the following:\n"
    usageStr += "\tcreate, read, read_all, update, delete\n"
    usageStr += "and <object> is one of the following:\n"
    usageStr += "\tdatasource, term, course, user, membership\n"
    usageStr += "-t is required; No -c args will run demo in predetermined order.\n"
    usageStr += "-c commands require a valid datasource PK1 - \n"
    usageStr += "\ta datasource get will be run in these cases, defaulting to create\n"
    usageStr += "\tif the demo datasource does not exist."

    if len(sys.argv) > 1: #there are command line arguments
        try:
            opts, args = getopt.getopt(argv,"ht:c:",["target=","command="])
        except getopt.GetoptError:
            print usageStr
            sys.exit(2)
        for opt, arg in opts:
            if opt == '-h':
                print usageStr
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
        print '[main] Target is:', target_url
        print '[main] Command is:', COMMAND


    else:
        print(usageStr)
        sys.exit(2)


    #Set up some booleans for processing flags and order of processing
    if "course" in COMMAND:
        print("[main] Run course command")
        COURSE = True
    elif "user" in COMMAND:
        print("[main] Run user command")
        USER = True
    elif "membership" in COMMAND:
        print("[main] Run membership command")
        MEMBERSHIP = True
    elif "term" in COMMAND:
        print("[main] Run term command")
        TERM = True
    elif "datasource" in COMMAND:
        print("[main] Run datasource command")
        DATASOURCE = True
    else:
        print("[main] Empty Command: Run All\n")
        ALL = True

    print ('\n[main] Acquiring auth token...\n')
    authenticated_session = AuthToken(target_url)
    authenticated_session.setToken()
    print ('\n[main] Returned token: ' + authenticated_session.getToken() + '\n')

    #run commands in required order if running ALL
    if DATASOURCE or ALL:
        #process Datasource command
        print("\n[main] Run datasource command: " + ('ALL' if ALL else COMMAND) + '...')
        datasource_session = DataSource(target_url, authenticated_session.getToken())
        if 'datasource' in COMMAND:
            datasource_session.execute(COMMAND, authenticated_session.getToken())
        else:
            #datasource_session.getDataSources(authenticated_session.getToken())
            datasource_session.createDataSource(authenticated_session.getToken())
            datasource_PK1 = datasource_session.datasource_PK1
            print("[main] datasource_PK1: " + datasource_PK1)
            datasource_session.getDataSource(authenticated_session.getToken())
            datasource_session.updateDataSource(authenticated_session.getToken())


    if TERM or ALL:
        term_session = Term(target_url, authenticated_session.getToken())
        #process term command
        print("\n[main] Run term command: " + ('ALL' if ALL else COMMAND) + '...')
        if 'term' in COMMAND:
            if (('delete' in COMMAND) or ('read' in COMMAND)):
                print ("[main] Deleting or getting does not require a datasource.")
            else:
                print("[main] datasource_PK1:  not known... searching...")
                datasource_session = DataSource(target_url, authenticated_session.getToken())
                datasource_session.getDataSource(authenticated_session.getToken())
                datasource_PK1 = datasource_session.datasource_PK1
                print("[main] datasource_PK1: " + datasource_PK1)
                if (datasource_PK1 is None):
                    print ("[main] data source not found, creating for demo...")
                    datasource_session.createDataSource(authenticated_session.getToken())
                    datasource_PK1 = datasource_session.datasource_PK1

            term_session.execute(COMMAND, datasource_PK1, authenticated_session.getToken())
        else:
            #term_session.getTerms(authenticated_session.getToken())
            term_session.createTerm(datasource_PK1, authenticated_session.getToken())
            term_session.getTerm(authenticated_session.getToken())
            term_session.updateTerm(datasource_PK1, authenticated_session.getToken())

    if COURSE or ALL:
        course_session = Course(target_url, authenticated_session.getToken())
        #process course command
        print("\n[main] Run course command: " + ('ALL' if ALL else COMMAND) + '...')
        if 'course' in COMMAND:
            if (('delete' in COMMAND) or ('read' in COMMAND)):
                print ("[main] Deleting or getting does not require a datasource.")
            else:
                print("[main] datasource_PK1:  not known... searching...")
                datasource_session = DataSource(target_url, authenticated_session.getToken())
                datasource_session.getDataSource(authenticated_session.getToken())
                datasource_PK1 = datasource_session.datasource_PK1
                print("[main] datasource_PK1: " + datasource_PK1)
                if (datasource_PK1 is None):
                    print ("[main] data source not found, creating for demo...")
                    datasource_session.createDataSource(authenticated_session.getToken())
                    datasource_PK1 = datasource_session.datasource_PK1
            course_session.execute(COMMAND, datasource_PK1, authenticated_session.getToken())
        else:
            #course_session.getCourses(authenticated_session.getToken())
            course_session.createCourse(datasource_PK1, authenticated_session.getToken())
            course_session.getCourse(authenticated_session.getToken())
            course_session.updateCourse(datasource_PK1, authenticated_session.getToken())

    if USER or ALL:
        user_session = User(target_url, authenticated_session.getToken())
        #process user command
        print("\n[main] Run user command: " + ('ALL' if ALL else COMMAND) + '...')
        if 'user' in COMMAND:
            if (('delete' in COMMAND) or ('read' in COMMAND)):
                print ("[main] Deleting or getting does not require a datasource.")
            else:
                print("[main] datasource_PK1:  not known... searching...")
                datasource_session = DataSource(target_url, authenticated_session.getToken())
                datasource_session.getDataSource(authenticated_session.getToken())
                datasource_PK1 = datasource_session.datasource_PK1
                print("[main] datasource_PK1: " + datasource_PK1)
                if (datasource_PK1 is None):
                    print ("[main] data source not found, creating for demo...")
                    datasource_session.createDataSource(authenticated_session.getToken())
                    datasource_PK1 = datasource_session.datasource_PK1
            user_session.execute(COMMAND, datasource_PK1, authenticated_session.getToken())
        else:
            #user_session.getUsers(authenticated_session.getToken())
            user_session.createUser(datasource_PK1, authenticated_session.getToken())
            user_session.getUser(authenticated_session.getToken())
            user_session.updateUser(datasource_PK1, authenticated_session.getToken())

    if MEMBERSHIP or ALL:
        membership_session = Membership(target_url, authenticated_session.getToken())

        #process membership command
        print("\n[main] Run membership command: " + ('ALL' if ALL else COMMAND) + '...')
        if 'membership' in COMMAND:
            if (('delete' in COMMAND) or ('read' in COMMAND)):
                print ("[main] Deleting or getting does not require a datasource.")
            else:
                print("[main] datasource_PK1:  not known... searching...")
                datasource_session = DataSource(target_url, authenticated_session.getToken())
                datasource_session.getDataSource(authenticated_session.getToken())
                datasource_PK1 = datasource_session.datasource_PK1
                print("[main] datasource_PK1: " + datasource_PK1)
                if (datasource_PK1 is None):
                    print ("[main] data source not found, creating for demo...")
                    datasource_session.createDataSource(authenticated_session.getToken())
                    datasource_PK1 = datasource_session.datasource_PK1
            membership_session.execute(COMMAND, datasource_PK1, authenticated_session.getToken())
        else:
            #membership_session.getMemberships(authenticated_session.getToken())
            membership_session.createMembership(datasource_PK1, authenticated_session.getToken())
            membership_session.getMembership(authenticated_session.getToken())
            membership_session.updateMembership(datasource_PK1, authenticated_session.getToken())

    #clean up if not using individual commands
    if ALL:
        print('\n[main] Completing Demo and deleting created objects...')
        print "[main] Deleting membership"
        membership_session.deleteMembership(authenticated_session.getToken())
        print "[main] Deleting Course"
        user_session.deleteUser(authenticated_session.getToken())
        print "[main] Deleting Course"
        course_session.deleteCourse(authenticated_session.getToken())
        print "[main] Deleting Term"
        term_session.deleteTerm(authenticated_session.getToken())
        print "[main] Deleting DataSource"
        datasource_session.deleteDataSource(authenticated_session.getToken())
    else:
        print("Remember to delete created demo objects!")


    print("[main] Processing Complete")

    #revoke issued Token
    #authenticated_session.revokeToken()

if __name__ == '__main__':
    main(sys.argv[1:])
