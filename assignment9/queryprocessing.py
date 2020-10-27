from disk_relations import *

# We will implement our operators using the iterator interface
# discussed in Section 12.7.2.1
class Operator:
	def init(self):
		return
	def get_next(self):
		return
	def close(self):
		return

# We will only support equality predicate for now
# This class denotes a predicate, e.g. "a = 5" (attribute will be a, and value will be 5), 
# and it supports a single method: "satisfiedBy"
class Predicate:
	def __init__(self, attribute, value):
		self.attribute = attribute
		self.value = value
	def satisfiedBy(self, t):
		return t.getAttribute(self.attribute) == self.value

# The simplest operator is SequentialScan, whose get_next() simply returns all the tuples one by one
class SequentialScan(Operator):
	def __init__(self, relation, predicate = None):
		self.relation = relation
		self.predicate = predicate

	# Typically the init() here would open the appropriate file, etc. In our 
	# simple implementation, we don't need to do anything, especially when we
	# use "yield"
	def init(self):
		return

	# This is really simplified because of "yield", which allows us to return a value, 
	# and then continue where we left off when the next call comes
	def get_next(self):
		for i in range(0, len(self.relation.blocks)):
			b = self.relation.blocks[i]
			if Globals.printBlockAccesses:
				print("Retrieving " + str(b))
			for j in range(0, len(self.relation.blocks[i].tuples)):
				t = b.tuples[j]
				if t is not None and (self.predicate is None or self.predicate.satisfiedBy(t)):
					yield t

	# Typically you would close any open files etc.
	def close(self):
		return

# Next we implement the Nested Loops Join, which has two other operators as inputs: left_child and right_child
# We will only support Equality joins and Left Outer Joins -- Right Outer Joins are tricky to do using NestedLoops
class NestedLoopsJoin(Operator):
	INNER_JOIN = 0
	LEFT_OUTER_JOIN = 1
	def __init__(self, left_child, right_child, left_attribute, right_attribute, jointype = INNER_JOIN):
		self.left_child = left_child
		self.right_child = right_child
		self.left_attribute = left_attribute
		self.right_attribute = right_attribute
		self.jointype = jointype

	# Call init() on the two children
	def init(self):
		self.left_child.init()
		self.right_child.init()

	# Again using "yield" greatly simplifies writing of this code -- otherwise we would have 
	# to keep track of current pointers etc
	def get_next(self):
		for l in self.left_child.get_next():
			foundAMatch = False
			for r in self.right_child.get_next():
				if l.getAttribute(self.left_attribute) == r.getAttribute(self.right_attribute):
					foundAMatch = True
					output = list(l.t)
					output.extend(list(r.t))
					yield Tuple(None, output)
			# If we are doing LEFT_OUTER_JOIN, we need to output a tuple if there is no match
			if self.jointype == NestedLoopsJoin.LEFT_OUTER_JOIN and not foundAMatch:
				output = list(l.t)
				for i in range(0, len(self.right_child.relation.schema)):
					output.append("NULL")
				yield Tuple(None, output)
			# NOTE: RIGHT_OUTER_JOIN is not easy to do with NestedLoopsJoin, so you would swap the children
			# if you wanted to do that

	# Typically you would close any open files etc.
	def close(self):
		return

