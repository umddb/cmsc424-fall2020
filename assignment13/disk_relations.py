import json
import os
import threading
from threading import Thread

class Globals:
        blockSize = 1200 # bytes
        stringSize = 10
        BufferPoolSize = 5

# json.loads() create unicode strings. The following makes it into standard Strings.
def byteify(input):
        if isinstance(input, dict):
                return {byteify(key):byteify(value) for key,value in input.items()}
        elif isinstance(input, list):
                return [byteify(element) for element in input]
        elif isinstance(input, str):
                return input.encode('utf-8')
        elif isinstance(input, bytes):
                return input.encode('utf-8')
        else:
                return input

# A simple Tuple class -- with the only main functionality of retrieving and setting the 
# attribute value through a brute-force search
class RelationTuple: 
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

        def setAttribute(self, attribute, value):
                for i,attr in enumerate(self.schema):
                        if attr == attribute:
                                self.t[i] = value 
                                return
                raise ValueError("Should not reach here")

class RelationBlock:
        def __init__(self, schema, diskBlockNumber):
                self.schema = schema
                self.diskBlockNumber = diskBlockNumber
        # We will only serialize out the lists with the Tuple themselves
        def toJSON(self):
                listOfTuples = [t.t for t in self.tuples]
                print("Relation Block {}".format(self.diskBlockNumber))
                print(listOfTuples)
                return json.dumps(listOfTuples).ljust(Globals.blockSize)
        def initializeFromJSON(self, js):
                self.tuples = [RelationTuple(self.schema, t) for t in json.loads(js)]
        def __str__(self):
                return self.toJSON()
        def getTuple(self, primary_id):
                for t in self.tuples:
                        if t.getAttribute('ID') == primary_id:
                                return t
                print(self)
                assert False

# A relation is characterized by two things: 
#     (1) a schema: for us this will just be a list of attribute names -- we will assume String domains 
#     (2) a list of RelationBlocks that contain the data
#     (3) A dict with the blockNumbers that contain the relation blocks on disk, with the value being the number
#         of tuples in each block 
#     (4) A very simple index that maps a tuple's primary key (the 1st attribute) to its location -- typically
#         we would use B+-trees for this purpose, but to keep things simple, we will just use a simple hash table (dict)
#         The simpleIndex will also be serialized out to the disk as JSON
#
# We will assume that each relation maps to a "text file" in the file system, whichs is sub-divided
# into chunks of size blockSize. If the provided file is empty, we will create it and initialize 
# it with some initial data
#
class Relation: 
        inMemoryRelations = dict()
        @staticmethod
        def getRelationByName(relationName):
                if relationName in Relation.inMemoryRelations:
                        return Relation.inMemoryRelations[relationName]
                else:
                        return Relation(relationName)

        def __init__(self, fileName):
                self.fileName = fileName
                Relation.inMemoryRelations[fileName] = self

                # (1) If the file already exists, we will open it, and read the first block, which contains
                # some minimal information, including an index that maps tuple primary id's (the first
                # attribute) to the block that contains it
                # (2) If the file doesn't exist, we will create it, prepopulate it with some information, 
                # write it back.
                # To keep the file consistent, we will only open it when needed and close it immediately
                if os.path.isfile(fileName):
                        dataFile = open(fileName, 'r')
                        infojson = dataFile.read(Globals.blockSize)
                        [self.schema, self.numBlocks, self.index] = json.loads(infojson)
                        #print "Read relation " + str(self.schema) + " with index: " + str(self.index) 
                        dataFile.close()
                else: 
                        self.schema = ['ID', 'A']
                        self.index = dict()
                        # Create 10 relation blocks
                        blocks = [RelationBlock(self.schema, i) for i in range(1, 11)]
                        self.numBlocks = len(blocks)
                        primary_id = 0
                        defaultA = 10
                        for b in blocks:
                                b.tuples = list()
                                for i in range(0, 10):
                                        b.tuples.append(RelationTuple(self.schema, [str(primary_id), str(defaultA)]))
                                        self.index[str(primary_id)] = b.diskBlockNumber
                                        primary_id += 1


                        # First we write the Relation Information Block -- pad it with spaces (using ljust) 
                        # to make it of size Globals.blockSize
                        infojson = json.dumps([self.schema, self.numBlocks, self.index]).ljust(Globals.blockSize)
                        assert len(infojson) <= Globals.blockSize

                        # Write out the info block, followed by the other blocks
                        dataFile = open(fileName, 'w')
                        dataFile.write(infojson)
                        for b in blocks:
                                dataFile.write(b.toJSON())
                        dataFile.close()

        def getTuple(self, primary_id):
                diskBlockNumber = self.findBlockContainingTuple(primary_id)
                be = BufferPool.getBlock(self, diskBlockNumber)
                return be.block.getTuple(primary_id)

        def findBlockContainingTuple(self, primary_id):
                #print self.index
                return int(self.index[primary_id])
        
        def readBlockIntoMemory(self, diskBlockNumber):
                dataFile = open(self.fileName, 'r')
                dataFile.seek(diskBlockNumber * Globals.blockSize)
                blockjson = dataFile.read(Globals.blockSize)
                dataFile.close()

                rblock = RelationBlock(self.schema, diskBlockNumber)
                rblock.initializeFromJSON(blockjson)
                return rblock

        def writeBlockToDisk(self, rblock):
                blockjson = rblock.toJSON()
                assert len(blockjson) <= Globals.blockSize

                dataFile = open(self.fileName, 'r+')
                dataFile.seek(rblock.diskBlockNumber * Globals.blockSize)
                dataFile.write(blockjson)
                dataFile.close()

