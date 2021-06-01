def readProducts(self):
    productLinks = open('products.txt', 'r')
    for productLink in productLinks:
        openedLinks[productLink] = 'Closed'
    productLinks.close()