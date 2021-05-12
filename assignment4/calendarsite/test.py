import os
import sys
from django.test import Client
import django


def main():
    django.setup()
    c = Client()

    try_urls = ['/mycalendar/user/1/', 
                '/mycalendar/event/1/', 
                '/mycalendar/task1/11/',
                '/mycalendar/task2/Finance/',
                '/mycalendar/task3/Acme',
                '/mycalendar/task4/9/',
                '/mycalendar/task5/',
                ]


    for u in try_urls:
        try:
            print("=============== Trying {} =========".format(u))
            response = c.get(u)
            print(response.content)
        except:
            pass


if __name__ == '__main__':
    main()
