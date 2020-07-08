#web_scraper.py
from urllib.request import urlopen 
from bs4 import BeautifulSoup as soup

#Define the url I am going to web scrape from
my_url  = "https://www.pricerunner.dk/pl/1244-4275270/Koekkenmaskiner-Foodprocessorer/Bosch-MUM9AD1S00-Sammenlign-Priser"

#opening up connection and grabbing the page
uClient = urlopen(my_url)
page_html = uClient.read()
uClient.close() 

#html parsing
page_soup = soup(page_html,"html.parser")

#grabs each product
filename = "List of prices.csv"
f = open(filename,'w')

headers = "website name, price, availability\n"

f.write(headers)


containers = page_soup.findAll("div",{"class":"BY4UGRFGh9"})

for container in containers:
	website_name = container.div.div.button["aria-label"].split("Vis information om")[1]

	price_container = container.findAll("span",{"currency":"DKK"})
	if "." in (price_container[0].text.split("\xa0kr")[0]):
		price = (price_container[0].text.split("\xa0kr")[0]).replace(".",'')
	else:
		price = price_container[0].text.split("\xa0kr")[0]

	available_container = container.findAll("span",{"class":"CAaYFUUbFa VBOOVcu_VV"})
	availability = available_container[0].div["aria-label"]

	print("website name:" + website_name)
	print("price:" + price)
	print("availability:" + availability + "\n")

	f.write(website_name + "," + price + "," + availability + "\n")

f.close()