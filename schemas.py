from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class CategoryEnum(str, Enum):
    finished = "finished"
    semi_finished = "semi-finished"
    raw = "raw"

class UOMEnum(str, Enum):
    mtr = "mtr"
    mm = "mm"
    ltr = "ltr"
    ml = "ml"
    cm = "cm"
    mg = "mg"
    gm = "gm"
    unit = "unit"
    pack = "pack"

class ProductBase(BaseModel):
    name: str
    category: CategoryEnum
    description: Optional[str]
    product_image: Optional[str]
    sku: str
    unit_of_measure: UOMEnum
    lead_time: int = Field(..., le=999)

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class ProductOut(ProductBase):
    product_id: int
    created_date: Optional[str]
    updated_date: Optional[str]

    class Config:
        orm_mode = True
