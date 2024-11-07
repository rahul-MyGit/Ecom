from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean
from sqlalchemy.orm import relationship
from utils.init_db import Base

class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(80), nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    isAdmin = Column(Boolean, default=False)
    items = relationship("Item", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return 'UserModel(name=%s, email=%s, password=%s, isAdmin=%s)' % (self.name, self.email, self.password, self.isAdmin)

class Item(Base):
    __tablename__ = "item"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(80), nullable=False, unique=True)
    price = Column(Float(precision=2), nullable=False)
    description = Column(String(200))
    quantity = Column(Integer, index=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship("User", back_populates="items")

    def __repr__(self):
        return 'ItemModel(name=%s, price=%s, description=%s, quantity=%s)' % (self.name, self.price, self.description, self.quantity)
