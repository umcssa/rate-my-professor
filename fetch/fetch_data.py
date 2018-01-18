import requests
import re
import time
import random

jar = requests.cookies.RequestsCookieJar()
jar.set('34a06e11aa9ea7a5c71e670d3e9a5a7f',
        '88465fc532e4757009de6d6d8a3fb715', domain='art.ai.umich.edu',
        path='/')
jar.set('_ga', 'GA1.2.1020928685.1516233529', domain='.umich.edu',
        path='/')
jar.set('_gat', '1', domain='.umich.edu', path='/')
jar.set('_gid', 'GA1.2.1172081647.1516233529', domain='.umich.edu',
        path='/')
jar.set('csrftoken',
        'lIpYsQBzE7wxoDppdHq2FKGh786KTS8IAwV0W0xTIj4nZCFTdXC4dYH3x8jtyJBA',
        domain='art.ai.umich.edu', path='/')
jar.set('sessionid', 'b6v34tn4hkvxojzw6bv5pospprcla1wz',
        domain='art.ai.umich.edu', path='/')

departments_file = open('data/departments.txt')
departments = departments_file.readlines()
for department in departments:
    department = department[:-1]
    courses_file = open('data/{}_courses.txt'.format(department), 'a')
    professors_file = open('data/{}_professors.txt'.format(department), 'a')
    for i in range(100, 1000):
        url = 'https://art.ai.umich.edu/course/{}%20{}/'.format(department, i)
        r = requests.get(url, cookies=jar)
        html = r.text
        title = re.findall('<title>(.+?)</title>', html)
        if len(title) > 0:
            title = title[0]
            if str(i) in title:
                courses_file.write(title + "\n")
                print(title)
                professors = re.findall(
                    '<a href="/instructor/(?:.+?)/">(.+?)</a>',
                    html)
                for professor in professors:
                    professors_file.write(professor + "\n")
                    print(professor)
        #time.sleep(random.random() * 2)
    courses_file.close()
    professors_file.close()
