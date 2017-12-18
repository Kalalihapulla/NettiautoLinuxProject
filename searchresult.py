#!/usr/bin/python3.5

import cgitb
import cgi
import requests
import json
from lxml import html
import pymysql
import re

#Enables CGI to print contet to the web page.
cgitb.enable()

print("Content-Type: text/html")
print()

#Manipulates the data taken from a html form on frontpage.html
#Uses cgi.fieldstorage to get the data.
#The Url that is used to search for cars at www.Nettiauto.com is formed from user inputs.

def userSearch():

	userSearchForm = cgi.FieldStorage()
	carBrand = userSearchForm.getvalue('carBrand')
	carBrandList = userSearchForm.getvalue('carBrandList') 
	setBrand = ""

	if (carBrandList == None and carBrand == None):
		setBrand = ""

	elif carBrand == None:
		setBrand= carBrandList + "/"
	
	else:
		setBrand = carBrand + "/"


	carModel = userSearchForm.getvalue('carModel')
	carModelList = userSearchForm.getvalue('carModelList')
	setModel = ""

	if (carModelList == None and carModel == None):
		setModel = ""

	elif carModel == None:
		setModel = carModelList + "/"
	
	else:
		setModel = carModel + "/"

	priceFrom = userSearchForm.getvalue('priceFrom')
	priceTo = userSearchForm.getvalue('priceTo')
	vehicleType = userSearchForm.getvalue('vehicleType')
	chassisType = userSearchForm.getvalue('chassisType')
	fuelType = userSearchForm.getvalue('fuelType')
	gearType = userSearchForm.getvalue('gearType')
	yearFrom = userSearchForm.getvalue('yearFrom')
	yearTo = userSearchForm.getvalue('yearTo')
	engineFrom = userSearchForm.getvalue('engineFrom')
	engineTo = userSearchForm.getvalue('engineTo')
	mileageFrom = userSearchForm.getvalue('mileageFrom')
	mileageTo = userSearchForm.getvalue('mileageTo')
	roadPermit = userSearchForm.getvalue('roadPermit')

	if roadPermit != "N":
		roadPermit = "Y"

	airCon = userSearchForm.getvalue('airCon')
	cruiseControl = userSearchForm.getvalue('cruiseControl')
	towBar = userSearchForm.getvalue('towBar')
	allWheelDrive = userSearchForm.getvalue('4wd')


	varlist = [vehicleType, chassisType, fuelType, gearType, priceFrom, priceTo, yearFrom, yearTo, engineFrom, engineTo, mileageFrom, mileageTo, roadPermit, airCon, cruiseControl, towBar, allWheelDrive]
	
	#The values that are not given in the search form are marked as empty, so they wont affect the search.
	for i, item in enumerate(varlist):
		if item == None:
			varlist[i] = ""

	#The final url used to form the search is formed from the parts.		
	finalUrl =  'https://www.nettiauto.com/' + setBrand + setModel +'vaihtoautot?id_vehicle_type='
	 + varlist[0] + '&id_car_type=' + varlist[1] + '&id_fuel_type=' + varlist[2] + 
	 '&id_gear_type=' + varlist[3] + '&pfrom=' + varlist[4] + '&pto=' + varlist[5] + 
	 '&yfrom=' + varlist[6] + '&yto=' + varlist[7] + '&engineFrom=' + varlist[8] + '&engineTo=' 
	 + varlist[9] + '&mileageFrom=' + varlist[10] + '&mileageTo=' + varlist[11] + '&road_permit=' 
	 + varlist[12] + '&id_acc_air=' + varlist[13] + '&id_acc_cruise_control=' + varlist[14] + 
	 '&id_acc_tow_bar=' + varlist[15] + '&id_four_wheel=' + varlist[16] +
	  '&show_search=1&sortCol=enrolldate&ord=DESC&page=1&'
	
	
	print("<br>")
	print("<br>")


	#The final url is returned for scraping.
	return finalUrl


