from pydantic import BaseModel

class CreateProduct(BaseModel):
    name: str
    description: str
    price: float
    active: bool

class UpdateProduct(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    active: bool | None = None

class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float
    active: bool

    class Config:
        fromAttributes = True