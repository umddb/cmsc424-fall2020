queries = ["" for i in range(0, 15)]

### 0. Report the votes for the normal (i.e, not special) Senate Election in Maryland in 2018.
### Output column order: candidatename, candidatevotes
### Order by candidatename ascending
queries[0] = """
select candidatename, partyname, candidatevotes
from sen_state_returns
where year = 2018 and statecode = 'MD' and specialelections = False
order by candidatename asc;
"""

### 1. Write a query to find the maximum, minimum, and average population in 2010 across all states.
### The result will be a single row.
### Truncate the avg population to a whole number using trunc
### Output Columns: max_population, min_population, avg_population
queries[1] = """
select max(population_2010) as max_population, min(population_2010) as min_population, trunc(avg(population_2010)) as avg_population
from states;
"""

### 2. Write a query to find the candidate with the maximum votes in the 2008 MI Senate Election. 
### Output Column: candidatename
### Order by: candidatename
queries[2] = """
select candidatename
from sen_state_returns
where statecode = 'MI' and year = 2008 and 
    candidatevotes = (select max(candidatevotes) from sen_state_returns where statecode = 'MI' and year = 2008)
order by candidatename;
"""

### 3. Write a query to find the number of candidates who are listed in the sen_state_returns table for each senate election held in 2018. 
### Note that there may be two elections in some states, and there should be two tuples in the output for that state.
### 'NA' or '' (empty) should be treated as candidates. 
### Output columns: statecode, specialelections, numcandidates
### Order by: statecode, specialelections
queries[3] = """
select statecode, specialelections, count(*) as numcandidates
from sen_state_returns
where year = 2018
group by statecode, specialelections
order by statecode, specialelections
"""

### 4. Write a query to find, for the 2008 elections, the number of counties where Barack Obama received strictly more votes 
### than John McCain.
### This will require you to do a self-join, i.e., join pres_county_returns with itself.
### Output columns: num_counties
queries[4] = """
select count(*) as num_counties
from pres_county_returns p1, pres_county_returns p2
where p1.candidatename = 'Barack Obama' and p2.candidatename = 'John McCain' and p1.year = p2.year and p1.statecode = p2.statecode and p1.countyname = p2.countyname
and p1.candidatevotes > p2.candidatevotes and p1.year = 2008
"""


### 5. Write a query to find the names of the states with at least 100 counties in the 'counties' table.
### Use HAVING clause for this purpose.
### Output columns: statename, num_counties
### Order by: statename
queries[5] = """
select s.name as statename, count(*) as num_counties
from states s, counties c
where s.statecode = c.statecode
group by s.statecode, s.name
having count(*) >= 100
order by statename;
"""

### 6. Write a query to construct a table:
###     (statecode, total_votes_2008, total_votes_2012)
### to count the total number of votes by state for Barack Obama in the two elections.
###
### Use the ability to "sum" an expression (e.g., the following query returns the number of counties in 'AR')
### select sum(case when statecode = 'AR' then 1 else 0 end) from counties;
###
### Order by: statecode
queries[6] = """
select statecode, sum(case when year = 2008 then candidatevotes else 0 end) as total_votes_2008, 
       sum(case when year = 2012 then candidatevotes else 0 end) as total_votes_2012
from pres_county_returns
where candidatename = 'Barack Obama' 
group by statecode
order by statecode;
"""

### 7. Create a table to list the disparity between the populations listed in 'states' table and those listed in 'counties' table for 1950 and 2010.
### Result should be: 
###        (statename, disparity_1950, disparity_2010)
### So disparity_1950 = state population 1950 - sum of population_1950 for the counties in that state
### Use HAVING to only output those states where there is some disparity (i.e., where at least one of the two is non-zero)
### Order by statename
queries[7] = """
select s.name as statename, s.population_1950 - sum(c.population_1950) as disparity_1950, s.population_2010 - sum(c.population_2010) as disparity_2010
from states s, counties c
where s.statecode = c.statecode
group by s.name, s.population_1950, s.population_2010
having s.population_2010 != sum(c.population_2010) or s.population_1950 != sum(c.population_1950)
order by s.name
"""