# We will only support Equality joins
# Inner Hash Joins are very simple to implement, especially if you assume that the right relation fits in memory
# We start by loading the tuples from the right input into a hash table, and then for each tuple in the second
# input (left input) we look up matches
class HashJoin(Operator):
	INNER_JOIN = 0
	FULL_OUTER_JOIN = 1
	def __init__(self, left_child, right_child, left_attribute, right_attribute, jointype):
		self.left_child = left_child
		self.right_child = right_child
		self.left_attribute = left_attribute
		self.right_attribute = right_attribute
		self.jointype = jointype

	# Call init() on the two children
	def init(self):
		self.left_child.init()
		self.right_child.init()

	# We will use Python "dict" data structure as the hash table
	def get_next(self):
		if self.jointype == self.INNER_JOIN:
			# First, we load up all the tuples from the right input into the hash table
			hashtable = dict()
			for r in self.right_child.get_next():
				key = r.getAttribute(self.right_attribute)
				if key in hashtable:
					hashtable[r.getAttribute(self.right_attribute)].append(r)
				else: 
					hashtable[r.getAttribute(self.right_attribute)] = [r]
			# Then, for each tuple in the left input, we look for matches and output those
			# Using "yield" significantly simplifies this code
			for l in self.left_child.get_next():
				key = l.getAttribute(self.left_attribute)
				if key in hashtable:
					for r in hashtable[key]:
						output = list(l.t)
						output.extend(list(r.t))
						yield Tuple(None, output)

		elif self.jointype == self.FULL_OUTER_JOIN:
			raise ValueError("Functionality to be implemented")
		else:
			raise ValueError("This should not happen")

	# Typically you would close any open files, deallocate hash tables etc.
	def close(self):
		self.left_child.close()
		self.right_child.close()
		return

class GroupByAggregate(Operator):
	COUNT = 0
	SUM = 1
	MAX = 2
	MIN = 3
	AVERAGE = 4
	MEDIAN = 5
	MODE = 6

	@staticmethod
	def initial_value(aggregate_function):
		initial_values = [0, 0, None, None, None, None, None]
		return initial_values[aggregate_function]

	@staticmethod
	def update_aggregate(aggregate_function, current_aggregate, new_value):
		if aggregate_function == GroupByAggregate.COUNT:
			return current_aggregate + 1
		elif aggregate_function == GroupByAggregate.SUM:
			return current_aggregate + int(new_value)
		elif aggregate_function == GroupByAggregate.MAX:
			if current_aggregate is None:
				return new_value
			else:
				return max(current_aggregate, new_value)
		elif aggregate_function == GroupByAggregate.MIN:
			if current_aggregate is None:
				return new_value
			else:
				return min(current_aggregate, new_value)
		elif aggregate_function == GroupByAggregate.AVERAGE:
			raise ValueError("Functionality to be implemented")
		elif aggregate_function == GroupByAggregate.MEDIAN:
			raise ValueError("Functionality to be implemented")
		elif aggregate_function == GroupByAggregate.MODE:
			raise ValueError("Functionality to be implemented")
		else:
			raise ValueError("No such aggregate")

	# Do any final computation that needs to be done 
	# For COUNT, SUM, MIN, MAX, we can just return what we have been computing
	# For the other three, we need to do something more
	@staticmethod
	def final_aggregate(aggregate_function, current_aggregate):
		if aggregate_function in [GroupByAggregate.COUNT, GroupByAggregate.SUM, GroupByAggregate.MIN, GroupByAggregate.MAX]:
			return current_aggregate 
		elif aggregate_function == GroupByAggregate.AVERAGE:
			raise ValueError("Functionality to be implemented")
		elif aggregate_function == GroupByAggregate.MEDIAN:
			raise ValueError("Functionality to be implemented")
		elif aggregate_function == GroupByAggregate.MODE:
			raise ValueError("Functionality to be implemented")
		else:
			raise ValueError("No such aggregate")


	def __init__(self, child, aggregate_attribute, aggregate_function, group_by_attribute = None):
		self.child = child
		self.group_by_attribute = group_by_attribute
		self.aggregate_attribute = aggregate_attribute
		# The following should be between 0 and 3, as interpreted above
		self.aggregate_function = aggregate_function

	def init(self):
		self.child.init()

	def get_next(self):
		if self.group_by_attribute is None:
			# We first use initial_value() to set up an appropriate initial value for the aggregate, e.g., 0 for COUNT and SUM
			aggr = GroupByAggregate.initial_value(self.aggregate_function)

			# Then, for each input tuple: we update the aggregate appropriately
			for t in self.child.get_next():
				aggr = GroupByAggregate.update_aggregate(self.aggregate_function, aggr, t.getAttribute(self.aggregate_attribute))

			# There is only one output here, but we must use "yield" since the "else" code needs to use "yield" (that code
			# may return multiple groups)
			yield Tuple(None, (GroupByAggregate.final_aggregate(self.aggregate_function, aggr)))
		else:
			# for each different value "v" of the group by attribute, we should return a 2-tuple "(v, aggr_value)",
			# where aggr_value is the value of the aggregate for the group of tuples corresponding to "v"
			
			# we will set up a 'dict' to keep track of all the groups
			aggrs = dict()

			for t in self.child.get_next():
				g_attr = t.getAttribute(self.group_by_attribute)

				# initialize if not already present in aggrs dictionary
				if g_attr not in aggrs:
					aggrs[g_attr] = GroupByAggregate.initial_value(self.aggregate_function)

				aggrs[g_attr] = GroupByAggregate.update_aggregate(self.aggregate_function, aggrs[g_attr], t.getAttribute(self.aggregate_attribute))

			# now that the aggregate is compute, return oen by one
			for g_attr in aggrs:
				yield Tuple(None, (g_attr, GroupByAggregate.final_aggregate(self.aggregate_function, aggrs[g_attr])))


