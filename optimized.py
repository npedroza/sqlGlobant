import csv
import mysql.connector
import pandas as pd
import pymysql
import sqlalchemy as sa
import time
from tabulate import tabulate

#Connect to database
db = mysql.connector.connect(
    host='host',
    user='user',
    database='db',
    passwd='123',
    port = 3306
)
##Create cursor for SQL queries
mycursor = db.cursor()
mycursor = db.cursor(buffered=True)

#Check if database is there
mycursor.execute("SELECT DATABASE()")
# Fetch the result
data = mycursor.fetchone() 
# Print the database connection
if len(data) == 0:
    print("Connection not established")
else:
    print("Connection established to database: ", data)

### NOT OPTIMAL
#### Reset tables in Database ###
##Foreign key checks set to zero so we can remove tables without
##problems of tables related between each other
mycursor.execute("SET FOREIGN_KEY_CHECKS = 0")
##Drop each table if they exist in the database
sql = "DROP TABLE IF EXISTS jobs"
mycursor.execute(sql)
sql = "DROP TABLE IF EXISTS departments"
mycursor.execute(sql)
sql = "DROP TABLE IF EXISTS employees"
mycursor.execute(sql)
#
#### Tables creation using Cursor from mysql
##Create Tables
#print("Creating tables")
#mycursor.execute("CREATE TABLE jobs (id_job INT PRIMARY KEY, job_name TEXT)")
#mycursor.execute("CREATE TABLE departments (id_dep INT PRIMARY KEY, dep_name TEXT)")
#mycursor.execute("CREATE TABLE employees (id_emp INT PRIMARY KEY, \
#                 name TEXT, date TEXT, id_dep INT, id_job INT, FOREIGN KEY (id_dep) \
#                 REFERENCES departments(id_dep), FOREIGN KEY (id_job) REFERENCES jobs(id_job))")
#
### Let's create a timer for analyzing the performance
start_time = time.time()
# Perform some time-consuming operation into table population
print("Optimum data population")
#Engine creation
engine = sa.create_engine('mysql+pymysql://user:passwd@shost:3306/user') #This needs to be modified to a set of correct credentials

csv_file_path="jobs.csv"
with open(csv_file_path, 'r') as file:
    data_df = pd.read_csv(file, header=None)
    data_df.columns = ['id_job','job_name']
data_df.to_sql('jobs',  engine, index=False, if_exists='replace')

csv_file_path="departments.csv"
with open(csv_file_path, 'r') as file:
    data_df = pd.read_csv(file, header=None)
    data_df.columns = ['id_dep','dep_name']
data_df.to_sql('departments',  engine, index=False, if_exists='replace')

csv_file_path="employees.csv"
with open(csv_file_path, 'r') as file:
    data_df = pd.read_csv(file, header=None)
    data_df.columns = ['id_emp','name', 'date', 'id_dep', 'id_job']
data_df.to_sql('employees',  engine, index=False, if_exists='replace')
elapsed_time = time.time() - start_time
print("Elapsed time:", elapsed_time, "seconds for inserting data into Tables")

mycursor.execute("SELECT dep_name,job_name, \
COUNT( CASE WHEN date >= '2021-01-01' AND date < '2021-04-01' THEN 1 END) as Q1, \
COUNT( CASE WHEN date >= '2021-04-01' AND date < '2021-07-01' THEN 1 END) as Q2, \
COUNT( CASE WHEN date >= '2021-07-01' AND date < '2021-10-01' THEN 1 END) as Q3, \
COUNT( CASE WHEN date >= '2021-10-01' AND date < '2021-12-31' THEN 1 END) as Q4 \
FROM employees \
LEFT JOIN departments ON employees.id_dep = departments.id_dep  \
LEFT JOIN jobs on jobs.id_job = employees.id_job \
WHERE  job_name IS NOT NULL AND dep_name IS NOT NULL \
GROUP BY dep_name ORDER BY dep_name asc, job_name asc")
#here i am fetching the first 10 but for all we use fetchall() 
myresult = mycursor.fetchmany(size=10) 
print(tabulate(myresult,headers=['department', 'job', 'Q1', 'Q2','Q3', 'Q4'], tablefmt='psql'))

mycursor.execute('SELECT employees.id_dep, dep_name, count(name) as hired \
FROM employees left join departments on departments.id_dep = employees.id_dep \
WHERE date like  "2021%"  and employees.id_dep is not null \
AND departments.id_dep is not null and employees.id_job is not null \
GROUP by employees.id_dep \
HAVING hired > ( \
  SELECT AVG(q) from ( \
    SELECT count(name) as q FROM employees left join departments on departments.id_dep = employees.id_dep \
    WHERE date like "2021%" and employees.id_dep is not null \
    AND departments.id_dep is not null and employees.id_job is not null  GROUP by employees.id_dep \
  ) as T1\
) \
order by hired DESC') 
myresult = mycursor.fetchmany(size=5) #fetchall()
print(tabulate(myresult,headers=['id_dep', 'dep_name', 'hired'], tablefmt='psql'))
db.close()





