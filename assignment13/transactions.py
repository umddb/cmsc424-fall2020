from disk_relations import *
import threading
from threading import Thread
import time

#######################################################################################################
# Locking Stuff
#######################################################################################################
class LockHashTableEntry:
	def __init__(self):
		self.current_transactions_and_locks = list()
		self.waiting_transactions_and_locks = list()

# We will do locking at the level of tuples or above
class LockTable:
	# Different types of locks
	S = 0
	X = 1
	IS = 2
	IX = 3

	# Compatibility matrix
	compatibility_list = [(IS, IS), (IS, S), (S, IS), (S, S)]
	@staticmethod
	def areCompatible(ltype1, ltype2):
		return (ltype1, ltype2) in LockTable.compatibility_list
				
	# Static variables
	lockhashtable = dict()
	condition_objects = dict()
	hashtable_lock = threading.Lock()

	@staticmethod
	def getLock(transaction_id, objectid, locktype):
		# We will be using condition objects to wait -- let's acquire the condition object for this objectid first
		with LockTable.hashtable_lock:
			if objectid not in LockTable.lockhashtable:
				LockTable.lockhashtable[objectid] = LockHashTableEntry()
				LockTable.condition_objects[objectid] = threading.Condition(LockTable.hashtable_lock)
			cond = LockTable.condition_objects[objectid]

		# Since the same underlying lock is used by all condition objects, when we have acquired the condition,
		# we have also acquired the hashtable_lock
		with cond:
			while True:
				e = LockTable.lockhashtable[objectid]
				if (transaction_id, locktype) in e.waiting_transactions_and_locks:
					e.waiting_transactions_and_locks.remove( (transaction_id, locktype) )

				if not e.current_transactions_and_locks:
					print("Transaction {} able to get this lock on {}".format(transaction_id, objectid))
					e.current_transactions_and_locks.append((transaction_id, locktype))
					return True
				else:
					# If there is anyone else waiting, we will wait as well to prevent the possibility of "starvation"
					# We will do this even if we are compatible with the locks that are being held right now
					# i.e., if we are asking for a S lock, and there is currently an S lock on the object, we can acquire
					# the lock but we won't do so if there is another transaction blocked on this object
					if not e.waiting_transactions_and_locks:
						# Check if the lock we want is compatible with the locks being current held
						compatible = all(LockTable.areCompatible(locktype, ltype) for (tid, ltype) in e.current_transactions_and_locks)
						if compatible:
							print("Transaction {}: compatible so able to get this lock on {}".format(transaction_id,  objectid))
							e.current_transactions_and_locks.append((transaction_id, locktype))
							return True
						else:
							print("Transaction {}: Unable to get this lock on {}, so waiting".format(transaction_id, objectid))
							e.waiting_transactions_and_locks.append((transaction_id, locktype))
					else:
						print("Transaction {}: Someone else is waiting for a lock on {} so waiting".format(transaction_id, objectid))
						e.waiting_transactions_and_locks.append((transaction_id, locktype))

				# If the lock has not been granted, we must wait for someone to release the lock
				cond.wait(15)
				print("Transaction {}: Notified that the lock has been released, or Time Out -- checking again".format(transaction_id))

				# When the transaction is awake, there is a possibility that it needs to be aborted
				if TransactionManager.hasBeenAborted(transaction_id):
					# Remove the transaction from the waiting list
					e.waiting_transactions_and_locks.remove( (transaction_id, locktype) )
					return False

	@staticmethod
	def releaseLock(transaction_id, objectid, locktype):
		cond = LockTable.condition_objects[objectid]
		with cond: 
			print("Transaction {}: Releasing lock on {}".format(transaction_id, objectid))
			e = LockTable.lockhashtable[objectid]
			e.current_transactions_and_locks.remove((transaction_id, locktype))
			if not e.current_transactions_and_locks:
				cond.notifyAll()

	@staticmethod
	def detectDeadlocksAndChooseTransactionsToAbort():
		############################################
		####
		#### Your deadlock detection code here -- it should use the lockhashtable to check for deadlocks
		####
		#### If deadlocks are found, you should create a list of transaction_ids to abort, and return it.
		#### detectDeadlocks() will take care of calling signalAbortTransaction() -- see below
		#### 
		#### Make sure to lock the hash table (using "with" as above) before processing it
		####
		############################################

		# Return the list of transactions to be aborted (empty if none)
		return []

	@staticmethod
	def detectDeadlocks():
		while True:
			print("Running deadlock detection algorithm...")
			time.sleep(10)

			for tid in LockTable.detectDeadlocksAndChooseTransactionsToAbort():
				print("Signaling Transaction {} to abort".format(tid))
				TransactionManager.signalAbortTransaction(tid)

