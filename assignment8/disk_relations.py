class Globals:
	blockSize = 100
	stringSize = 10
	pointerSize = 8
	diskSizeInBlocks = 1000 # This should be a large number for our purposes
	printBlockAccesses = False

# A Block is a base class, subclassed by different types of blocks. 
class Block:
	def __init__(self, blockNumber):
		self.size = Globals.blockSize
		self.blockNumber = blockNumber

# A disk consists of a set of blocks -- we will statically allocate a large array of blocks,
# assume that we never run out of blocks
class Disk:
	blocks = [Block(i) for i in range(0, Globals.diskSizeInBlocks)]
	used = [False] * Globals.diskSizeInBlocks
	@staticmethod
	def addBlock(b):
		# Given a block b, look for an unused block and replace that with this block
		for i in range(0, len(Disk.blocks)):
			if not Disk.used[i]:
				Disk.blocks[i] = b
				Disk.used[i] = True
				b.blockNumber = i
				return b
		raise ValueError("Should not reach here")
	@staticmethod
	def releaseBlock(b): 
		Disk.used[b.blockNumber] = False


# A simple Tuple class -- with the only main functionality of retrieving the attribute
# value through a brute-force search
class Tuple: 
	def __init__(self, schema, t):
		self.t = t
		self.schema = schema
	def __str__(self):
		return str(self.t)
	def getAttribute(self, attribute):
		for i,attr in enumerate(self.schema):
			if attr == attribute:
				return self.t[i] 
		raise ValueError("Should not reach here")

# A RelationBlock simulates a disk block that contains tuples/records from a relation
# We will assume fixed-length tuples, and represent the data as a list of tuples
# To handle deletions, free lists should be maintained per block, but here we have 
# implemented a brute-force approach for simplicity
class RelationBlock(Block):
	def __init__(self, blockNumber, tuplesize):
		Block.__init__(self,blockNumber)
		maxTuples = int(self.size/tuplesize)
		self.tuples = [None] * maxTuples
	def __str__(self):
		return "Block No. {}, Type: RelationBlock: ".format(self.blockNumber) + ", ".join([str(t) for t in self.tuples])
	def getTuple(self, index):
		return self.tuples[index]
	def hasSpace(self):
		# Check if any of the tuples are set to None
		return any(i is None for i in self.tuples)
	def insertTuple(self, t):
		# We assume that this function is only called if there is space in this block
		for i in range(0, len(self.tuples)):
			if self.tuples[i] is None: 
				self.tuples[i] = t
				return Pointer(self.blockNumber, i)
		raise ValueError("Should not reach here")
	def deleteTuple(self, index):
		self.tuples[index] = None

	# The following method is to be called when we create a new index on an existing relation
	# We simply go over all the 
	def insertAllIntoIndex(self, btree, attribute):
		for i in range(0, len(self.tuples)):
			if self.tuples[i] is not None:
				btree.insert(self.tuples[i].getAttribute(attribute), Pointer(self.blockNumber, i))


# A relation is characterized by two things: 
#     (1) a schema: for us this will just be a list of attribute names -- we will assume String domains; 
#     (2) a list of RelationBlocks that contain the data
class Relation:
	def __init__(self, relname, schema):
		self.relname = relname
		self.schema = schema
		self.tuplesize = len(schema) * Globals.stringSize
		self.blocks = list()
		self.indexes = list()
	def addNewIndex(self, btree, attribute):
		self.indexes.append((btree, attribute))
		for b in self.blocks:
			b.insertAllIntoIndex(btree, attribute)
	def insertTuple(self, t):
		# Check if any of the existing blocks have space, otherwise add one
		found = False
		for b in self.blocks:
			if b.hasSpace():
				found = True
				ptr = b.insertTuple(t)
		if not found:
			n = Disk.addBlock(RelationBlock(-1, self.tuplesize))
			ptr = n.insertTuple(t)
			self.blocks.append(n)
		for (btree, attribute) in self.indexes:
			btree.insert(t.getAttribute(attribute), ptr)
	def findBlock(self, blockNumber):
		for b in self.blocks:
			if b.blockNumber == blockNumber:
				return b
	def deleteTuple(self, ptr):
		# We can't use the ptr.blockNumber directly -- we have to find that in the blocks we have
		b = self.findBlock(ptr.blockNumber)
		for (btree, attribute) in self.indexes:
			btree.delete(key = b.getTuple(ptr.index).getAttribute(attribute), ptr = ptr)
		b.deleteTuple(ptr.index)
	def printTuples(self):
		print("================================================================================")
		print("Relation {} contains {} blocks".format(self.relname, len(self.blocks)))
		for b in self.blocks:
			print(str(b))

# For simplicity, we will use a single Pointer class to maintain a pointer in the indexes
# If the pointer is pointing to a block, then the index will be "None" and will be ignored
# If the pointer is supposed to point to a specific tuple, then the index will be set accordingly
# to allow us to find the tuple in that block
class Pointer:
	def __init__(self, blockNumber, index = None):
		self.blockNumber = blockNumber
		self.index = index
	def __str__(self):
		if self.index is None:
			return "{{Block {}}}".format(self.blockNumber)
		else:
			return "{{Block {}, Tuple {}}}".format(self.blockNumber, self.index)
	def __eq__(self, other):
		return self.blockNumber == other.blockNumber and self.index == other.index
	def getBlock(self):
		if Globals.printBlockAccesses:
			print("Retrieving " + str(Disk.blocks[self.blockNumber]))
		return Disk.blocks[self.blockNumber]
	def getTuple(self):
		return self.getBlock().getTuple(self.index)

