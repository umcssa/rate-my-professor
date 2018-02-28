import re

input = open('insta485db-dump.txt').read()
output = open('data.sql','w')
sql = ''

tables = re.findall('FROM (.+?)\'((\n([^\S\n]*(.+?) = (.+?)\n)+)+)',
                    input)
for table in tables:
    table_name = table[0]
    insert = "INSERT INTO " + table_name + " ("
    insert_has_columns = 0
    values = "VALUES "
    rows = re.findall('(\n([^\S\n]*(.+?) = (.+?)\n)+)', table[1])
    for row in rows:
        values = values + "("
        columns = re.findall('([^\S\n]*(.+?) = (.+?)\n)', row[0])
        if not insert_has_columns:
            for column in columns:
                insert = insert + column[1] + ", "
            insert = insert[:-2] + ")"
            insert_has_columns = 1
        for column in columns:
            values = values + "'" + column[2] + "', "
        values = values[:-2] + "),\n"
    values = values[:-2] + ";\n"
    sql = sql + insert +"\n" + values + "\n"

output.write(sql)
