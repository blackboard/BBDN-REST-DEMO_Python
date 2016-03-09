# BBDN-REST_DEMO-Python
This project contains sample code for demonstrating the Blackboard Learn REST APIs in Python.
This sample code was built with Python 2.7.10.

###Project at a glance:
- Target: Blackboard Learn SaaS Release 2015.11.0-ci.23+a9a4758 minimum
- Source Release: v1.0
- Release Date  2016-02-24
- Author: moneil
- Tested on Blackboard Learn SaaS Release 2015.11.0-ci.23+a9a4758

###Requirements:
- Python  2.7.10
- Developer account - register at https://developer.blackboard.com
- Test instance


### Setting Up Your Development Environment
#### Python development tools
You will first need to install Python 2.7.10. You can use tools like brew or ports to install, or run the installation manually.

You may also install Python tools for your IDE or use a text editor and terminal to run the python code.


### Included Files
restdemo.py - this is the main script
auth.py - this script contains the code for authenticating the application and managing tokens
datasouce.py - this script contains examples for each of the REST endpoints for managing Data Sources in Learn
term.py - this script contains examples for each of the REST endpoints for managing Terms in Learn
course.py - this script contains examples for each of the REST endpoints for managing Courses in Learn
user.py - this script contains examples for each of the REST endpoints for managing Users in Learn
membership.py - this script contains examples for each of the REST endpoints for managing Memberships in Learn Courses


### What it does
The rest demo script demonstrates authenticating a REST application, management and use of the authorization token, and creating, updating, discovering, and deleting supported Learn objects.

<i><b>NOTE:</b> Before running the example code you must register a developer account and application as described on the Developer Community <a href="https://community.blackboard.com/docs/DOC-1579">What is the Developer Portal: Developer Registration and Application Management</a> and <a href="https://community.blackboard.com/docs/DOC-1580">Managing REST Integrations in Learn: The REST Integrations Tool for System Administrators</a> pages. You must also configure the script as outlined in the below Configure the Script section.</i>

When run with only a target URL the script will in the following order
Authenticate<br/>
Create, Read, and Update a Data Source<br/>
Create, Read, and Update a Term<br/>
Create, Read, and Update a Course<br/>
Create, Read, and Update a User<br/>
Create, Read, and Update a Membership<br/>
Delete created objects in reverse order of create - membership, user, course, term, datasource.

When run with a specific command on an object only that operation will be run - you are responsible for system cleanup.

All generated output is sent to the terminal (or IDE output window).

e.g.:
<pre>
$ python restdemo.py -h

restdemo.py -t|--target <target root URL> -c|--command <command><br/>
e.g. restdemo.py -t www.myschool.edu -c create_course<br/>
command: <command>_<object> where <command> is one of the following:<br/>
	create, read, read_all, update, delete<br/>
and <object> is one of the following:<br/>
	datasource, term, course, user, membership<br/>
-t is required; No -c args will run demo in predetermined order.<br/>
</pre>

<pre>
$ python restdemo.py -t localhost:9877
</pre>
<i>Runs the full CRUD demo</i>

<pre>
$ python restdemo.py -t localhost:9877 -c create_datasource
</pre>
<i>Runs the datasource.py:createDataSource() demo code and does not clean up the remote system after running you must run: </i>

<pre>
    $ python restdemo.py -t localhost:9877 -c delete_datasource
</pre>
<i>to remove the created data source.</i>
<br/><br/>

## Running the Demo!
### Setup Your Test Server
To run the demo if you have not already done so you must as outlined above register the application via the Developer Portal and add the application to your test environment using the REST API Integration tool.


### Configuring the Script
Before executing the script to run against your test server you must configure it with your registered application's Key and Secret.

Open auth.py and edit lines 37 and 38.
On line 37 replace "insert_your_application_key_here" with the key issued when you registered your application.<br/>
On line 38 replace "insert_your_application_secret_here" with the secret issued when you registered your application.

Once you have setup your test server and changed auth.py to reflect your application's key and secret you may run the command line tools as outlined above or via your IDE.


### Conclusion
For a thorough walkthrough of this code, visit the corresponding Blackboard Developer Community <a href="<need a url">REST Demo Using Python</a>.
