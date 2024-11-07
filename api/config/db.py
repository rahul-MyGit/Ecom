from sqlalchemy.orm import Session
from . import models, schemas

class UserRepo:

    async def fetch_by_id(db: Session, _id):
        return db.query(models.User).filter(models.User.id == _id).first()
    
    async def create(db: Session, item: schemas.users.UserCreate):
        db_user = models.User(name=item.name,price=item.price,description=item.description)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
class ItemRepo:

    async def fetch_by_id(db: Session, _id):
        return db.query(models.User).filter(models.Item.id == _id).first()
    
    async def create(db: Session, item: schemas.items.createItem):
        db_item = models.Item(name=item.name, price=item.price,description=item.description, quantity= item.quantity)
        db.add(db_item)
        db.commit()
        db.refresh(ItemRepo)
        return db_item
    

    async def fetchAll(db:Session, skip: int = 0, limit: int = 100):
        return db.query(models.Item).offset(skip).limit(limit).all()
        