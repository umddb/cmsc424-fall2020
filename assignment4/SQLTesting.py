import psycopg2
import os
import sys
import datetime
from collections import Counter
from types import *
import argparse

from queries import *


correct_answers = []

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--interactive', help="Run queries one at a time, and wait for user to proceed", required=False, action="store_true")
parser.add_argument('-q', '--query', type = int, help="Only run the given query number", required=False)
args = parser.parse_args()

interactive = args.interactive

conn = psycopg2.connect("dbname=elections user=vagrant")
cur = conn.cursor()

for i in range(0, 8):
    # If a query is specified by -q option, only do that one
    if args.query is None or args.query == i:
        try:
            if interactive:
                os.system('clear')
            print("========== Executing Query {}".format(i))
            print(queries[i])
            cur.execute(queries[i])

            if i in [1, 2, 3]:
                ans = cur.fetchall()
                correct_answers.append(ans)

                print("--------- Your Query Answer ---------")
                for t in ans:
                    print(t)
                print("")
            else:
                if i in [4]:
                    conn.commit()
                    query_string = "select name, statecode, num_counties(name) from states order by name limit 10"
                    print("--------- Running {} -------".format(query_string))
                    cur.execute(query_string)
                    ans = cur.fetchall()
                    print("-- Result")
                    for t in ans:
                        print(t)
                    print("")
                if i in [5]:
                    conn.commit()
                    query_string = "select statecode, name, presidential_winner(statecode, name, 2008) from counties where statecode = 'MD' order by statecode limit 10"
                    print("--------- Running {} -------".format(query_string))
                    cur.execute(query_string)
                    ans = cur.fetchall()
                    print("-- Result")
                    for t in ans:
                        print(t)
                    print("")
                if i in [6]:
                    conn.commit()
                    query_string = 'SELECT n.nspname as "Schema", p.proname as "Name", pg_catalog.pg_get_function_result(p.oid) as "Result data type" FROM pg_catalog.pg_proc p LEFT JOIN pg_catalog.pg_namespace n ON n.oid = p.pronamespace WHERE p.proname = \'update_num_large_counties_on_insert\'' 
                    print("--------- Running {} -------".format(query_string))
                    cur.execute(query_string)
                    ans = cur.fetchall()
                    print("-- Result (should list the trigger function)")
                    for t in ans:
                        print(t)
                    print("")
                if i in [7]:
                    conn.commit()
                    query_string = "insert into counties values('Fake', 'MD', 0, 10000000)"
                    cur.execute(query_string)
                    conn.commit()
                    query_string = "insert into counties values('Fake', 'CA', 0, 10000000)"
                    cur.execute(query_string)
                    conn.commit()
                    query_string = "select * from num_large_counties"
                    print("--------- Running {} -------".format(query_string))
                    cur.execute(query_string)
                    ans = cur.fetchall()
                    print("-- Result (should list California with 10 and Maryland with 1)")
                    for t in ans:
                        print(t)
                    print("")
                
            if interactive:
                input('Press enter to proceed')
                os.system('clear')
        except:
            print(sys.exc_info())
            raise
