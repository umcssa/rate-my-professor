professors_file = open('professors.txt')
professors = list(set(professors_file.readlines()))
sql = "INSERT INTO professors (name) VALUES \n"
for professor in professors:
    sql += "('" + professor[:-1] + "'), \n"
sql = sql[:-3]
output = open('data.sql', 'w')
output.write(sql)