###########################################################################################################
###########################################################################################################
###########################################################################################################
###########################################################################################################
# Buffer Pool Implementation
#
# We will do a very simple LRU implementation -- LRUOrder[0] is the next page to be evicted (if it is None,
# then we don't need to evict anything). If the page to be evicted has been changed (dirty), it is written
# back to the disk first.
#
###########################################################################################################
###########################################################################################################
###########################################################################################################
class BufferPoolEntry:
        def __init__(self):
                self.block = None
                self.pinCounter = 0

class BufferPool:
        entries = [BufferPoolEntry() for i in range(0, Globals.BufferPoolSize)]
        LRUOrder = [i for i in range(0, Globals.BufferPoolSize)]
        bufferpool_lock = threading.Lock()

        @staticmethod
        def toString():
                ret = ""
                for be in BufferPool.entries:
                        if be.block is None:
                                ret += "None, "
                        else: 
                                ret += "Block {}, ".format(be.block.diskBlockNumber)
                return ret

        # Returns the BufferPoolEntry containing the required block, fetching the block from the relation file if required
        @staticmethod
        def getBlock(relation, diskBlockNumber): 
                with BufferPool.bufferpool_lock:
                        for index, be in enumerate(BufferPool.entries):
                                if be.block is not None:
                                        if diskBlockNumber == be.block.diskBlockNumber:
                                                # Move "index" to the end of the LRUOrder
                                                BufferPool.LRUOrder.remove(index)
                                                BufferPool.LRUOrder.append(index)
                                                return be
                        # Not found -- remove the first page in LRUOrder that is not currently pinned
                        foundIndex = 0
                        for index in BufferPool.LRUOrder:
                                if BufferPool.entries[index].pinCounter == 0:
                                        foundIndex = index
                                        break
                        assert foundIndex >= 0
                        be = BufferPool.entries[foundIndex]
                        if be.block is not None:
                                relation.writeBlockToDisk(be.block)
                        be.block = relation.readBlockIntoMemory(diskBlockNumber)
                        BufferPool.LRUOrder.remove(foundIndex)
                        BufferPool.LRUOrder.append(foundIndex)
                        return be

        @staticmethod
        def writeAllToDisk(relation):
                with BufferPool.bufferpool_lock:
                        for be in BufferPool.entries:
                                if be.block is not None:
                                        relation.writeBlockToDisk(be.block)
