from src.stores.BestBuy import BestBuy
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Chrome
import webbrowser
import schedule, time

def checkProducts():
    for product in allProducts:
        product.checkProduct()

webbrowser.register('chrome',
    None,
    webbrowser.BackgroundBrowser('C://Program Files (x86)//Google//Chrome//Application//chrome.exe'))

option = webdriver.ChromeOptions()
chrome_prefs = {}
option.experimental_options["prefs"] = chrome_prefs
chrome_prefs["profile.default_content_settings"] = {"images": 2}
chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}
driver = webdriver.Chrome(options=option)

allProducts = []
driver.get("https://www.bestbuy.com/cart")
driver.execute_script("window.open('');")
driver.switch_to.window(driver.window_handles[1])

productLinks = open('products.txt', 'r')
for productLink in productLinks:
    store = productLink[productLink.find('www.') + len('www.'):productLink.rfind('.com')]

    if(store == 'bestbuy'):
        allProducts.append(BestBuy(productLink, driver))
productLinks.close()

for product in allProducts:
    print(product)

schedule.every(5).to(10).seconds.do(checkProducts)
while True:
    schedule.run_pending()
    #time.sleep(1)