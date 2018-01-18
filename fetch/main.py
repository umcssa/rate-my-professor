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

courses_file = open("courses.txt", "a")
professors_file = open("professors.txt", "a")

for i in range(100, 1000):
    url = 'https://art.ai.umich.edu/course/EECS%20{}/'.format(i)
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
    time.sleep(random.random())
