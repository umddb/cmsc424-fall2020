import psycopg2
import os
import sys
import datetime
from collections import Counter
from types import *
import argparse

from queries import *

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--interactive', help="Run queries one at a time, and wait for user to proceed", required=False, action="store_true")
parser.add_argument('-q', '--query', type = int, help="Only run the given query number", required=False)
args = parser.parse_args()

interactive = args.interactive

conn = psycopg2.connect("dbname=elections user=vagrant")
cur = conn.cursor()

totalscore = 0
for i in range(0, 17):
    # If a query is specified by -q option, only do that one
    if args.query is None or args.query == i:
        try:
            if interactive:
                os.system('clear')
            print("========== Executing Query {}".format(i))
            print(queries[i])
            cur.execute(queries[i])

            if i not in [14, 15, 16]:
                ans = cur.fetchall()

                print("--------- Your Query Answer ---------")
                for t in ans:
                    print(t)
                print("")
            else:
                if i in [14, 15]:
                    conn.commit()
                    print("--------- Running SELECT * FROM Counties LIMIT 5 -------")
                    cur.execute("select * from counties limit 5")
                    ans = cur.fetchall()
                    print("-- Result")
                    for t in ans:
                        print(t)
                    print("")
                else:
                    conn.commit()
                    print("--------- Running SELECT count(*) FROM pres_county_returns where partyname not in ('democrat', 'republican') -------")
                    cur.execute("select count(*) from pres_county_returns where partyname not in ('democrat', 'republican')")
                    ans = cur.fetchall()
                    print("-- Result (should be 0)")
                    for t in ans:
                        print(t)
                    print("")
                
            if interactive:
                input('Press enter to proceed')
                os.system('clear')
        except:
            print(sys.exc_info())
            raise
