import os
import re

departments = []
sql = ""
for filename in os.listdir('data'):
    if 'courses' in filename:
        department_name = filename[:filename.find('_')]
        departments.append(department_name)

for filename in os.listdir('data'):
    department_name = filename[:filename.find('_')]
    department_id = departments.index(department_name) + 1
    read_file = open(os.path.join('data', filename))
    if 'professors' in filename:
        professors = list(set(read_file.readlines()))
        sql += "\nINSERT INTO professors (departmentid, name) VALUES \n"
        for professor in professors:
            sql += "(" + str(department_id) + ", '" + professor[:-1] + "'), \n"
        sql = sql[:-3] + ";\n"

    elif 'courses' in filename:
        courses = read_file.readlines()
        sql += "\nINSERT INTO courses (departmentid, number, title) VALUES \n"
        for course in courses:
            result = re.findall('^\w+ (\d{3}): (.+)$', course)[0]
            number = result[0]
            title = result[1]
            sql += "(" + str(department_id) + ", " + number + ", '" + title + "'), \n"
        sql = sql[:-3] + ";\n"

output = open('sql/data.sql', 'w')
output.write(sql)
