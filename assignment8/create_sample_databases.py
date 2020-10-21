import math
from disk_relations import *
from queryprocessing import *

# A simple class to keep track of the set of relations and indexes created together
class Database:
	def __init__(self, name):
		self.name = name
		self.relations = dict()
		self.indexes = dict()
	def newRelation(self, relname, rel_schema):
		self.relations[relname] = Relation(relname, rel_schema)
		return self.relations[relname]
	def getRelation(self, relname):
		return self.relations[relname]
	def newIndex(self, relname, attribute, keysize):
		return self.indexes[(relname, attribute)]
	def getIndex(self, relname, attribute):
		return self.indexes[(relname, attribute)]

def createDatabase1(name):
	## Let's first create a relation with a bunch of tuples 
 	
	db = Database(name)
	instr_schema = ["ID", "name", "dept_name", "salary"]
	instructor = db.newRelation("instructor", instr_schema)
	instructor.insertTuple(Tuple(instr_schema, ('10101', 'Srinivasan', 'Comp. Sci.', '65000')));
	instructor.insertTuple(Tuple(instr_schema, ('12121', 'Wu', 'Finance', '90000')));
	instructor.insertTuple(Tuple(instr_schema, ('15151', 'Mozart', 'Music', '40000')));
	instructor.insertTuple(Tuple(instr_schema, ('22222', 'Einstein', 'Physics', '95000')));
	instructor.insertTuple(Tuple(instr_schema, ('32343', 'El Said', 'History', '60000')));
	instructor.insertTuple(Tuple(instr_schema, ('33456', 'Gold', 'Physics', '87000')));
	instructor.insertTuple(Tuple(instr_schema, ('45565', 'Katz', 'Comp. Sci.', '75000')));
	instructor.insertTuple(Tuple(instr_schema, ('58583', 'Califieri', 'History', '62000')));
	instructor.insertTuple(Tuple(instr_schema, ('76543', 'Singh', 'Finance', '80000')));
	instructor.insertTuple(Tuple(instr_schema, ('76766', 'Crick', 'Biology', '72000')));
	instructor.insertTuple(Tuple(instr_schema, ('83821', 'Brandt', 'Comp. Sci.', '92000')));
	instructor.insertTuple(Tuple(instr_schema, ('98345', 'Kim', 'Elec. Eng.', '80000')));

	dept_schema = ["dept_name", "building", "budget"]
	department = db.newRelation("department", dept_schema)
	department.insertTuple(Tuple(dept_schema, ('Biology', 'Watson', '90000')));
	department.insertTuple(Tuple(dept_schema, ('Ca is after bio but before comp sci', 'Watson', '90000')));
	department.insertTuple(Tuple(dept_schema, ('Comp. Sci.', 'Taylor', '100000')));
	department.insertTuple(Tuple(dept_schema, ('Elec. Eng.', 'Taylor', '85000')));
	department.insertTuple(Tuple(dept_schema, ('Finance', 'Painter', '120000')));
	department.insertTuple(Tuple(dept_schema, ('History', 'Painter', '50000')));
	department.insertTuple(Tuple(dept_schema, ('Music', 'Packard', '80000')));
	department.insertTuple(Tuple(dept_schema, ('Physics', 'Watson', '70000')));

	instructor2 = db.newRelation("instructor_2", instr_schema)
	instructor2.insertTuple(Tuple(instr_schema, ('10101', 'Srinivasan', 'Comp. Sci.', '65000')));
	instructor2.insertTuple(Tuple(instr_schema, ('12121', 'Wu', 'Finance', '90000')));
	instructor2.insertTuple(Tuple(instr_schema, ('58583', 'Califieri', 'History', '62000')));
	instructor2.insertTuple(Tuple(instr_schema, ('76543', 'Singh', 'Finance', '80000')));
	instructor2.insertTuple(Tuple(instr_schema, ('76766', 'Crick', 'Biology', '72000')));
	instructor2.insertTuple(Tuple(instr_schema, ('83821', 'Brandt', 'Comp. Sci.', '92000')));
	instructor2.insertTuple(Tuple(instr_schema, ('98345', 'Kim', 'Elec. Eng.', '80000')));
	instructor2.insertTuple(Tuple(instr_schema, ('34322', 'Davis', 'Finance', '92000')));
	instructor2.insertTuple(Tuple(instr_schema, ('51769', 'Gray', 'Elec. Eng.', '80000')));

	return db