#######################################################################################################
# Logging Stuff
#######################################################################################################
class LogRecord:
	# What type of log record and the information within it
	START = 'START'
	COMMIT = 'COMMIT'
	ABORT = 'ABORT'
	UPDATE = 'UPDATE'
	CLR = 'CLR'
	CHECKPOINT = 'CHECKPOINT'
	def __init__(self, info):
		self.info = info

# We will simplify the implementation of logging, by writing each log record directly to the file, and closing
# the file immediately
class LogManager:
	fileName = None
	logfile_lock = threading.Lock()

	# If the log file is already present, read and analyze it to:
	# 	(1) find the last transaction id that was used so we can start from that point
	#	(2) check if recovery is needed -- if the last record is not a 
	#		CHECKPOINT record with 0 active transactions, then we need to do a recovery
	@staticmethod
	def setAndAnalyzeLogFile(fileName):
		LogManager.fileName = fileName
		if not os.path.isfile(fileName):
			return
		# logfile already exists -- analyze it
		# We don't really need synchronization here, but let's take it in just in case
		with LogManager.logfile_lock:
			f = open(LogManager.fileName, 'r')
			allrecords = [LogManager.readLogRecord(line) for line in f.readlines()]
			f.close()
		if allrecords:
			TransactionManager.last_transaction_id = max(allrecords, key=lambda lr: lr.info[0]).info[0]
			print("Setting the last_tranasction_id to be " + str(TransactionManager.last_transaction_id))

			lastrecord = allrecords[-1]
			if lastrecord.info[1] != LogRecord.CHECKPOINT or len(lastrecord.info[2]) != 0:
				LogManager.restartRecovery()

	##################################
	#
	# Complete this function -- your code should read the logrecords from the beginning, bring the system to a 
	# consistent state, write out all the # updated pages in the memory to the disk, and 
	# write out a CHECKPOINT log record (with an empty active transaction list)
	# The last step is already done for you.
	#
	##################################
	@staticmethod
	def restartRecovery():
		print("Starting Restart Recovery.......")
		#raise ValueError("Functionality to be implemented")

		# After the restart recovery is done (i.e., all the required changes redone, all the incomplete transactions
		# undone, and all the pages have been written to disk), we can now write out a CHECKPOINT record to signify
		# that the file contents are in a consistent state
		lr = LogRecord([-1, LogRecord.CHECKPOINT, list()])
		LogManager.writeLogRecord(lr)

	@staticmethod
	def writeLogRecord(lr):
		with LogManager.logfile_lock:
			w = json.dumps(lr.info) + "\n"
			f = open(LogManager.fileName, 'a')
			f.write(w)
	@staticmethod
	def readLogRecord(js):
		return LogRecord(json.loads(js))
	@staticmethod
	def createStartLogRecord(transactionid):
		lr = LogRecord([transactionid, LogRecord.START])
		LogManager.writeLogRecord(lr)
	@staticmethod
	def createCommitLogRecord(transactionid):
		lr = LogRecord([transactionid, LogRecord.COMMIT])
		LogManager.writeLogRecord(lr)
	@staticmethod
	def createAbortLogRecord(transactionid):
		lr = LogRecord([transactionid, LogRecord.ABORT])
		LogManager.writeLogRecord(lr)
	@staticmethod
	def createUpdateLogRecord(transactionid, relationName, primary_id, attrname, oldvalue, newvalue):
		lr = LogRecord([transactionid, LogRecord.UPDATE, relationName, primary_id, attrname, oldvalue, newvalue])
		LogManager.writeLogRecord(lr)

	@staticmethod
	def revertChanges(transactionid):
		# For simplicity, we will just read all the logrecords line by line and create a list of all log records
		# written by this transaction
		# We will then go backwards in that list and undo the changes, while writing CLRs
	
		# We don't really need synchronization for this, but we will go ahead and do that anyway, at least while reading the log records
		with LogManager.logfile_lock:
			f = open(LogManager.fileName, 'r')
			allrecords = [LogManager.readLogRecord(line) for line in f.readlines()]
			f.close()
		undorecords = [lr for lr in allrecords if lr.info[0] == transactionid]
		for lr in reversed(undorecords):
			if lr.info[1] == LogRecord.UPDATE:
				tup = Relation.getRelationByName(lr.info[2]).getTuple(lr.info[3])
				tup.setAttribute(lr.info[4], lr.info[5])
				clr = LogRecord([transactionid, LogRecord.CLR, lr.info[2], lr.info[3], lr.info[4], lr.info[5]])
				LogManager.writeLogRecord(clr)

