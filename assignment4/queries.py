queries = ["" for i in range(0, 8)]

### 0. Report the votes for the normal (i.e, not special) Senate Election in Maryland in 2018.
### Output column order: candidatename, candidatevotes
### Order by candidatename ascending
queries[0] = """
select candidatename, partyname, candidatevotes
from sen_state_returns
where year = 2018 and statecode = 'MD' and specialelections = False
order by candidatename asc;
"""

### 1. Write a query to rank the states by the number of counties, with the highest number of counties getting rank 1. 
### Use the default RANK function, not DENSERANK
###
### We have created a WITH table to help with this.
### 
### Output Columns: statecode, name, num_counties, rank
### Order by: rank, statecode
queries[1] = """
with temp as
    (select s.statecode, s.name, count(c.name) as num_counties
     from counties c, states s
     where c.statecode = s.statecode
     group by s.statecode, s.name
    )
select *
from temp;
"""

### 2. Use window functions to construct a query to associate the average population in all counties of a state 
### to the counties tables.
###
### See here: https://www.postgresql.org/docs/current/tutorial-window.html
###
### Output Column: countyname, statecode, population_2010, avg_population_2010
### Order by: countyname, statecode
queries[2] = """
select 0;
"""

### 3. Use window functions to rank the counties within each state by population in 2010, decreasing.
###
### Output Column: countyname, statecode, population_2010, rank 
### The "rank" here would be the rank within the counties for that state. 
### First 31 rows of the result look something like this.
###
### Anchorage                      | AK        |          291826 |    1
### Fairbanks North Star           | AK        |           97581 |    2
### Matanuska-Susitna              | AK        |           88995 |    3
### ..... (skipped)
### Bristol Bay                    | AK        |             997 |   27
### Skagway                        | AK        |             968 |   28
### Yakutat                        | AK        |             662 |   29
### Jefferson                      | AL        |          658466 |    1
### Mobile                         | AL        |          412992 |    2
###
### Order by: statecode, rank, countyname
queries[3] = """
select 0;
"""


### 4. Write a function that takes in a statename as input, and returns the number of counties in it.
###
### Function signature: num_counties(statename varchar, out num_counties bigint)
### 
### So calling num_counties('California') should return 58, where calling num_counties('Canada') should return 0.
### 
### Confirm that the query below works after the function is created:
###             select name, statecode, num_counties(name) from states
###
queries[4] = """
select 0;
"""

### 5. Write a function that takes in a state name and a county name and a year as input, and returns 
### a JSON with the results of the election that year.
###
### So SQL query: select presidential_winner('MD', 'Montgomery', 2008);
### should return a single tuple as:
###     { "votes": [{"name": Barack Obama, "votes": 314444}, {"name": John McCain, "votes": 118608}, {"name": Other, "votes": 6209}]}
### The order is decreasing by candidate votes. Try to conform to this structure as much as possible, but we will allow for variations.
###
### If the inputs don't match any data (e.g., say the year is 2007), then the result should be: 
###          { "votes": []}
### 
### You should use PL/pgSQL for this purpose -- writing this purely in SQL is somewhat cumbersome.
###
### Function signature: presidential_results(scode varchar, cname varchar, y integer, out results_json varchar)
###
### We have used slightly different names to avoid confusion within the function (otherwise you have to do some renaming).
### 
### You can do concatenation of strings using ||.
queries[5] = """
CREATE OR REPLACE FUNCTION presidential_winner(scode varchar, cname varchar, y integer, out results_json varchar)
AS $$
$$
LANGUAGE plpgsql;
"""

### 6. Create a new table using (this is already created in the new populate.sql file):
###         create table num_large_counties as
###             select states.statecode, states.name, count(*) as num_large_counties
###             from states join counties on (states.statecode = counties.statecode)
###             where counties.population_2010 >= 1000000
###             group by states.statecode, states.name;
###
### Create a new trigger that: 
###         When a tuple is inserted in the counties relation, appropriately modifies num_large_counties.
###         Specifically:
###             If the new counties tuple has population_2010 > 1000000, 
###                     then the count for that state should increase by 1
###                     Note that, the state may not be present in the table originally.
###
###  As per PostgreSQL syntax, you have to write two different statements -- queries[6] should be the CREATE FUNCTION statement, 
###  and queries[7] should be the CREATE TRIGGER statement.
###
###  We have provided some partial syntax.
###
### You can test using: insert into counties values('Fake', <STATECODE>, 0, 10000000), for different statecodes. 
### Keep in mind that deletes of these fake tuples will not be reflected in the num_large_counties table because
### we don't have any trigger for deletes.
###
queries[6] = """
CREATE OR REPLACE FUNCTION update_num_large_counties_on_insert()
    RETURNS TRIGGER
    LANGUAGE PLPGSQL
    AS
    $$
    $$;
"""

queries[7] = """
select 0;
"""