def scrapeData(url):

	#Gets the page content from the search Url given as parameter using requests python package.
	page = requests.get(url)

	#Parses the html from the page.
	tree = html.fromstring(page.content)

	count = 3

	#Scrapes the needed car data using xpaths. Formats the output to wanted form and prints it to the web page.
	while count < 34:

		print("<div class='carCont'>")
		carLink = str(tree.xpath("//*[@id='listingData']/div[" + str(count) + "]/a/@href[1]"))[2:-18]
		#print(carLink)

		carName = str(tree.xpath("//*[@id='listingData']/div[" + str(count) + 
		"]/div/div[2]/div[1]/text()"))[2:-2]
		print("<h3>")
		print("<a href='" + carLink + "'>" + carName + "</a>" ) 
		print("</h3>")

		carImage = str(tree.xpath("//*[@id='listingData']/div[" + str(count) + 
		"]/div/div[1]/div[2]/div/a[1]/@alt"))[2:-2]
		print("<a href='" + carLink + "'>")
		print("<img class='carImage' src=" + carImage+
		" alt='https://www.cstatic-images.com/stock/900x600/274720.jpg'>")
		print("</a>")

	
		carEngSize = str(tree.xpath("//*[@id='listingData']/div[" + str(count) + 
		"]/div/div[2]/div[1]/span/text()"))[2:-2]
		print(carEngSize)


		carMileage = str(tree.xpath("//*[@id='listingData']/div[" + str(count) + 
		"]/div/div[2]/div[2]/div[2]/div[2]/ul/li[2]/text()"))[2:-2]
		print(carMileage + " |")

		carFuelType = str(tree.xpath("//*[@id='listingData']/div[" + str(count) + 
		"]/div/div[2]/div[2]/div[2]/div[2]/ul/li[3]/text()"))[2:-2]
		print(carFuelType + " |")

		carTransType = str(tree.xpath("//*[@id='listingData']/div[" + str(count) +
		"]/div/div[2]/div[2]/div[2]/div[2]/ul/li[4]/text()"))[2:-2]
		print(carTransType)

		carPrice = str(tree.xpath("//*[@id='listingData']/div[" + str(count) + 
		"]/div/div[2]/div[2]/div[1]/div/text()"))[4:-46]
		print(carPrice)
		print("<br>")
		print("<br>")


		count += 1
		print("</div>")

#Checks for faulty searches by checking if the formed urls either don't find any matching results, 
#or if there is an user input error.
#Redirects to given pages is an error happens.
def checkFaulty(testUrl):
	
	page1 = requests.get(testUrl)

	tree1 = html.fromstring(page1.content)

	test = str(tree1.xpath('.//h1[contains(text(),"")]/text()'))[2:-14]

	test2 = str(tree1.xpath('//*[@id="msg"]/span/text()'))[2:-73]

	if test == "Hups, sivua":		
		redirectURL = "frontpage.html"
		print("<script> alert('Faulty search options. Redicting...') </script>")
		print('<html>')
		print('  <head>')
		print('    <meta http-equiv="refresh" content="0;url='+str(redirectURL)+'" />') 
		print('  </head>')
		print('</html>')

	if test2 == "Antamillasi hakukriteereill":		
		print("<script> alert('Nothing found with given values. Showing closest hits.') </script>")
	
#Runs the functions and outputs the data in html form.
#Imports the stylesheets and JavaScript libraries
if __name__ == "__main__": 

	finalUrl = userSearch()

	checkFaulty(finalUrl)

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

<div id="resultTextDiv">
  <a href="frontpage.html">
    <img id="fpLogoSearch" src="http://www.theonestopcarshop.co.uk/wp-content/uploads/2016/02/car-search.png">
  </a>
  	<div id="resultsText">
	<h2> Search results</h2>''')
	print("<form action= 'saveCar.py' method='POST'>")
	print("<button type='submit' id='savebutton' name='finalUrl' value=" + finalUrl +"  /> Save search</button>")
	print("</form>")
	print('''
	</div>

</div>	
	<div class="container2">
    ''')

	scrapeData(finalUrl)

	print('''
	
		</div>
  <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.3/umd/popper.min.js" integrity="sha384-vFJXuSJphROIrBnz7yo7oB41mKfc8JzQZiCq4NCceLEaO4IHwicKwpJf9c9IpFgh" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.2/js/bootstrap.min.js" integrity="sha384-alpBpkh1PFOepccYVYDB4do5UnbKysX5WZXm3XxPqe5iKTfUKjNkCk9SaVuEZflJ" crossorigin="anonymous"></script>
    ''')
print("</body>")
print("</html>")



