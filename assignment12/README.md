## Assignment 12: Transactions, CMSC424, Fall 2020

*The assignment is to be done by yourself.*

*Although we have provided a Vagrantfile as usual, you only really need python3 for this assignment.*

### Overview

In this assignment, you will modify a very simple database system that we have written to illustrate some of the transactions functionality.
The database system is written in Python and attempts to simulate how a database system would work, including what blocks it would read from disk, etc.
*The next assignment also is based on essentially the same codebase -- however, we have removed those parts of the code that are needed for this assignment.*

**NOTE**: This codebase is different from the earlier codebase, with simpler relation schema and querying interface, but a more complex Buffer Pool Manager, and File Management.
See some details below.

**Another Important Note:** We have taken a few shortcuts in this code to simplify it, which unfortunately means that there may be important synchronization failures we missed. Let me know if you see any unexpected behavior.


#### Synchronization in Python
Although you won't need to do any synchronization-related coding, it would be necessary for you to understand the basic Python synchronization primitives. The manual
explains this quite well: [https://docs.python.org/3/library/threading.html](Thread-based Parallelism in Python). Some basics:
- Each transaction for us will be started in a sepearate thread (see `testing.py` for some examples). The main command for doing so is: `threading.Thread`, which takes a function name as an argument.
- The main synchronization primitives are: `Lock` and `RLock`. You create them by calling `threading.Lock()` or `threading.RLock()`, and you use them by acquiring and releasing them. Only one thread can take a Lock or a RLock at any time.
- Two other primitives build on top of the above: `Conditions` and `Events`. See the manual for the details on those. We use `Conditions` in `transactions.py` to signal threads.
- Using `with` simplifies this: a Lock/RLock/Condition/Event is passed as an argument, and only one thread can be in the body of the `with`.

#### `disk_relations.py` 
A `Relation` is backed by a file in the file system, i.e., all the data in the relation is written to a file and is read from a file. If a Relation is created with a non-existing fileName, then a new Relation is created with pre-populated 100 tuples. The file is an ASCII file -- the reading and writing is using `json` module. 
You can open the file and see the contents of it. 

`disk_relations.py` also contains a LRU Buffer Pool Implementation, with a fixed size Buffer Pool. 

#### `transactions.py`

This contains the implementaion of the Lock Table. Some more details:
- `class LockTable`: This class implements a standard hash-based lock table. Object names are used as the identifiers for locking (so `objectid`s must be unique across all  
relations and tuples). **The code here and elsewhere implicitly assumes that there is a single relation in the database.** For each such object name, we keep track of the transations that currently have the lock (at most one in case of X locks), and a list of transactions that are waiting for a lock. 
- To avoid starvation: if T1 wants an S lock and T2 currently has one on that object, but T3 is waiting (say because it wants an X lock), we make T1 also wait, even though the locks would be compatible.
- Since we don't have an ability to interrupt a running thread (a limitation of Python), a waiting transaction wakes up periodically and checks whether it needs to be aborted. **Currently, the hasBeenAborted will never return true, since no one sets that -- your deadlock detection code needs to set that by calling singleAbortTransaction() on an appropriate transaction.**
- `class TransactionManager`: manages the currently running transactions, basically doing some bookkeeping.
- `class TransactionState`: This class encapsulates some of the basic functionality of transactions, including some helper functions to create log records, keeping track of 
what locks the transaction currently holds, etc.

#### `testing.py`

This contains some code for testing. You should be able to run: `python3 testing.py` to get started. Note that the first time you run it, it will create the
two files `relation1` and `logfile`, but after you kill it, the logfile will be inconsistent. So you should remove those two files every time while working on these two tasks.

Currently the only way to stop testing.py is through killing it through Ctrl-C. If that doesn't work, try stopping it (Ctrl-Z), and then killing it using `kill %`.

### Your Task

Your task is to finish a few of the unfinished pieces in the two files (0.5 points for the first one, and 1.5 points for the second one).
* Implementing IX Locks in `transactions.py`: Currently the code supports S, X, and IS locks. So if a transaction needs to lock a tuple in the X mode, the entire relation is locked. This is of course not ideal and we would prefer to use IX locks (on the relation) to speed up concurrency. The code for this will largely mirror the code for IS. You will have to change the `getXLockTuple()` function and also the `compatibility_list` appropriately. 
* Function `detectDeadlocksAndChooseTransactionsToAbort()` in `transactions.py`: The deadlock detection code is called once every few seconds. You should analyze the `waits-for` graph and figure out 
if there are any deadlocks and decide which transactions to abort to resolve it. This function only needs to decide which transactions to kill --  our code handles the actual abort (see `detectDeadlocks()`).

### Submission
You should submit modified `transactions.py` file to Gradescope. 

You shouldn't need to change anything in `disk_relations.py`. If you see any need for that, let us know and we can modify and commit changes to that file if we decide that is needed.
