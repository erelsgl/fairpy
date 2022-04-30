"""
A utility program that reads a MySQL dump file and converts it to an sqlite3 database.

AUTHOR: Erel Segal-Halevi
SINCE:  2020-07-06
"""

import sqlite3, re, sys

if len(sys.argv)<2:
    print("SYNTAX: python mysql_to_sqlite.py <source>.sql")
    sys.exit(1)

source = sys.argv[1]
target = source.replace(".sql",".db")

with open(f'{source}','r') as sql_file:
    sql_text = sql_file.read()

connection = sqlite3.connect(f'{target}')
sql_text = sql_text.replace("NOT NULL AUTO_INCREMENT", "")
sql_text = re.sub(r"AUTO_INCREMENT=(\d)+", "", sql_text)
sql_text = sql_text.replace("AUTO_INCREMENT=6", "")
sql_text = sql_text.replace("ENGINE=InnoDB", "")
sql_text = sql_text.replace("DEFAULT NULL", "")
sql_text = sql_text.replace("DEFAULT CHARSET=utf8mb4", "")
sql_text = sql_text.replace("DEFAULT CHARSET=utf8s", "")
sql_text = sql_text.replace("DEFAULT CHARSET=utf8", "")
sql_text = re.sub(r"LOCK TABLES `[^`]+` WRITE;", "", sql_text)
sql_text = sql_text.replace("UNLOCK TABLES;", "")
sql_text = sql_text.replace("\\'", "")

sql_commands = sql_text.split(";")
for sql_command in sql_commands:
    connection.executescript(sql_command)

connection.close()