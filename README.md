# pricerunner_scraper

This is a pricerunner_scraper, currently one needs to manually input the link of the product to obtain the list of prices in a csv_file.
I plan on implementing more detailed features in the near future like asking the user for the name of the product and also scraping amazon.de

Update [01/10/2020]:
I added an amazon.de scraper just in time for black friday. It verifies the first page of products and returns the biggest discounts. I decided to not
create csv files this time and just print the values on the prompt. It installs chromedriver for every run, if you have it in your computer, just change
the command to follow the path in which your driver is located.
