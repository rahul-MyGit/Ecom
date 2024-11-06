from pydantic import BaseModel

class ItemsBase(BaseModel):
    name: str
    price: float
    description: str
    quantity: int

class ItemsCreate(ItemsBase):
    pass

class ItemsEdit(ItemsBase):
    pass
