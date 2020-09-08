queries = ["" for i in range(0, 17)]

### 0. Report the votes for the normal (i.e, not special) Senate Election in Maryland in 2018.
### Output column order: candidatename, partyname, candidatevotes
### Order by candidatename ascending
queries[0] = """
select candidatename, partyname, candidatevotes
from sen_state_returns
where year = 2018 and statecode = 'MD' and specialelections = False
order by candidatename asc;
"""

### 1. Report the number of votes for candidate 'Ben Cardin' across all the senate elections.
### Output Column: year, statecode, specialelections, candidatevotes 
### Order by candidatevotes increasing
queries[1] = """
select 0;
"""


### 2. Write a query to output the % increase, truncated to whole integer using TRUNC, in the population from 1950 to 2010.
### So for Autauga, the answer would be: 200  (54571-18186)*100/18186 = 200.7 ==> truncated to 200
### There are some counties with 0 population in 1950 -- remove those counties from the answer.
### Output columns: countyname, statecode, percentincrease
### Order output by precentincrease increasing
queries[2] = """
select 0;
"""

### 3. Select all the "distinct" party names that senate candidates have been affiliated over all
### the elections. 
### Output column: partyname
### Order output by partyname ascending
queries[3] = """
select 0;
"""

### 4. Write a query to output for each state how many years ago it was admitted to the union. 
### So if a state was admitted to the union in 1819, the answer would 201 (2020 - 1819). Ignore the specific dates.
### Output columns: name, admittedduration
### Order by admittedduration decreasing
queries[4] = """
select 0;
"""

### 5. Write a query to find the states where the increase in population from 1900 to 1950 was lower than the increase in population from 2000 to 2010.
### Output Column: name
### Order by: name increasing
queries[5] = """
select 0;
"""

### 6. Write a query to find all candidates for senate who satisfy one of the following conditions:
###        - the candidate is a 'democrat' and has more than 750000 votes in Alabama.
###        - the candidate is a 'republican' and has more 1,000,000 votes in Maryland.
###        - the candidate is neither a democrat or nor a republican and has more than 500,000 votes (in any state).
### Some candidates appear under multiple party names. Ignore that for now (in other words, if a democrat has 700,000 votes in AL as a 'democrat' and
### also gets 100,000 votes as something else, that candidate should NOT be in the result
### Also: ignore any party names like 'democratic-farmer-labor' etc.
### Output columns: year, statecode, specialelections, candidatename, partyname
queries[6] = """
select 0;
"""


### 7. Write a query to join the tables states and counties to create a list of county names, county population in 2010, state name, the state
### population in 2010
### Output columns: statename, statepopulation, countyname, countypopulation
### Order first by statename, then by countyname, increasing
queries[7] = """
select 0;
"""

### 8. Write a query to join the tables states and counties to find the counties that had over
### 50% of the population of the state in 2010
### Output columns: statename, countyname 
### Order by statename, then by countyname, increasing
queries[8] = """
select 0;
"""


### 9. Write a query to join sen_state_returns and sen_elections to find the candidates that received 70% or more of the total vote.
### Output columns: year, statecode, specialelections, candidatename
### Order by percentage of total vote increasing
queries[9] = """
select 0;
"""


### 10. The tables were collected from 2 different sources, and there may be some consistency issues across them. 
### Write a query to find all counties (and the corresponding state names) that are present in "pres_county_returns" table, but 
### do not have any corresponding entry in the "counties"
### table (through straightforward string equality -- so 'Autauga' and 'Autauga ' (with an extra space) would NOT be considered a match.
### Each county+state combination should only appear once in the output.
### HINT: Use "not in".
### Output Columns: countyname, statename
### Order by countyname, statename ascending
queries[10] = """
select 0;
"""


### 11. For the 2012 presidential elections and for 'Barack Obama', write a
### query to combine pres_county_returns and counties so that, to produce a result
### with the following columns:
###     countyname, statecode, candidatevotes, population_2010
### However, for the counties in pres_county_returns that do not have a match in 
### 'counties' table, we want population_2010 to be set to NULL.
### Use a left (or right) outer join to achive this.
### Output: countyname, statecode, candidatevotes, population_2010
### Order by: countyname, statecode ascending
queries[11] = """
select 0;
"""


### 12. SQL "with" clause can be used to simplify queries. It essentially allows
### specifying temporary tables to be used during the rest of the query. See Section
### 3.8.6 (6th Edition) for some examples.
###
### Below we are providing a part of a query that uses "with" to create a
### temporary table where, for 2000 elections, we are finding the maximum of the
### candidate votes for each county. Join this temporary table with the
### 'pres_county_returns' table to find the winner for each county. 
### This is unfortunately the easiest way to do this task.
###
### You don't need to fully understand what the 'temp' query does to do the join
### -- as provided, the query shows you the result of the "temp" table
### Output columns: countyname, statecode, candidatename
### Order by: countyname, statecode
queries[12] = """
with temp as (select countyname, statecode, max(candidatevotes) as maxvotes
        from pres_county_returns
        where year = 2000
        group by countyname, statecode)
select *
from temp t;
"""


### 13. Let's create a table showing the vote differences between 2000 and 2016 for
### the democratic presidential candidates. So the result should be four columns:
###        statecode, countname2000, countyname2016,  votes2000, votes2016
### However, the list of counties is different, we want the other one to be set
### to None. We will do this through use of two temporary tables using WITH
### clause. You have to complete this query using a "full outer join" to get the 
### desired result.
###
### NOTE: Only output those tuples where both the statecodes are not NULL.
###
### Output: statecode, countname2000, countyname2016, votes2000, votes2016
### Order by: statecode, countyname2000, countyname2016 ascending
queries[13] = """
with temp1 as (select countyname, statecode, candidatevotes
               from pres_county_returns
               where partyname = 'democrat' and year = 2000),
temp2 as (select countyname, statecode, candidatevotes
          from pres_county_returns
          where partyname = 'democrat' and year = 2016)
select *
from temp1;
"""



### 14. Write a statement to add a new column to the counties table called 'pop_trend' of type 'string'.
queries[14] = """
select 0;
"""

### 15. The values for the above added column with be empty to begin with. Write an update statement to 
### set it to 'decreased', 'increased somewhat', and 'increased a lot', depending on whether the population decreased,
### increased by less than a factor of 2 (i.e., population_2010 <= 2*population_2950), or increased by a factor of more than 2.
### Use CASE statement to make this easier.
queries[15] = """
select 0;
"""


### 16. Write a statement to delete all tuples from pres_county_returns where the party is neither 'democrat' not 'republican'.
### NOTE: Keep in mind that you will need repopulate the table if you are trying to test the earlier
### queries after this delete.
queries[16] = """
select 0;
"""
