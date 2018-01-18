import requests
import re
import time
import random
import os

departments_file = open('data/departments.txt')
departments = departments_file.readlines()
for department in departments:
    department = department[:-1]
    html_filenames = sorted(os.listdir(os.path.join('data', department)))

    courses_file = open('data/{}_courses.txt'.format(department), 'a')
    professors_file = open('data/{}_professors.txt'.format(department), 'a')
    for html_filename in html_filenames:
        i = int(html_filename[:3])
        html_file = open(os.path.join('data', department, html_filename))
        html = html_file.read()
        title = re.findall('<title>(.+?)</title>', html)
        if len(title) > 0:
            title = title[0]
            courses_file.write(title + "\n")
        else:
            print(os.path.join('data', department, html_filename))
        professors = re.findall(
            '<a href="/instructor/(?:.+?)/">(.+?)</a>',
            html)
        for professor in professors:
            professors_file.write(professor + "\n")
        # time.sleep(random.random() * 2)
    courses_file.close()
    professors_file.close()
