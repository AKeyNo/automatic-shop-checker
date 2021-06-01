from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Chrome
import requests
from datetime import datetime
import schedule, time
import webbrowser
from bs4 import BeautifulSoup

from .Product import Product
from ..utilities.color import color

class BestBuy(Product):    
    agent = {'User-Agent':'Mozilla/5.0'}

    def __init__(self, url, driver):
        self.name = ''
        self.price = 0
        self.status = ''
        self.url = url
        self.driver = driver
        self.opened = False
        self.checkProduct()

    def checkProduct(self):
        print(color.PURPLE + 'Checking products...' + color.END)
        productLinks = open('products.txt', 'r')

        now = datetime.now()
        current_time = now.strftime('%H:%M:%S')
        print('Current Time =', current_time)

        page = requests.get(self.url, headers=self.agent)
        soup = BeautifulSoup(page.content, 'html.parser')
        self.name = soup.select_one('.sku-title .heading-5').text.strip()
        self.price = soup.select_one('.priceView-hero-price.priceView-customer-price').text.strip()
        self.price = str(self.price.split(' is ')[-1])
        self.status = soup.select_one('.add-to-cart-button').text.strip()

        if self.status == 'Add to Cart':          
            print(color.GREEN + self.name + color.END + color.YELLOW + ' ' + self.price + color.END)
            if self.opened == False:
                self.opened = True
                self.openProductPage()
        else:
            print(color.RED + self.name + ' ' + self.price + ' ' + self.status + color.END)
        #print()

    def openProductPage(self):
        self.driver.switch_to.window(self.driver.window_handles[1])        
        self.driver.get(self.url)
        self.driver.find_element_by_class_name("add-to-cart-button").click()
        time.sleep(2)
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.driver.refresh()

    def closeDriver(self, driver):
        self.driver.close()