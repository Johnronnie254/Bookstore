# models.py

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    genre = Column(String)
    price = Column(Integer)
    availability = Column(Integer, default=0)  # 0 for unavailable, 1 for available

    # Define the relationship between Book and Order
    orders = relationship('Order', back_populates='book')

class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    contact_details = Column(String)
    preferences = Column(String)

    # Define the relationship between Customer and Order
    orders = relationship('Order', back_populates='customer')

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable=False)
    total_price = Column(Integer, nullable=False)

    # Define foreign keys for relationships
    book_id = Column(Integer, ForeignKey('books.id'))
    customer_id = Column(Integer, ForeignKey('customers.id'))

    # Define the relationship between Order and Book/Customer
    book = relationship('Book', back_populates='orders')
    customer = relationship('Customer', back_populates='orders')

# Replace 'sqlite:///example.db' with your actual database connection string
DATABASE_URL = 'sqlite:///example.db'
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)

print(1+1)
