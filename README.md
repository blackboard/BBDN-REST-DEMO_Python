# BBDN-REST_DEMO-Python
This project contains sample code for demonstrating the Blackboard Learn REST APIs in Python.
This sample code was built with Python 3.9.1.

### Project at a glance:
- Target: Blackboard Learn SaaS Release 2015.11.0-ci.23+a9a4758 minimum
- Source Release: v2.0
- Release Date  2020-12-22
- Author: shurrey
- Tested on Blackboard Learn SaaS Release 3900.2.0-rel.34+4ad580a
- Source Release: v1.0
- Release Date  2016-02-24
- Author: moneil
- Tested on Blackboard Learn SaaS Release 2015.11.0-ci.23+a9a4758

### Requirements:
- Python  3.9.1
- Developer account - register at https://developer.blackboard.com
- Test instance


### Setting Up Your Development Environment
#### Python development tools
You will first need to install Python 3.9.1. You can use tools like brew or ports to install on Mac, Powershell and the Marketplace on Windows, or run the installation manually.

You may also install Python tools for your IDE or use a text editor and terminal to run the python code.


### Included Files
restdemo.py - this is the main script<br/>
auth.py - this script contains the code for authenticating the application and managing tokens<br/>
datasouce.py - this script contains examples for each of the REST endpoints for managing Data Sources in Learn<br/>
term.py - this script contains examples for each of the REST endpoints for managing Terms in Learn<br/>
course.py - this script contains examples for each of the REST endpoints for managing Courses in Learn<br/>
user.py - this script contains examples for each of the REST endpoints for managing Users in Learn<br/>
membership.py - this script contains examples for each of the REST endpoints for managing Memberships in Learn Courses


### What it does
The rest demo script demonstrates authenticating a REST application, management and use of the authorization token, and creating, updating, discovering, and deleting supported Learn objects.

<i><b>NOTE:</b> Before running the example code you must register a developer account and application as described on the Developer Community <a href="https://docs.blackboard.com/learn/REST/Getting%20Started%20With%20REST.html">Getting Started with REST</a> and <a href="https://docs.blackboard.com/learn/REST/Managing%20REST%20Integrations%20in%20Learn.html">Managing REST Integrations in Learn: The REST Integrations Tool for System Administrators</a> pages. You must also configure the script as outlined in the below Configure the Script section.</i>

When run with only a target URL the script will in the following order
1. Authenticate<br/>
2. Create, Read, and Update a Data Source<br/>
3. Create, Read, and Update a Term<br/>
4. Create, Read, and Update a Course<br/>
5. Create, Read, and Update a User<br/>
6. Create, Read, and Update a Membership<br/>
7. Delete created objects in reverse order of create - membership, user, course, term, datasource.

When run with a specific command on an object only that operation will be run - you are responsible for system cleanup.

All generated output is sent to the terminal (or IDE output window).

e.g.:
```
$ python restdemo.py -h
  restdemo.py -t|--target <target root URL> -c|--command <command>
  e.g.:$ restdemo.py -t www.myschool.edu -c create_course
         command: <command>_<object> where <command> is one of the following:
           create, read, update, delete
         and &lt;object&gt; is one of the following:
           datasource, term, course, user, membership
         -t is required; No -c args will run demo in predetermined order.
         -c commands require a valid datasource PK1 -
	    a datasource get will be run in these cases, defaulting to create
	    if the demo datasource does not exist.
```

For example:
```
$ python restdemo.py -t localhost:9877
```
<i>Runs the full CRUD demo</i>

```
$ python restdemo.py -t localhost:9877 -c create_datasource
```
<i>Runs the datasource.py:createDataSource() demo code and does not clean up the remote system after running you must run: </i>

```
$ python restdemo.py -t localhost:9877 -c delete_datasource
```
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
For a thorough walkthrough of this code, visit the corresponding Blackboard Developer Community documentation <a href="https://docs.blackboard.com/learn/rest/examples/python-demo">REST Demo Using Python</a>.
