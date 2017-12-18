#!/usr/bin/python3.5

import cgitb
import cgi
import requests
import json
from lxml import html
import pymysql


print("Content-Type: text/html")
print()


cgitb.enable()

#Saves the search Url given by user to the database.
def saveToDb(finalUrl):

	conn = pymysql.connect(
    db='savedSearches',
    user='root',
    passwd='NaProjSQL',
    host='localhost')

	c = conn.cursor()

	addData = {
    'url': finalUrl,

	}
	#Deletes the last row from the database to allow only 3 saved entries.
	c.execute("DELETE FROM savedUrls order by id asc limit 1")
	#Inserts the data to the database
	c.execute ("""
        INSERT INTO savedUrls (savedUrl)
        VALUES
            (%(url)s)
        """, addData)

	conn.commit()

#Gets the desired saved Url from the html input.
def getSaveUrl():
	userSearchForm = cgi.FieldStorage()
	finalUrl = userSearchForm.getvalue('finalUrl')

	print("<script> alert("+ finalUrl+") </script>")

	
	if(finalUrl != None):
		print("<script> alert('saved') </script>")
		saveToDb(finalUrl)
#Redirects to the right page
def redirectSaved():
	redirectURL = "saved.py"
	
	print('<html>')
	print('  <head>')
	print('    <meta http-equiv="refresh" content="0;url='+str(redirectURL)+'" />') 
	print('  </head>')
	print('</html>')

getSaveUrl()

redirectSaved()

