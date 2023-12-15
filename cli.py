# cli.py

import click
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Book, Customer, Order

DATABASE_URL = 'sqlite:///example.db'  # Adjust with your actual database connection string
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

@click.group()
def main():
    """Bookstore Manager CLI."""
    pass

@main.command()
@click.option('--title', prompt='Book Title', help='Title of the book')
@click.option('--author', prompt='Author', help='Author of the book')
@click.option('--genre', prompt='Genre', help='Genre of the book')
@click.option('--price', prompt='Price', type=float, help='Price of the book')
def add_book(title, author, genre, price):
    """Add a new book to the inventory."""
    session = Session()
    new_book = Book(title=title, author=author, genre=genre, price=price)
    session.add(new_book)
    session.commit()
    click.echo(f"Book '{title}' added to the inventory.")

@main.command()
def list_books():
    """List all books in the inventory."""
    session = Session()
    books = session.query(Book).all()
    for book in books:
        click.echo(f"{book.title} by {book.author}, Genre: {book.genre}, Price: ${book.price}")

@main.command()
@click.option('--title', prompt='Book Title', help='Title of the book to update')
@click.option('--new-title', prompt='New Title', help='New title for the book')
@click.option('--new-author', prompt='New Author', help='New author for the book')
@click.option('--new-genre', prompt='New Genre', help='New genre for the book')
@click.option('--new-price', prompt='New Price', type=float, help='New price for the book')
def update_book(title, new_title, new_author, new_genre, new_price):
    """Update information for a specific book."""
    session = Session()
    book = session.query(Book).filter_by(title=title).first()
    if book:
        book.title = new_title or book.title
        book.author = new_author or book.author
        book.genre = new_genre or book.genre
        book.price = new_price or book.price
        session.commit()
        click.echo(f"Book '{title}' updated.")
    else:
        click.echo(f"Book '{title}' not found.")

@main.command()
@click.option('--title', prompt='Book Title', help='Title of the book to delete')
def delete_book(title):
    """Delete a book from the inventory."""
    session = Session()
    book = session.query(Book).filter_by(title=title).first()
    if book:
        session.delete(book)
        session.commit()
        click.echo(f"Book '{title}' deleted from the inventory.")
    else:
        click.echo(f"Book '{title}' not found.")

@main.command()
@click.option('--name', prompt='Customer Name', help='Name of the customer')
@click.option('--contact-details', prompt='Contact Details', help='Contact details of the customer')
@click.option('--preferences', prompt='Preferences', help='Customer preferences')
def add_customer(name, contact_details, preferences):
    """Add a new customer to the database."""
    session = Session()
    new_customer = Customer(name=name, contact_details=contact_details, preferences=preferences)
    session.add(new_customer)
    session.commit()
    click.echo(f"Customer '{name}' added to the database.")

@main.command()
def list_customers():
    """List all customers in the database."""
    session = Session()
    customers = session.query(Customer).all()
    for customer in customers:
        click.echo(f"Customer: {customer.name}, Contact: {customer.contact_details}, Preferences: {customer.preferences}")

@main.command()
@click.option('--name', prompt='Customer Name', help='Name of the customer to update')
@click.option('--new-name', prompt='New Name', help='New name for the customer')
@click.option('--new-contact-details', prompt='New Contact Details', help='New contact details for the customer')
@click.option('--new-preferences', prompt='New Preferences', help='New preferences for the customer')
def update_customer(name, new_name, new_contact_details, new_preferences):
    """Update information for a specific customer."""
    session = Session()
    customer = session.query(Customer).filter_by(name=name).first()
    if customer:
        customer.name = new_name or customer.name
        customer.contact_details = new_contact_details or customer.contact_details
        customer.preferences = new_preferences or customer.preferences
        session.commit()
        click.echo(f"Customer '{name}' updated.")
    else:
        click.echo(f"Customer '{name}' not found.")

@main.command()
@click.option('--customer-name', prompt='Customer Name', help='Name of the customer placing the order')
@click.option('--book-title', prompt='Book Title', help='Title of the book in the order')
@click.option('--quantity', prompt='Quantity', type=int, help='Quantity of books in the order')
def track_order(customer_name, book_title, quantity):
    """Record a new customer order."""
    session = Session()
    customer = session.query(Customer).filter_by(name=customer_name).first()
    book = session.query(Book).filter_by(title=book_title).first()

    if customer and book:
        total_price = quantity * book.price
        new_order = Order(quantity=quantity, total_price=total_price, book=book, customer=customer)
        session.add(new_order)
        session.commit()
        # cli.py (continued)

        click.echo(f"Order placed by {customer_name} for {quantity} copies of '{book_title}'. Total Price: ${total_price}")
    else:
        click.echo("Customer or book not found.")

@main.command()
def list_orders():
    """List all customer orders."""
    session = Session()
    orders = session.query(Order).all()
    for order in orders:
        click.echo(f"Order ID: {order.id}, Customer: {order.customer.name}, Book: {order.book.title}, Quantity: {order.quantity}, Total Price: ${order.total_price}")

# Add this section to your cli.py file after the previous commands
from datetime import datetime

def seed_data():
    session = Session()

    # Seed books
    books_data = [
        {'title': 'The Great Gatsby', 'author': 'F. Scott Fitzgerald', 'genre': 'Fiction', 'price': 19.99},
        {'title': 'To Kill a Mockingbird', 'author': 'Harper Lee', 'genre': 'Fiction', 'price': 29.99},
        {'title': '1984', 'author': 'George Orwell', 'genre': 'Dystopian', 'price': 24.99},
        {'title': 'The Catcher in the Rye', 'author': 'J.D. Salinger', 'genre': 'Coming-of-age', 'price': 22.99},
        {'title': 'Pride and Prejudice', 'author': 'Jane Austen', 'genre': 'Romance', 'price': 18.99},
    ]

    for book_data in books_data:
        new_book = Book(**book_data)
        session.add(new_book)

    # Seed customers
    customers_data = [
        {'name': 'Alice Johnson', 'contact_details': 'Email: alice@example.com', 'preferences': 'Sci-Fi'},
        {'name': 'Bob Smith', 'contact_details': 'Phone: 555-1234', 'preferences': 'Mystery'},
        {'name': 'Charlie Brown', 'contact_details': 'Email: charlie@example.com', 'preferences': 'Thriller'},
        {'name': 'David Miller', 'contact_details': 'Phone: 555-5678', 'preferences': 'Fantasy'},
        {'name': 'Eve Wilson', 'contact_details': 'Email: eve@example.com', 'preferences': 'Historical Fiction'},
    ]

    for customer_data in customers_data:
        new_customer = Customer(**customer_data)
        session.add(new_customer)

    session.commit()
    click.echo("Sample data seeded successfully.")

seed_data()

if __name__ == '__main__':
    main()

