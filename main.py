from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Chrome
import requests
from datetime import datetime
import schedule, time
import webbrowser
from bs4 import BeautifulSoup

tabs = 0
agent = {'User-Agent':'Mozilla/5.0'}
webbrowser.register('chrome',
	None,
	webbrowser.BackgroundBrowser('C://Program Files (x86)//Google//Chrome//Application//chrome.exe'))

option = webdriver.ChromeOptions()
chrome_prefs = {}
option.experimental_options["prefs"] = chrome_prefs
chrome_prefs["profile.default_content_settings"] = {"images": 2}
chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}
driver = webdriver.Chrome(options=option)

openedLinks = {}

class color:
   PURPLE = '\033[1;35;48m'
   CYAN = '\033[1;36;48m'
   BOLD = '\033[1;37;48m'
   BLUE = '\033[1;34;48m'
   GREEN = '\033[1;32;48m'
   YELLOW = '\033[1;33;48m'
   RED = '\033[1;31;48m'
   BLACK = '\033[1;30;48m'
   UNDERLINE = '\033[4;37;48m'
   END = '\033[1;37;0m'

def readProducts():
    productLinks = open('products.txt', 'r')
    for productLink in productLinks:
        openedLinks[productLink] = 'Closed'
    productLinks.close()

def checkProductGPU():
    print(color.PURPLE + 'Checking products...' + color.END)
    productLinks = open('products.txt', 'r')

    for productLink in openedLinks:
        now = datetime.now()
        current_time = now.strftime('%H:%M:%S')
        print('Current Time =', current_time)

        page = requests.get(productLink, headers=agent)
        soup = BeautifulSoup(page.content, 'html.parser')
        name = soup.select_one('.sku-title .heading-5').text.strip()
        price = soup.select_one('.priceView-hero-price.priceView-customer-price').text.strip()
        price = str(price.split(' is ')[-1])
        status = soup.select_one('.add-to-cart-button').text.strip()

        if status == 'Add to Cart':
            print(color.GREEN + name + color.END + color.YELLOW + ' ' + price + color.END)
            if openedLinks[productLink] == 'Closed':
                openedLinks[productLink] = 'Opened'
                openProductPage(productLink)
        else:
            print(color.RED + name + ' ' + price + ' ' + status + color.END)
    print()
    productLinks.close()

def openProductPage(link):
    driver.get(link)
    driver.find_element_by_class_name("add-to-cart-button").click()
    time.sleep(2)
    driver.get("https://www.bestbuy.com/cart")
    global tabs
    tabs = tabs + 1
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[tabs])

if __name__ == "__main__":
    readProducts()
    #print(openedLinks)
    schedule.every(5).to(10).seconds.do(checkProductGPU)

    while True:
        schedule.run_pending()
        #time.sleep(1)