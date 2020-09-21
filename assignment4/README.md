# Assignment 4: SQL Part 3; Web Application Development with Python Django Part 1, CMSC424, Fall 2020

**This assignment is to be done by yourself, but you are welcome to discuss the assignment with others.**


## SQL Assignment Part 3 (2 points)

See the previous assignments for more details on the data etc. You can use the same database that you have already created -- but we recommend populating it again using the `populate.sql` file (one minor difference from the previous one).


See `queries.py` for the assignment itself. We have again provided an `SQLTesting.py` file for testing it.


## Web Application Development with Python Django Part 1 (2 points)

The goal of this assignment (and the following one) is to learn how Web Application Frameworks like Python Django (similar to Ruby-on-Rails) work, and
how they interact with the underlying data store. We will be providing you with a skeleton code, and describe a set of files that you need to modify. 

For the Part 1, the deliverable is to complete a few files as described below, and upload just those files for grading. 

In the past, students had most trouble with getting things to work, so we have provided skeleton code where all the links etc., work, except that they don't do anything in some cases. You have to implement that functionality by modifying the specified files. In all cases, there is at least one other similar file that you can use as template. 

### Getting Started
As before, we have provided with a VagrantFile, that installs Django and sets up a few port forwards. 
After logging into the virtual machine with `vagrant ssh`, go to: `/vagrant/calendarsite/` and do `python3 manage.py runserver 0.0.0.0:8888`.

This starts a webserver at port 8888, using our application code and data (that is already loaded). Go to: `http://localhost:8888/mycalendar/` for 
the main index page of the web application. See below for more details on the application.

### Introduction to Django
You can walk through the excellent Django tutorial, but you don't need to: [Django Tutorial](https://docs.djangoproject.com/en/3.0/intro/tutorial01/) -- we don't cover all of that in the description below since the tutorial does a great job at that. Django is quite popular, and there are quite a few other resources online as well. If you run into an error, searching for the error on Google should lead to some solutions (often on stackoverflow).

The initial web app that we have created is present in `calendarsite/mycalendar` subdirectory (in `/vagrant` on your VM, and `assignment4` in your host machine).
See below for more details about that app.

Django is a high-level Python Web framework for simplifying creation of complex, database-driven websites. It follows the so-called MVT (Model-View-Template) framework, which is mostly the same as the MVC (Model-View-Controller) framework (used by Ruby Rails framework). These frameworks are usually built around an Object-Relational Mapping (ORM), where the models (defined as Python classes in Django) are transparently mapped to Relations in a backend relational database. 

At a high level, the following things need to be done in order to set up a minimal web application using Django.
* We need to create a set of `models`, which roughly correspond to `entities` in E/R Modeling, and relations in relational databases. In Python code, the models serve as classes of objects, whereas the Django framework takes care of saving any such objects to the database etc. The models are defined in the file `mycalendar/models.py`. You can see the definitions of the models discussed below.
* We need to provide a mapping between URLs and `views`, so that when the web server sees a specific URL, it knows what function to call. See `mycalendar/urls.py` file for these mappings. As an example, the URL `http://localhost:8888/mycalendar/event/1` will result in a call to `eventindex` in `views.py`.
* In each of the `views`, we need to collect the appropriate data, and call a `template`. The `eventindex` view simply finds the Event (corresponding to that `id`) and calls the template `eventindex`.
* Templates tell the framework what HTML webpages to construct and return to the web browser. Our templates are in `mycalendar/templates/mycalendar` directory (the tutorial discusses why this specific directory). The `eventindex.html` template file has a mix of python commands and HTML, and it creates an HTML page after executing of the Python commands. The resulting HTML is what is returned and displayed on the browser when you call: `http://localhost:8888/mycalendar/event/1`

**python3 manage.py shell**: This is an important command that allows you to manipulate the data in the database directly (outside of the web application). The file `populate.py` contains the commands used to construct the data in the provided database.

