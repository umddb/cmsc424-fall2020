## Assignment 9: Query Processing, CMSC424, FAll 2020

*The assignment is to be done by yourself.*

### Overview

In this project, you will modify a very simple database system that we have written to illustrate some of the B+-Tree and Query Processing algorithms. 
The database system is written in Python and attempts to simulate how a database system would work, including what blocks it would read from disk, etc.

* `disk_relations.py`: This module contains the classes Block, RelationBlock, Relation, and a few others helper classes like Pointer. A Block is a base class, 
that is subclassed by RelationBlock and BTreeBlock (in `btree.py` file). A RelationBlock contains a set of tuples, and a Relation contains a list of RelationBlocks. 
* `queryprocessing.py`: This contains naive implementations of some of the query processing operators, including SequentialScan, NestedLoopsJoin, HashJoin, and SortMergeJoin. The operators are written using the iterator `get_next` interface, which is discussed in Chapter 12.7.2.1.

There are a set of parameters that control how many tuples can be stored in each RelationBlock, etc. You can't set those directly, but you can set the "blockSize" and also the size of a key, etc. Those parameters are in the class `Globals`, and can be modified to constructs trees of different fanouts.

### How to Use the Files

The directory also contains two other files:
* `create_sample_databases.py`: Creates a sample database with 2 relations and 2 indexes.
* `testing-queryprocessing.py`: Shows the execution of some simple query processing tasks using sample data. 

The simplest way you can run this is by just doing: `python3 testing-queryprocessing.py`. That will run all the code in the `testing-queryprocessing.py` file.

A better option is to do: `python3 -i testing-queryprocessing.py`. This will execute all the code in `testing-queryprocessing.py` file and then it will open a Python shell. In that shell, you can start doing more operations.

### Your Task

Your task is to finish a few of the unfinished pieces in the `btree.py` and `queryprocessing.py` files.
* (1pt) Function `HashJoin.get_next()` in `queryprocessing.py`: Your task is to implement the FULL OUTER JOIN variant of the HashJoin algorithm.
* (1pt) Functions in `GroupByAggregate` in `queryprocessing.py`: The GroupByAggregate handles 4 aggregation operators -- your task is to finish the implementation of three more: AVERAGE, MEDIAN, and MODE.
* (1pt) Function `SetIntersection.get_next()` in `queryprocessing.py`: Here you have to finish the implementation of the SetIntersection operation.

### Submission
You should submit modified `queryprocessing.py` files. We will test those in an automated fashion, using a set of test cases (on Gradescope).

Note: Make sure to handle extreme cases (e.g., no input tuples for the joins or SetIntersection, etc.)