class SortMergeJoin(Operator):
	INNER_JOIN = 0

	def __init__(self, left_child, right_child, left_attribute, right_attribute, jointype = INNER_JOIN):
		self.left_child = left_child
		self.right_child = right_child
		self.left_attribute = left_attribute
		self.right_attribute = right_attribute
		self.jointype = jointype

	# Call init() on the two children
	def init(self):
		self.left_child.init()
		self.right_child.init()

	# We assume that the two inputs are small enough to fit into memory, so there is no need to do external sort
	# We will load the two relations into arrays and use Python sort routines to sort them, and then merge, using 'yield' to simplify the code
	def get_next(self):
		left_input = [r for r in self.left_child.get_next()]
		right_input = [r for r in self.right_child.get_next()]

		left_input.sort(key=lambda t: t.getAttribute(self.left_attribute))
		right_input.sort(key=lambda t: t.getAttribute(self.right_attribute))

		if self.jointype == self.INNER_JOIN:
			ptr_l = 0
			ptr_r = 0

			while ptr_l < len(left_input) and ptr_r < len(right_input):
				set_L = [left_input[ptr_l]]
				l_attr = left_input[ptr_l].getAttribute(self.left_attribute) 

				ptr_l += 1
				while ptr_l < len(left_input):
					if left_input[ptr_l].getAttribute(self.left_attribute) == l_attr:
						set_L.append(left_input[ptr_l])
						ptr_l += 1
					else:
						break

				while ptr_r < len(right_input) and right_input[ptr_r].getAttribute(self.right_attribute) <= l_attr:
					if right_input[ptr_r].getAttribute(self.right_attribute) == l_attr:
						for l in set_L:
							output = list(l.t)
							output.extend(list(right_input[ptr_r].t))
							yield Tuple(None, output)
					ptr_r += 1

		else:
			raise ValueError("This should not happen")

	# Typically you would close any open files, deallocate hash tables etc.
	def close(self):
		self.left_child.close()
		self.right_child.close()

# You have to implement the Set INTERSECTION operator 
# The input is two relations with identical schema, and the output is: left_child INTERSECT right_child
# By default, SQL INTERSECTION removes duplicates -- our implementation may or may not remove duplicates based on the flag 'keep_duplicates' -- you have to implement both
# Easiest way to implement this operator is through using a Hash Table, similarly to the Hash Join above
class SetIntersection(Operator):
	def __init__(self, left_child, right_child, keep_duplicates = False):
		self.left_child = left_child
		self.right_child = right_child
		self.keep_duplicates = keep_duplicates

	# Call init() on the two children
	def init(self):
		self.left_child.init()
		self.right_child.init()

	# As above, use 'yield' to simplify writing this code
	def get_next(self):
		raise ValueError("Functionality to be implemented")
		
	# Typically you would close any open files etc.
	def close(self):
		return