#######################################################################################################
#class RecoveryManager:
	# Keeps track of Logfile
#######################################################################################################

class TransactionManager:
	tm_lock = threading.Lock()
	last_transaction_id = 0
	abortlist = list()

	@staticmethod
	def startTransaction():
		with TransactionManager.tm_lock:
			TransactionManager.last_transaction_id += 1
			LogManager.createStartLogRecord(TransactionManager.last_transaction_id)
			return TransactionManager.last_transaction_id

	@staticmethod
	def hasBeenAborted(transaction_id):
		with TransactionManager.tm_lock:
			return transaction_id in TransactionManager.abortlist

	@staticmethod
	def signalAbortTransaction(transaction_id):
		with TransactionManager.tm_lock:
			TransactionManager.abortlist.append(transaction_id)


class TransactionState:
	def __init__(self):
		self.transaction_id = TransactionManager.startTransaction()
		self.locks = list()

	# Go backwards in the lock undoing all the changes, and then release all the locks
	def abortTransaction(self):
		print("Aborting transaction {}".format(self.transaction_id))
		LogManager.revertChanges(self.transaction_id)
		LogManager.createAbortLogRecord(self.transaction_id)
		for [objectid, locktype] in reversed(self.locks):
			LockTable.releaseLock(self.transaction_id, objectid, locktype)

	# Write out the COMMIT log record, and release all the locks
	def commitTransaction(self):
		LogManager.createCommitLogRecord(self.transaction_id)
		for [objectid, locktype] in reversed(self.locks):
			LockTable.releaseLock(self.transaction_id, objectid, locktype)


	def getLock(self, objectid, locktype):
		if LockTable.getLock(self.transaction_id, objectid, locktype):
			self.locks.append([objectid, locktype])
			return True
		else:
			self.abortTransaction()
			return False

	def getXLockRelation(self, relation):
		return [relation.fileName, LockTable.X] in self.locks or self.getLock(relation.fileName, LockTable.X)

	def getSLockRelation(self, relation):
		return [relation.fileName, LockTable.S] in self.locks or self.getLock(relation.fileName, LockTable.S)

	def getXLockTuple(self, relation, primary_id):
		return [relation.fileName, LockTable.X] in self.locks or self.getLock(relation.fileName, LockTable.X)

	def getSLockTuple(self, relation, primary_id):
		if [relation.fileName, LockTable.IS] not in self.locks and [relation.fileName, LockTable.S] not in self.locks:
			return self.getLock(relation.fileName, LockTable.IS) and self.getLock(primary_id, LockTable.S)
		else:
			return self.getLock(primary_id, LockTable.S)