### 8. Use 'EXISTS' or 'NOT EXISTS' to find the states where no counties have population in 2010 above 500000 (500 thousand).
### Output columns: statename
### Order by statename
queries[8] = """
select s.name as statename
from states s
where not exists (select * from counties c where c.statecode = s.statecode and c.population_2010 > 500000)
order by statename;
"""

### 9. List all counties and their basic information that have a unique name across all states. 
### Use scalar subqueries to simplify the query.
### Output columns: all attributes of counties (name, statecode, population_1950, population_2010)
### Order by name, statecode
queries[9] = """
select * 
from counties c
where 1 = (select count(*) from counties c2 where c2.name = c.name)
order by name, statecode;
"""

### 10. Use Set Intersection to find the counties that Barack Obama lost in 2008, but won in 2012.
### We have created a temporary table using WITH that you can use (or not).
###
### Output columns: countyname, statecode
### Order by countyname, statecode
queries[10] = """
with temp1 as (select countyname, statecode, year, max(candidatevotes) as maxvotes
        from pres_county_returns 
        group by countyname, statecode, year
        ),
     temp2 as (
             select p.countyname, p.statecode, p.year, p.candidatevotes = t.maxvotes as won
             from pres_county_returns p, temp1 t
             where p.countyname = t.countyname and p.statecode = t.statecode and p.year = t.year and p.candidatename = 'Barack Obama'
)
select countyname, statecode from temp2 where year = 2012 and won = True
intersect
select countyname, statecode from temp2 where year = 2008 and won = False
order by countyname, statecode;
"""


### 11. Find all presidential candidates listed in pres_county_returns who did NOT run for elections as a senator.
### HINT: Use "except" to simplify the query
###
### Every candidate should be reported only once. You will see incorrect answers in there because "names" don't match -- that's fine.
###
### Output columns: candidatename
### Order by: candidatename
queries[11] = """
select distinct candidatename
from pres_county_returns
except
select distinct candidatename
from sen_state_returns
order by candidatename
"""



### 12. Create a table listing the months and the number of states that were admitted to the union (admitted_to_union field) in that month.
### Use 'extract' for operating on dates, and the ability to create a small inline table in SQL. For example, try:
###         select * from (values(1, 'Jan'), (2, 'Feb')) as x;
###
### Output columns: month_no, monthname, num_states_admitted
### month should take values: Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec
### Order by: month_no
queries[12] = """
select month_no, monthname, count(*) as num_states_admitted
from states, (values (1, 'Jan'), (2, 'Feb'), (3, 'Mar'), (4, 'Apr'), (5, 'May'), (6, 'Jun'), (7, 'Jul'), (8, 'Aug'), (9, 'Sep'), (10, 'Oct'), (11, 'Nov'), (12, 'Dec')) as months(month_no, monthname)
where extract(month from admitted_to_union) = month_no
group by month_no, monthname
order by month_no;
"""


### 13. Create a view pres_state_votes with schema (year, statecode, candidatename, partyname, candidatevotes) where we maintain aggregated counts by statecode (i.e.,
### candidatevotes in this view would be the total votes for each state, including states with statecode 'NA').
queries[13] = """
create view pres_state_votes as 
select year, statecode, candidatename, partyname, sum(candidatevotes) as candidatevotes
from pres_county_returns
group by year, statecode, candidatename, partyname;
"""

### 14. Use a single ALTER TABLE statement to add (name, statecode) as primary key to counties, and to add CHECKs that neither of the two populations are less than zero.
### Name the two CHECK constraints nonzero2010 and nonzero1950.
queries[14] = """
ALTER TABLE counties ADD CONSTRAINT pk PRIMARY KEY (name, statecode), 
      ADD CONSTRAINT nonzero2010 CHECK (population_2010 >= 0),
      ADD CONSTRAINT nonzero1950 CHECK (population_1950 >= 0);
"""

