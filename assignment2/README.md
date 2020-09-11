## Assignment 2: SQL Assignment - Part 1, CMSC424, Fall 2020

*The assignment is to be done by yourself.*

The following assumes you have gone through PostgreSQL instructions and have ran some queries on the `university` database. 
It also assumed you have cloned the git repository, and have done a `git pull` to download the directory `assignment2`. The files are:

1. README.md: This file
1. populate.sql: The SQL script for creating the data.
1. queries.py: The file where to enter your answer
1. SQLTesting.py: File to be used for running the queries (in `queries.py`) against the database, and generate the file to be submitted.
1. Vagrantfile: A Vagrantfile that creates the `elections` database and populates it using `populate.sql` file.

### Getting started
Start the VM with `vagrant up` in the `assignment2/` directory. The database should already be set up, but if not: 
- Create a new database called `elections` and switch to it (see the PostgreSQL setup instructions).
- Run `\i populate.sql` to create and populate the tables. 

### Schema 
The dataset contains results of `senate` and `presidential` elections for a subset of the years. For the `senate`, it contains only the statewide results from 1976 to 2018, whereas for the `presidential` elections, it contains county-level data going back to 2000.

The schema of the tables should be self-explanatory. 

The data was collected from https://electionlab.mit.edu/data.

Some things to remember: 
- The `special senate` elections are problematic. Typically senate elections take place every 6 years, with the two elections for a given state staggered. So generally speaking, any given year (say 2018), there would only be one senate election per state. However, because of special circumstances, there are
sometimes 2 elections in a given year for the same state. These two can be disambiguated based on the `specialelections` boolean flag in the database.

In many cases (especially for complex queries or queries involving 
`max` or `min`), you will find it easier to create temporary tables
using the `with` construct. This also allows you to break down the full
query and makes it easier to debug.

You don't have to use the "hints" if you don't want to; there might 
be simpler ways to solve the questions.

### Testing and submitting using SQLTesting.py
Your answers (i.e., SQL queries) should be added to the `queries.py` file. A simple query is provided for the first answer to show you how it works.
You are also provided with a Python file `SQLTesting.py` for testing your answers.

- We recommend that you use `psql` to design your queries, and then paste the queries to the `queries.py` file, and confirm it works.

- SQLTesting takes quite a few options: use `python3 SQLTesting.py -h` to see the options.

- To get started with SQLTesting, do: `python3 SQLTesting.py -v -i` -- that will run each of the queries and show you your answer.

- If you want to run your query for Question 1, use: `python3 SQLTesting.py -q 1`. 

- `-i` flag to SQLTesting will run all the queries, one at a time (waiting for you to press Enter after each query).

- **Note**: We will essentially run a modified version of `SQLTesting.py` that compares the returned answers against correct answers. So it imperative that `python3 SQLTesting.py` runs without errors.

### Submission Instructions
Submit the `queries.py` file on Gradescope under Assignment 2. 
      
### Assignment Questions
See `queries.py` file.
