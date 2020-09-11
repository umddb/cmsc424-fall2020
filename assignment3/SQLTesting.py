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

totalscore = 0
for i in range(0, 15):
    # If a query is specified by -q option, only do that one
    if args.query is None or args.query == i:
        try:
            if interactive:
                os.system('clear')
            print("========== Executing Query {}".format(i))
            print(queries[i])
            cur.execute(queries[i])

            if i not in [13, 14]:
                ans = cur.fetchall()
                correct_answers.append(ans)

                print("--------- Your Query Answer ---------")
                for t in ans:
                    print(t)
                print("")
            else:
                if i in [13]:
                    conn.commit()
                    print("--------- Running SELECT * FROM pres_state_votes LIMIT 5 -------")
                    cur.execute("select * from pres_state_votes limit 5")
                    ans = cur.fetchall()
                    print("-- Result")
                    for t in ans:
                        print(t)
                    print("")
                else:
                    conn.commit()
                    print("--------- Listing constraints for 'counties' -------")
                    cur.execute(" SELECT conname, contype FROM pg_catalog.pg_constraint con INNER JOIN pg_catalog.pg_class rel ON rel.oid = con.conrelid INNER JOIN pg_catalog.pg_namespace nsp ON nsp.oid = connamespace WHERE rel.relname = 'counties' ")

                    ans = cur.fetchall()
                    print("-- Result should list the 4 constraints with appropriate names")
                    for t in ans:
                        print(t)
                    print("")
                
            if interactive:
                input('Press enter to proceed')
                os.system('clear')
        except:
            print(sys.exc_info())
            raise
            



