# gudlift-registration

## Why

 This is a proof of concept (POC) project to show a light-weight version of our competition booking platform. The aim is the keep things as light as possible, and use feedback from the users to iterate.

## Getting Started

This project uses the following technologies:

* Python v3.10

* [Flask](https://flask.palletsprojects.com/en/2.3.x/)

    Whereas Django does a lot of things for us out of the box, Flask allows us to add only what we need. 

* [Virtual environment](https://virtualenv.pypa.io/en/stable/installation.html)

    This ensures you'll be able to install the correct packages without 
 interfering with Python on your machine.

Before you begin, please ensure you have this installed globally. 


## Installation

- After cloning, change into the directory and type <code>virtualenv .</code>. This will then set up a virtual python environment within that directory.

- Next, type <code>source bin/activate</code>. You should see that your 
  command prompt has changed to the name of the folder. This means that you can install packages in here without affecting files outside. To deactivate, type <code>deactivate</code>.

- Rather than hunting around for the packages you need, you can install in one step. 
  - Type <code>pip install -r requirements/production.
    txt</code>.  This will install all the packages listed in the 
    respective file. If you install a package, make sure others know by 
    updating the requirements/production.txt file. An easy way to do this is 
    <code>pip freeze > requirements/production.txt</code>
  - Requirements for developer use such as tests or CI are in a separate 
    requirement file named requirements/development.txt. Type <code>pip 
    install -r requirements/development.txt</code> to install the packages.
    This also installs the production requirements.

- Flask requires that you set an environmental variable to the python 
  file. However you do that, you'll want to set the file to be 
  <code>server.py</code>. Check [here](https://flask.palletsprojects.com/en/1.1.x/quickstart/#a-minimal-application) for more details.

- You should now be ready to test the application. In the directory, 
  type either <code>flask run</code> or <code>python -m flask run</code>.
  The app should respond with an address you should be able to go to using your browser.

## Current Setup

The app is powered by [JSON files](https://www.tutorialspoint.com/json/json_quick_guide.htm). This is to get around having a DB until we actually need one. The main ones are:
  
* competitions.json - list of competitions
* clubs.json - list of clubs with relevant information. You can look here to see what email addresses the app will accept for login.

## Testing

### Testing framework

We are using pytest. With your virtual environment activated, type "pytest" 
to launch the existing tests.

### Test coverage

We also like to show how well we're testing, so there's a module called 
[coverage](https://coverage.readthedocs.io/en/7.2.6/) we are using in 
this project. 

Type the following to launch the coverage report creation:

``coverage run -m pytest``

To display the report in the console, type:

``coverage report -m`` or ``coverage html``

### Performance tests

We use Locust to test performance. Launch the tool in the command line:

``locust -f app/tests/performance_tests/locustfile.py``

In your browser, access ``localhost:8089`` then fill out the amount of users 
you wish to pretend are accessing your site, then ``http://127.0.0.1:5000`` 
for example for your local Flask application, and start swarming. 


