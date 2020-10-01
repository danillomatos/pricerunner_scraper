from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from IPython.display import clear_output

class Product:
	def __init__(self, name, price, previous_price, availability, seller):
		self.name = name
		try:
			self.price = float(price.split('€')[0].replace('.','').replace(",", "."))
			self.previous_price = float(previous_price.split('€')[0].replace('.','').replace(",", "."))
			self.price_diff = round((1-self.price/self.previous_price)*100,2)
		except:
			self.price, self.previous_price, self.price_diff = '--', '--', '--'

		self.availability = availability
		self.seller = seller

		
	def __str__(self,idx):
		return f"{idx}. {self.name} \nPrice: {self.price}€   Previous price: {self.previous_price}€   Available: {self.availability}\n Discount: {self.price_diff}%\n"

	def get_link(self):
		element = driver.find_element_by_link_text(self.name)
		return element.get_attribute("href")

product = input("What are you looking for today? Try to be as specific as possible:\n")
#product = "xiaomi scooter"
''' Here the browser gets opened '''
options = webdriver.ChromeOptions()
options.add_experimental_option("prefs", {"profile.block_third_party_cookies": True})
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument("headless")

driver = webdriver.Chrome(ChromeDriverManager().install(), options = options)

driver.get("https://amazon.de")
search = driver.find_element_by_id("twotabsearchtextbox")
search.send_keys(product)
search.send_keys(Keys.RETURN)

try:	
	element = WebDriverWait(driver, 5).until(
		EC.presence_of_element_located((By.ID, "search"))
	)
	# ALL CONTAINERS
	containers = driver.find_elements_by_xpath("//div[@data-component-type= 's-search-result']")
# JUST ORGANIZING THE TEXT INSIDE!
except:
	driver.quit()

products = []

for container in containers:
	data_list = container.text.split("\n")

	if "Gesponsert" in container.text:
		data_list.pop(0)

	try:
		if "€" not in data_list[2]:
			data_list.insert(2, "Unavailable")
			availability = "No"
		else:
			availability = "Yes"

		if "€" not in data_list[3] and "€" in data_list[2]:
			data_list.insert(3, data_list[2])

	except:

		continue

	products.append(Product(data_list[0], data_list[2], data_list[3], availability, "Amazon"))

clear_output()

high_disc = 0 # Highest discount
for idx, product in enumerate(products):
	print(product.__str__(idx))
	if product.price_diff!='--' and  product.price_diff > high_disc:
		best_deal = product
		high_disc = product.price_diff

answer = input(f"The highest discount is for {best_deal.name}.\n It was {best_deal.previous_price}€ and now is{best_deal.price}€. A {best_deal.price_diff}% decrease!.\n\n Would you like to open the product page? (y/n)")

options_2 = webdriver.ChromeOptions()
options_2.add_experimental_option("prefs", {"profile.block_third_party_cookies": True})
options_2.add_argument('--ignore-certificate-errors')
while True:
	if answer in ['y','yes']:
		link = best_deal.get_link()
		driver2 = webdriver.Chrome(ChromeDriverManager().install(), options = options_2)
		driver2.get(link)
		break
	elif answer in ['n','no']:
		answer_2 = input('\nAny other value from the list you would like to check? (y/n)\t')
		if answer_2 in ['y','yes']:
			while True:
				try:
					idx_no = input('\nType in the corresponding number:\t')
					link = products[int(idx_no)].get_link()
					break
				except:
					print('Try a valid number this time')
			driver2 = webdriver.Chrome(ChromeDriverManager().install(), options = options_2)
			driver2.get(link)

		elif answer_2 in ['n','no']:
			break
		else:
			print('\nNot a valid answer!\n')
	else:
		print('Not a valid answer')

clear_output()
print('\nThanks for using me!\n')