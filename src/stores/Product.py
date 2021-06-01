class Product:
    def __init__(self, name, price, status, url):
        self.name = name
        self.price = price
        self.status = status
        self.url = url
    
    def __str__(self):
        return "{self.product} costs ${self.price} and is currently {self.status}\n{self.url}"