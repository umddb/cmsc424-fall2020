import math
from disk_relations import *
from queryprocessing import *
from create_sample_databases import *
import sys

# Create a sample database
db1 = createDatabase1("univ")
db1.getRelation("instructor").printTuples()
db1.getRelation("department").printTuples()

# Set up some simple operators manually: Nested Loops Join
def query1():
	scan1 = SequentialScan(db1.getRelation("instructor"))
	scan2 = SequentialScan(db1.getRelation("department"))
	nl_join = NestedLoopsJoin(scan2, scan1, "dept_name", "dept_name")
	print("==================== Executing Nested Loops Join ================")
	nl_join.init()
	for t in nl_join.get_next():
		print("---> " + str(t))

# Set up some simple operators manually: Nested Loops Join
def query1a():
	scan1 = SequentialScan(db1.getRelation("department"))
	scan2 = SequentialScan(db1.getRelation("instructor"), Predicate("salary", "80000"))
	nl_join = NestedLoopsJoin(scan1, scan2, "dept_name", "dept_name", NestedLoopsJoin.LEFT_OUTER_JOIN)
	print("==================== Executing Nested Loops Left Outer Join ================")
	nl_join.init()
	for t in nl_join.get_next():
		print("---> " + str(t))

# Set up some simple operators manually: Aggregate
def query2():
	scan1 = SequentialScan(db1.getRelation("instructor"))
	aggr = GroupByAggregate(scan1, "salary", GroupByAggregate.SUM)
	print("==================== Executing An Aggregate Query ================")
	aggr.init()
	for t in aggr.get_next():
		print("---> " + str(t))

# Set up some simple operators manually: Inner Hash Join
def query3():
	scan1 = SequentialScan(db1.getRelation("instructor"))
	scan2 = SequentialScan(db1.getRelation("department"))
	hash_join = HashJoin(scan1, scan2, "dept_name", "dept_name", HashJoin.INNER_JOIN)
	print("==================== Executing An Inner Hash Join ================")
	hash_join.init()
	for t in hash_join.get_next():
		print("---> " + str(t))

# Trying to execute a sort merge join
def query4():
	scan1 = SequentialScan(db1.getRelation("instructor"))
	scan2 = SequentialScan(db1.getRelation("department"))
	sm_join = SortMergeJoin(scan1, scan2, "dept_name", "dept_name")
	print("==================== Executing Sort Merge Join ================")
	sm_join.init()
	for t in sm_join.get_next():
		print("---> " + str(t))

# Trying to execute a group by aggregate
def query5():
	scan1 = SequentialScan(db1.getRelation("instructor"))
	aggr = GroupByAggregate(scan1, "salary", GroupByAggregate.SUM, "dept_name")
	print("==================== Executing A Groupby Aggregate Query ================")
	aggr.init()
	for t in aggr.get_next():
		print("---> " + str(t))

# The following operators work
#query1()
#query1a()
#query2()
#query3()
query4()
#query5()

# Full Outer Hash Join
def query6():
	scan1 = SequentialScan(db1.getRelation("instructor"))
	scan2 = SequentialScan(db1.getRelation("department"))
	hash_join = HashJoin(scan1, scan2, "dept_name", "dept_name", HashJoin.FULL_OUTER_JOIN)
	print("==================== Executing Full Outer Hash Join ================")
	hash_join.init()
	for t in hash_join.get_next():
		print("---> " + str(t))


# Trying to execute a group by aggregate
def query7a():
	scan1 = SequentialScan(db1.getRelation("instructor"))
	aggr = GroupByAggregate(scan1, "salary", GroupByAggregate.AVERAGE, "dept_name")
	print("==================== Executing A Groupby Aggregate Query ================")
	aggr.init()
	for t in aggr.get_next():
		print("---> " + str(t))

def query7b():
	scan1 = SequentialScan(db1.getRelation("instructor"))
	aggr = GroupByAggregate(scan1, "salary", GroupByAggregate.MEDIAN, "dept_name")
	print("==================== Executing A Groupby Aggregate Query ================")
	aggr.init()
	for t in aggr.get_next():
		print("---> " + str(t))

def query7c():
	scan1 = SequentialScan(db1.getRelation("instructor"))
	aggr = GroupByAggregate(scan1, "salary", GroupByAggregate.MODE, "dept_name")
	print("==================== Executing A Groupby Aggregate Query ================")
	aggr.init()
	for t in aggr.get_next():
		print("---> " + str(t))

def query8b():
	scan1 = SequentialScan(db1.getRelation("instructor"))
	scan2 = SequentialScan(db1.getRelation("instructor_2"))
	sm = SetIntersection(scan1, scan2, keep_duplicates = False)
	print("==================== Executing A Set Intersection Operation ================")
	sm.init()
	for t in sm.get_next():
		print("---> " + str(t))

#query8b()