**Database Backend**: Django can work with many database engines, including PostgreSQL (which is recommended for any serious development). Here we are using the `sqlite3` engine, primarily so we can easily provide you with the database (in the `calendarsite/db.sqlite3` file).

**Admin Website**: If you go to `http://localhost:8888/admin` with username `vagrant` and password `vagrant`, you can directly manipulate the objects.

### Application Scenario and the Initial E/R Model
The goal of this web application development project is to build an end-to-end application that has a web frontend, and a database backend.  The application scenario is that of handling an online calendar. Although there are ofcourse quite a few tools out there for this purpose today, we picked this scenario given you are well-familiar with the setting.


In the first part of the assignment (for Assignment 4), we only have two entities and relations in the applications -- `users` and `events`, with no relationships between them.
- **Users**: have a few attributes like `name`, `company`, `department`, etc.
- **Events:**  have attributes including `title`, `start_time` (including date) and `end_time`.

If you open the database using `sqlite3 calendarsite/db.sqlite3`, you can directly see the tables being created. The command `.schema` will show you all the tables that have been created.

The provided application currently has six types of URLs/views/webpages: 
- **mainindex**: Main "index" page, where we simply display a list of users, and a list of events. (example: http://localhost:8888/mycalendar/). Clicking on a user name would take us to `mycalendar/user/user_id`.
- **userindex**: User "index" page, which shows the basic information about the user. (example: http://localhost:8888/mycalendar/user/1). 
- **eventindex**: Event "index" page, which shows the details for an event. (example: http://localhost:8888/mycalendar/event/11)
- (Incomplete -- see below) **task1**: This is called with an event id as the parameters (example: http://localhost:8888/mycalendar/task1/11). For the event, it lists out the event title and the duration of the event. The template file and the view are complete, but there
is currently no entry in `urls.py` for this.
- (Incomplete -- see below) **task2**: This is called with a `department name` as the parameter (example: http://localhost:8888/mycalendar/task2/finance). For the department, it needs to list out the users in that department. The template file for this is not complete, but
the urls and view entries are complete.
- (Incomplete -- see below) **task3**: This is called with a `company name` as the parameter (example: http://localhost:8888/mycalendar/task3/acme). For the company, it needs to list out the users in that company. The template file and urls entry for this is complete, but the view is not completed.
- (Incomplete -- see below) **task4**: This is called with a `month` as the numeric parameter, i.e., between 1 and 12 (example: http://localhost:8888/mycalendar/task4/10). For the month, it needs to list out all the events for that month. The template file and urls entry for this is complete, but the view is not completed.
- (Incomplete -- see below) **task5**: This is called with no parameters (example: http://localhost:8888/mycalendar/task5). It needs to list out all events in a table format. The urls entry and the view are complete, but the templates file is not completed.

*Typically you would want to do some authorizations to separate out the different functionality. This is easy to add by having users, and using `sessions`. We will not worry about it for now. Our focus is on designing the E/R model and the schema, and understanding how to use Django.*

### Tasks (each 0.25 pts, except 0.5 for the last one)

All your modifications will be to the `views.py` file, `urls.py` file, or to one of the template files in `mycalendar/templates/mycalendar`. Specifically, the following
pieces need to be fixed. 


1. Modify `userindex.html` template file to add in the rest of the information for the user (currently it only shows the user name)
1. Modify `eventindex.html` template file to add in the end time for the event.
1. Modify `urls.py` to complete `task1`.
1. Modify `task2.html` to complete `task2`.
1. Modify `views.py` to complete `task3`.
1. Modify `views.py` to complete `task4`.
1. Modify `task5.html` to complete `task5`.


### Submission
Zip the `queries.py` file from the SQL part, and the following files together into a single zip file and upload it: `userindex.html`, `eventindex.html`, `urls.py`, `views.py`, `task2.html`, and `task5.html`.
