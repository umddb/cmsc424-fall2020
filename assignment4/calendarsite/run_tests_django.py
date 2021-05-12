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

try_urls = ['/mycalendar/user/6/', 
            '/mycalendar/event/44/', 
            '/mycalendar/task1/55/',
            '/mycalendar/task2/DevOps/',
            '/mycalendar/task3/Stark/',
            '/mycalendar/task4/4/',
            '/mycalendar/task5/',
            ]


regex_checks = [
        ['DevOps', 'Stark'],
        ['2021', '19'],
        ['SpecialMeeting'],
        ['Scarlett', 'Adam'],
        ['Scarlett', 'Adam'],
        ['AprilMeeting1', 'AprilMeeting2', 'AprilMeeting3'],
        ['table', 'AprilMeeting1', 'AprilMeeting2', 'AprilMeeting3', 'Event name', 'Event start time', 'Event end time']
        ]

for i in range(0, 7):
    max_score = 0.5 if i == 6 else 0.25
    try:
        u = try_urls[i]
        print("=============== Trying {} =========".format(u))
        response = c.get(u)
        print(response.content)
        print(response.status_code)

        passed = (response.status_code == 200) and all([r in str(response.content) for r in regex_checks[i]])

        if passed:
            print("Passed Successfully")
            add_test_result("{}: {}".format((i+1), "Django {}".format(i+1)), max_score, max_score, "Success")
        else:
            print("Failed")
            add_test_result("{}: {}".format((i+1), "Django {}".format(i+1)), 0, max_score, "Failed")
        write_out_results_json()
    except:
        exception = "Runtime error"
        #exception = "Runtime error:\n {}\n {}\n {}".format(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2])
        add_test_result("{}: {}".format((i+1), "Django {}".format(i+1)), 0, max_score, "Runtime Error")
        traceback.print_exc(file=sys.stdout)
        write_out_results_json()
