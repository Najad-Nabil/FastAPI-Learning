from fastapi import FastAPI
from fastapi import HTTPException
from models import Product

app = FastAPI()

@app.get("/")
def greet():
    return ("Welcome to my new project")

products = [
    Product(id = 1 ,name =  "Laptop" ,description =  "ASUS ROG" ,price = 59999 ,quantity = 10),
    Product(id = 2 ,name = "Mobile" ,description =  "Iphone 17 pro max" ,price =  157999 ,quantity =  10),
    Product(id = 3 ,name = "Tablet" ,description =  "Samsung Z Fold" ,price =  124999 ,quantity =  10),
    Product(id = 4 ,name = "Mouse" ,description =  "Corsair" ,price =  5999 ,quantity =  10)
]

@app.get("/product")
def view_products():
    return products

@app.get("/product/{product_id}")
def view_one_product(product_id: int):
    for product in products:
        if product_id == product.id:
            return product
    raise HTTPException(status_code=404, detail="Product not found")

@app.post("/product/add-product")
def add_product(product: Product):
    products.append(product)
    return product

@app.put("/product/update")
def update_product(id: int, product: Product):
    for i in range(len(products)):
        if products[i].id == id:
            products[i] = product
            return products[i]
        

