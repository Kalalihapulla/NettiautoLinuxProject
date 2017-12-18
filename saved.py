#!/usr/bin/python3.5

import cgitb
import cgi
import requests
import json
from lxml import html
from searchresult import userSearch, scrapeData
import pymysql
import re

#Establishes the database connection to get saved searches.
conn = pymysql.connect(
    db='savedSearches',
    user='root',
    passwd='NaProjSQL',
    host='localhost')

#adds an pointer for the database to be searched.
c = conn.cursor()

#Searches the dabatase for given arguments.
c.execute("SELECT savedUrl as '' FROM savedUrls")
#assings a varible for the database data.
rows = c.fetchall()

row = rows[0][0]

row2 = rows[1][0]

row3 = rows[2][0]


#Prints the searches based on the database data.
print('''
  <!doctype html>
	<html>
  <head>

    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>Saved cars</title>
   
   <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css" integrity="sha384-PsH8R72JQ3SOdhVi3uxftmaW6Vc51MKb0q5P2rRUpPvrszuE4W1povHYgTpBfshb" crossorigin="anonymous">

<link rel="stylesheet" type="text/css" href="style.css">
</head>
<body>
	''')
	
print('''
<div class="container1">
  <a href="frontpage.html">
    <img id="fpLogo" src="http://www.theonestopcarshop.co.uk/wp-content/uploads/2016/02/car-search.png">
  </a>
   
    <div class="col1" id="col1">
    ''')
print("<h2> Saved search #1 </h2>")
scrapeData(row)

print(''' </div>

    <div class="col1" id="col2">
    ''')
print("<h2> Saved search #2 </h2>")
scrapeData(row2)

print(''' </div>
 
    <div class="col1" id="col3">
    ''')
print("<h2> Saved search #3 </h2>")
scrapeData(row3)

print(''' 
	 </div>
  </div>
	''')
print('''
  <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.3/umd/popper.min.js" integrity="sha384-vFJXuSJphROIrBnz7yo7oB41mKfc8JzQZiCq4NCceLEaO4IHwicKwpJf9c9IpFgh" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.2/js/bootstrap.min.js" integrity="sha384-alpBpkh1PFOepccYVYDB4do5UnbKysX5WZXm3XxPqe5iKTfUKjNkCk9SaVuEZflJ" crossorigin="anonymous"></script>
    ''')
print("</body>")
print("</html>")




