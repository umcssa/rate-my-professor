import os

departments = []
for filename in os.listdir('data'):
    if 'courses' in filename:
        department_name = filename[:filename.find('_')]
        departments.append(department_name)

for filename in os.listdir('data'):
    if 'professors' in filename:
        department_name = filename[:filename.find('_')]
        department_id = departments.index(department_name) + 1
        professors_file = open(os.path.join('data', filename))
        professors = list(set(professors_file.readlines()))
        sql = "INSERT INTO professors (departmentid, name) VALUES \n"
        for professor in professors:
            sql += "(" + str(department_id) + ", '" + professor[:-1] + "'), \n"
        sql = sql[:-3]
        output = open('sql/data.sql', 'w')
        output.write(sql)
