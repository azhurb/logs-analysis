# Logs Analysis

Project for the Udacity Full Stack Web Developer Nanodegree Program.  
This reporting tool prints out reports (in plain text) based on the data in the new database, [provided](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) in the course.  
  
Reporting answers on three questions:  
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors? 

## Requirements
1. You need to have running `news` databases, provided in the course.
2. Installed python `2.7.*` or `3.*`
3. Installed PostgreSQL adapter for the Python `psycopg2`  
`pip install psycopg2`

## Example
To display report run in terminal  
`python ./report.py`  
  
Example output:
```
1. The most popular three articles of all time:
 * "Candidate is jerk, alleges rival" - 338647 views
 * "Bears love berries, alleges bear" - 253801 views
 * "Bad things gone, say good people" - 170098 views

2. The most popular article authors of all time:
 * Ursula La Multa - 507594 views
 * Rudolf von Treppenwitz - 423457 views
 * Anonymous Contributor - 170098 views
 * Markoff Chaney - 84557 views

3. Days which more than 1% of requests lead to errors:
 * Jul 17, 2016 - 2.3%
```
