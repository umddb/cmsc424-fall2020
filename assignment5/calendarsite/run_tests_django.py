import os
import sys
import datetime
from types import *
import argparse
import traceback
import json

from django.test import Client
import django

with open('/autograder/results/results.json', 'r') as f:
      results_json = json.load(f)

def add_test_result(test_no, score, max_score, output):
    results_json['tests'].append({"score": score, "max_score": max_score, "name": "Optional", "number": test_no, "output": output}) 
def write_out_results_json():
    with open('/autograder/results/results.json', 'w') as f:
        json.dump(results_json, f)

django.setup()
c = Client()

try:
    try_url = '/mycalendar/user/2/submitcreatecalendar/'

    response = c.post(try_url, {'title': 'XYZ', 'description': 'This is the XYZ Calendar', 'user_id': 2})
    print(response.content)
    print(response.status_code)
    if response.status_code == 200 and 'Alex' in response.content  and 'Work Calendar' in response.content and 'XYZ' in respnose.content:
        add_test_result("{}: {}".format(1, "Django {}".format(1)), 1, 1, "Success")
    else:
        add_test_result("{}: {}".format(1, "Django {}".format(1)), 0, 1, "Failed")
    write_out_results_json()
except:
    exception = "Runtime error"
    #exception = "Runtime error:\n {}\n {}\n {}".format(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2])
    add_test_result("{}: {}".format(1, "Django {}".format(1), 0, max_score, "Runtime Error"))
    traceback.print_exc(file=sys.stdout)
    write_out_results_json()
