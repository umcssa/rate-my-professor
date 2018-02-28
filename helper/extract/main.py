import codecs
import re
import requests
import json

file = codecs.open("data.txt", "r", "utf-8")
lines = file.readlines()

lines.reverse()
for i in range(len(lines)):
    if not re.match('\d', lines[i]):
        lines[i + 1] += lines[i]

for line in lines:
    items = line.split('\t')
    if len(items) >= 2 and re.findall(
            r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', items[1]):
        rate_id = items[0]
        timestamp = items[1]
        if len(items) >= 3 and re.findall(r'\w \d{3}', items[2]):
            course = items[2]
            if len(items) >= 5 and re.findall(r'(\d{4})', items[
                4]) and re.findall(
                r'([Ss]pring|[Ss]ummer|[Ff]all|[Ww]inter)',
                items[4]):
                professor = items[3]
                semester = re.findall(r'(\d{4})', items[4])[0] + ' ' + \
                           re.findall(
                               r'([Ss]pring|[Ss]ummer|[Ff]all|[Ww]inter)',
                               items[4])[0].capitalize()

                credits = 0
                if items[5] != '':
                    credits = int(items[5])

                types = []
                if len(items) >= 7 and (
                        items[6].startswith('HU') or items[
                    6].startswith('SS') or items[6].startswith(
                    'NS') or items[6].startswith('ID') or items[
                            6].startswith('RE') or items[
                            6].startswith('其他')):
                    if items[6].startswith('HU'):
                        types.append('HU')
                    if items[6].startswith('SS'):
                        types.append('SS')
                    if items[6].startswith('NS'):
                        types.append('NS')
                    if items[6].startswith('ID'):
                        types.append('ID')
                    if items[6].startswith('RE'):
                        types.append('RE')
                    if items[6].startswith('其他'):
                        types.append('Other')

                grade = items[7]

                difficulty = float(
                    items[8].split('/')[0]) / float(
                    items[8].split('/')[1])

                quality = float(
                    items[9].split('/')[0]) / float(
                    items[9].split('/')[1])

                workload = float(
                    items[10].split('/')[0]) / float(
                    items[10].split('/')[1])

                levels = ['很不推荐', '不太推荐', '比较推荐', '特别推荐']
                recommend = levels.index(items[11].strip())
                recommend = (recommend + 2) / 5 if recommend >= 2 else (recommend + 1) / 5

                suggestion = None
                if len(items) > 12 and items[12].strip() != '':
                    suggestion = items[12].strip().replace("'", "\'").replace('"', '')

                data = {'rate_id': rate_id, 'course': course, 'professor': professor, 'semester': semester,
                        'credits': credits, 'type[]': types, 'grade': grade, 'difficulty': difficulty,
                        'quality': quality, 'workload': workload, 'recommend': recommend}
                if suggestion:
                    data['suggestion'] = suggestion
                print(data)
                r = requests.post("http://localhost:8000/api/rate-my-professor/rmp-form", data=data)
                print(r.status_code, r.reason)
            else:
                print(items)
