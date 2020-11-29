from disk_relations import *
from transactions import *
import time
from exampletransactions import *

#####################################################################################################
####
#### Some testing code
####
#####################################################################################################
# Initial Setup
bpool = BufferPool()
r = Relation('relation1')
LogManager.setAndAnalyzeLogFile('logfile')

# Start the transactions
def testingone():
	for primary_id in ["0", "10", "20", "30", "40"]:
		t = threading.Thread(target=Transaction1, args=(r, primary_id, 10))
		t.start()

def testingabort():
	t = threading.Thread(target=Transaction4, args=(r, "0", "10", 2, True))
	t.start()

def deadlockSituation():
	t = threading.Thread(target=Transaction3, args=(r, "0", "10"))
	t.start()
	t = threading.Thread(target=Transaction3, args=(r, "10", "20"))
	t.start()
	t = threading.Thread(target=Transaction3, args=(r, "20", "0"))
	t.start()

testingone()
#testingabort()
#deadlockSituation()

### Start a thread to periodically check for deadlocks
t = threading.Thread(target=LockTable.detectDeadlocks())
t.start()

### Wait for all the threads to complete
main_thread = threading.currentThread()
for t in threading.enumerate():
	if t is not main_thread:
		t.join()
BufferPool.writeAllToDisk(r)
