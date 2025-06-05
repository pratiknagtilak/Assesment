from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/product/list", response_model=List[schemas.ProductOut])
def list_products(page: int = 1, db: Session = Depends(get_db)):
    offset = (page - 1) * 10
    return db.query(models.Product).offset(offset).limit(10).all()

@app.get("/product/{pid}/info", response_model=schemas.ProductOut)
def get_product_info(pid: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.product_id == pid).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.post("/product/add", response_model=schemas.ProductOut)
def add_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.put("/product/{pid}/update", response_model=schemas.ProductOut)
def update_product(pid: int, product: schemas.ProductUpdate, db: Session = Depends(get_db)):
    db_product = db.query(models.Product).filter(models.Product.product_id == pid).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    for key, value in product.dict().items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product
