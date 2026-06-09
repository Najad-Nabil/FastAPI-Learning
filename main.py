from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException
from models import Product
from config import SessionLocal, engine
import database_schema
from sqlalchemy.orm import Session

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "https://fast-api-learning-hazel.vercel.app"
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

database_schema.Base.metadata.create_all(bind=engine)

products = [
    Product(id = 1 ,name =  "Laptop" ,description =  "ASUS ROG" ,price = 59999 ,quantity = 10),
    Product(id = 2 ,name = "Mobile" ,description =  "Iphone 17 pro max" ,price =  157999 ,quantity =  10),
    Product(id = 3 ,name = "Tablet" ,description =  "Samsung Z Fold" ,price =  124999 ,quantity =  10),
    Product(id = 4 ,name = "Mouse" ,description =  "Corsair" ,price =  5999 ,quantity =  10)
]

def init_db():
    db = SessionLocal()
    count = db.query(database_schema.ProductDB).count
    if count == 0:
        for product in products:
            db.add(database_schema.ProductDB(**product.model_dump()))
        db.commit()
init_db()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/products")
def view_products(db: Session = Depends(get_db)):
    db_products = db.query(database_schema.ProductDB).all()
    return db_products

@app.get("/products/{product_id}")
def view_one_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_schema.ProductDB).filter(database_schema.ProductDB.id == product_id).first()
    if db_product:
        return db_product
    raise HTTPException(status_code=404, detail="Product not found")

@app.post("/products")
def add_product(product: Product, db: Session = Depends(get_db)):
    db.add(database_schema.ProductDB(**product.model_dump()))
    db.commit()
    return product

@app.put("/products/{id}")
def update_product(id: int, product: Product, db: Session = Depends(get_db)):
    db_products = db.query(database_schema.ProductDB).filter(database_schema.ProductDB.id == id).first()
    if db_products:
        db_products.name = product.name
        db_products.description = product.description
        db_products.price = product.price
        db_products.quantity = product.quantity
        db.commit()
        return {"message" : "Product Updated Successfully"}
    else:
        raise HTTPException(status_code = 404, detail = "Product Not Found")
        
@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_products = db.query(database_schema.ProductDB).filter(database_schema.ProductDB.id == product_id).first()
    if db_products:
        db.delete(db_products)
        db.commit()
        return {"message" : "Product Deleted Successfully"}
    else:
        raise HTTPException(status_code = 404, detail = "Product Not Found")
