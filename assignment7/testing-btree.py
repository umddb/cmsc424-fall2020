import math
from disk_relations import *
from btree import *
from create_sample_databases import *
import sys

# Create a sample database
db1 = createDatabase1("univ")
db1.getRelation("instructor").printTuples()
db1.getRelation("department").printTuples()
db1.getIndex("instructor", "name").printTree()
#db1.getIndex("instructor", "dept_name").printTree()

# Let's do a search -- we will print out the Blocks that were accessed during the search
# by setting Globals.printBlockAccesses
def searchExample():
	print("================================================================================")
	print("Searching for all instructors with names starting with M to R")
	Globals.printBlockAccesses = True
	results = db1.getIndex("instructor", "name").searchByRange("M", "S")
	if results is not None and len(results) != 0:
		print("Results: " + " ".join([str(ptr.getTuple()) for ptr in results]))
	else:
		print("No results found")
	Globals.printBlockAccesses = False

# Find a record by key and delete the first tuple in the results -- print out the resulting trees
def deleteFromTree(deleteKey):
	print("================================================================================")
	print("Deleting the entry for key " + deleteKey)
	index = db1.getIndex("instructor", "name")
	results = index.searchByKey(deleteKey)
	db1.getRelation("instructor").deleteTuple(results[0])
	# The BTrees should have been adjusted automatically
	index.printTree()
	#db1.getIndex("instructor", "dept_name").printTree()


# Example of a search can be found in searchExample() above
searchExample()

if False:
	# A delete that works
	deleteFromTree("Crick")
	db1.getIndex("instructor", "name").printTree()
	deleteFromTree("Califieri")
	db1.getIndex("instructor", "name").printTree()
else:
	# A delete that doesn't work because of missing functionality
	deleteFromTree("Mozart")
	db1.getIndex("instructor", "name").printTree()
	deleteFromTree("Einstein")
	db1.getIndex("instructor", "name").printTree()

