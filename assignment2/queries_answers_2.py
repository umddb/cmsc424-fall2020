queries = ["" for i in range(0, 17)]

### 0. Report the votes for the normal (i.e, not special) Senate Election in Maryland in 2018.
### Output column order: candidatename, candidatevotes
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
select year, statecode, specialelections, candidatevotes
from sen_state_returns
where candidatename = 'Ben Cardin'
order by candidatevotes asc;
"""


### 2. Write a query to output the % increase, truncated to whole integer using TRUNC, in the population from 1950 to 2010.
### So for Autauga, the answer would be: 200  (54571-18186)*100/18186 = 200.7 ==> truncated to 200
### There are some counties with 0 population in 1950 -- remove those counties from the answer.
### Output columns: countyname, statecode, percentincrease
### Order output by precentincrease increasing
queries[2] = """
select name as countyname, statecode, trunc((population_2010-population_1950)*100/population_1950) as percentincrease
from counties
where population_1950 > 0
order by percentincrease asc;
"""

### 3. Write a query to output for each state how many years ago it was admitted to the union. 
### So if a state was admitted to the union in 1819, the answer would 201 (2020 - 1819). Ignore the specific dates.
### Output columns: name, admittedduration
### Order by admittedduration decreasing
queries[3] = """
select name, (2020 - extract(year from admitted_to_union)) as admittedduration
from states
order by admittedduration asc;
"""

### 4. Write a query to find the states where the increase in population from 1900 to 1950 was lower than the increase in population from 2000 to 2010.
### Output Column: name
### Order by: name increasing
queries[4] = """
select name
from states
where (population_2010 - population_2000) > (population_1950 - population_1900)
order by name asc;
"""

### 5. Write a query to find all candidates for senate who satisfy one of the following conditions:
###        - the candidate is a 'democrat' and has more than 750000 votes in Alabama.
###        - the candidate is a 'republican' and has more 1,000,000 votes in Maryland.
###        - the candidate is neither a democrat or nor a republican and has more than 500,000 votes (in any state).
### Some candidates appear under multiple party names. Ignore that for now (in other words, if a democrat has 700,000 votes in AL as a 'democrat' and
### also gets 100,000 votes as something else, that candidate should NOT be in the result
### Also: ignore any party names like 'democratic-farmer-labor' etc.
### Output columns: year, statecode, specialelections, candidatename, partyname
queries[5] = """
select year, statecode, specialelections, candidatename, partyname
from sen_state_returns
where (partyname = 'democrat' and statecode = 'AL' and candidatevotes > 750000) or 
(partyname not in ('democrat', 'republican') and candidatevotes > 500000) or 
(partyname = 'republican' and statecode = 'MD' and candidatevotes > 1000000);
"""


### 6. Write a query to join the tables states and counties to create a list of county names, county population in 2010, state name, the state
### population in 2010
### Output columns: statename, statepopulation, countyname, countypopulation
### Order first by statename, then by countyname, increasing
queries[6] = """
select s.name as statename, s.population_2010 as statepopulation, c.name as countyname, c.population_2010 as countypopulation
from states s, counties c
where s.statecode = c.statecode
order by statename, countyname asc;
"""


### 7. Write a query to join sen_state_returns and sen_elections to find the candidates that received 70% or more of the total vote.
### Output columns: year, statecode, specialelections, candidatename
### Order by percentage of total vote increasing
queries[7] = """
select s1.year, s1.statecode, s1.specialelections, s1.candidatename
from sen_state_returns s1 natural join sen_elections s2
where s1.candidatevotes/s2.totalvotes >= 0.7
order by s1.candidatevotes/s2.totalvotes;
"""


### 8. The tables were collected from 2 different sources, and there may be some consistency issues across them. 
### Write a query to find all counties (and the corresponding state names) that are present in "pres_county_returns" table, but 
### do not have any corresponding entry in the "counties"
### table (through straightforward string equality -- so 'Autauga' and 'Autauga ' (with an extra space) would NOT be considered a match.
### Each county+state combination should only appear once in the output.
### Output Columns: countyname, statename
### Order by name, statecode ascending
queries[8] = """
select distinct p.countyname as countyname, s.name as statename
from pres_county_returns p, states s
where (p.countyname, p.statecode) not in (select name, statecode from counties) and p.statecode = s.statecode;
"""


### 9. Write a query to find the maximum, minimum, and average population in 2010 across all states.
### The result will be a single row
### Truncate the avg population to a whole number using trunc
### Output Columns: max_population, min_population, avg_population
queries[9] = """
select max(population_2010) as max_population, min(population_2010) as min_population, trunc(avg(population_2010)) as avg_population
from states;
"""

### 10. Write a query to find the candidate with the maximum votes in the 2008 MI Senate Election. 
### Output Column: candidatename
queries[10] = """
select candidatename
from sen_state_returns
where statecode = 'MI' and year = 2008 and 
    candidatevotes = (select max(candidatevotes) from sen_state_returns where statecode = 'MI' and year = 2008);
"""

### 11. Write a query to find the number of candidates who received a vote for each senate election held in 2018. 
### Note that there may be two elections in some states, and there should be two tuples in the output for that state.
### 'NA' or '' (empty) should be treated as candidates. 
### Output columns: statecode, specialelections, numcandidates
queries[11] = """
select statecode, specialelections, count(*) as numcandidates
from sen_state_returns
where year = 2018
group by statecode, specialelections
"""

### 12. Write a query to find, for the 2008 elections, the number of counties where Barack Obama received more votes than John McCain.
### This will require you to do a self-join, i.e., join pres_county_returns with itself.
### Output columns: num_counties
queries[12] = """
select count(*) 
from pres_county_returns p1, pres_county_returns p2
where p1.candidatename = 'Barack Obama' and p2.candidatename = 'John McCain' and p1.year = p2. year and p1.statecode = p2.statecode and p1.countyname = p2.countyname
and p1.candidatevotes > p2.candidatevotes
"""


### 13. Write a query to find the names of the states with at least 100 counties.
### Use HAVING clause for this purpose.
### Output columns: statename, num_counties
queries[13] = """
select s.name, count(*) as num_counties
from states s, counties c
where s.statecode = c.statecode
group by s.statecode
having count(*) > 100;
"""

### 14. Write a statement to add a new column to the counties table called 'pop_trend' of type 'string'.
queries[14] = """
alter table counties add column pop_increased boolean;
"""

### 15. The values for the above added column with be empty to begin with. Write an update statement to 
### set it to 'decreased', 'increased somewhat', and 'increased a lot', depending on whether the population decreased,
### increased by less than a factor of 2 (i.e., population_2010 <= 2*population_2950), or increased by a factor of more than 2.
### Use CASE statement to make this easier.
queries[15] = """
"""


### 16. Write a statement to delete all tuples from pres_county_returns where the party is neither 'democrat' not 'republican'.
queries[16] = """
delete from pres_county_returns
where partyname not in ['democrat', 'republican'];
"""
