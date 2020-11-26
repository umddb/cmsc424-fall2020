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

class TransactionManager:
	tm_lock = threading.Lock()
	last_transaction_id = 0
	abortlist = list()

	@staticmethod
	def startTransaction():
		with TransactionManager.tm_lock:
			TransactionManager.last_transaction_id += 1
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

	def abortTransaction(self):
		print("Aborting transaction {}".format(self.transaction_id))
        ###
        ### NEED TO UNDO ALL THE CHANGES HERE FOR THIS TO BE COMPLETE -- IMPLEMENTED AS PART OF LOG MANAGER FOR NEXT ASSIGNMENT
        ###
		for [objectid, locktype] in reversed(self.locks):
			LockTable.releaseLock(self.transaction_id, objectid, locktype)

	def commitTransaction(self):
		print("Committing transaction {}".format(self.transaction_id))
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
