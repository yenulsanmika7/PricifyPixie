from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import subprocess
from sqlalchemy.orm import Session
from database import TrackedProducts, SessionLocal
from tools.helpingFunc import check_file_empty, scrape_amazon_product_url, extract_price_from_url, tracked_product_email_confirmation
import json
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

RESULTS_FILEPATH = 'basic_scrapy_spider/output/results.json'

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/')
def root():
    return { "Welcome to" : "PriceWize Backend" }

@app.get("/amazon_scraper/search_keyword={keyword}")
def scrape_products(keyword: str):
    scrapy_crawler = 'basic_scrapy_spider'

    if not keyword.isalnum():
        raise HTTPException(status_code=400, detail="Invalid keyword")   
   
    if check_file_empty(RESULTS_FILEPATH) == True:
        os.remove(RESULTS_FILEPATH)

    activate_command = f'scrapy crawl amazon_search_product -o output/results.json -a keyword={keyword}'
    subprocess.run(activate_command, shell=True, cwd=scrapy_crawler)

    with open(RESULTS_FILEPATH, 'r') as data:        
        product_data = json.load(data)
        for product in product_data:
            if product['price'] == '$':
                product_price = extract_price_from_url(product['product_url'])
                product.price = product_price

    return JSONResponse(content=product_data)

@app.get('/amazon_scraper/product_url={product_url}')
def scrape_amazon_url_product(product_url: str):
    print(product_url)
    product_data = scrape_amazon_product_url(product_url)

    if product_data:
        return JSONResponse(content=product_data)
    else:
        raise HTTPException(status_code=404, detail="Product not found or invalid Amazon URL")

@app.get('/amazon_scraper/product={product_id}')
def get_product(product_id: str):
    with open(RESULTS_FILEPATH, 'r') as data:
        products_data = json.load(data)

    product_data = None

    for product in products_data:
        if str(product['id']) == product_id: 
            product_data = product
            break 

    return JSONResponse(content=product_data)

@app.get('/amazon_scraper/all_tracked_products')
def all_tracked_products(db: Session = Depends(get_db)):    
    tracked_products = db.query(TrackedProducts).all()
    return { 'All Tracked Products': tracked_products}

@app.get('/amazon_scraper/tracked_product={product_id}&user_email={email}')
def add_tracked_product(product_id: str, email: str,  db: Session = Depends(get_db) ):

    with open(RESULTS_FILEPATH, 'r') as data:
        products_data = json.load(data)

    product_data = None

    for product in products_data:
        if str(product['id']) == product_id: 
            product_data = product
            break 

    if product_data != None:
        if db.query(TrackedProducts).filter(TrackedProducts.name == product_data['name']).count() == 0:
            print('success')
            price = float(product_data['price'].replace('$', '').replace(',', ''))
            track_product = TrackedProducts(name=product_data['name'], email=email, url=product_data['product_url'], price=price, image=product_data['images'][0]['large'], tracked=True)
            db.add(track_product)
            db.commit()

            tracked_product_email_confirmation(product_data['name'], price, product_data['product_url'], email)
        else:
            return { "message" : "Product Already added to database!! "}
      

    return { 'Congragulation!' : 'Product added successfully to Database!' }

@app.get('/amazon_scraper/delete_tracked_product={product_id}')
def delete_tracked_product(product_id : str, db: Session = Depends(get_db)):
    tracked_product = db.query(TrackedProducts).filter(TrackedProducts.id == product_id).first()

    if tracked_product:
        db.delete(tracked_product)
        db.commit()
        return {"message": "Tracked product deleted successfully"}

    return {"message": "Tracked product not found"}

