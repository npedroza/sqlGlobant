# sqlGlobant Exercise
# Docker instructions
## Running using docker-compose (easiest way to run and interactively for visualizing the results)
 
1. Install docker on your computer
see https://docs.docker.com/

2. Clone this repository into your computer
git clone https://github.com/npedroza/sqlGlobant.git

2.1 Access the cloned repository as:
cd sqlGlobant
 
3. Build the following command `docker build -t name .`, changing the tag "name" to any desired name for the image
in my case I used t1 short for test1 (DO NOT MISS THE DOT AT THE END)
`docker build -t t1 .`

4. Run the image as (the -it option is for running interactively in your terminal):
`docker run -it t1`
The results for the SQL queries should be printed on the screen as the queries are called

5. Also you can try to pipe it to an output file like
`docker run -it t1 > output` 


#NOTES:
The script.sh file is the one that runs three versions of the code.
* test1.py works with the jobs.csv, departments.csv and the small version of employees.csv (100 rows).

* optimized.py uses the same csv files but in optimal writing to database.

* optimized\_big.py uses the same jobs and departments csv files but the full employees (2000 employees)
* Also at the end, there are two final append tests to benchmark the append timings one for 100 new users
and another for 1000 users. The timings are excellent.

## If you want to run it directly on your computer you have to install the python packages as:
`pip install -r requirements.txt`
or 
`pip3 install -r requirements.txt`

## Then you can just run the script.sh as:
`sh script.sh`

The tests can be run separately as the script.sh shows:

`python test.py`,
`python optimized.py`,
`python optimized_big.py`
