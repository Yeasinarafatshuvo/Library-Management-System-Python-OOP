from abc import ABC, abstractmethod
from datetime import datetime

#-------------Custom Exceptions------------------
class LibraryError(Exception):
    """Base class Library Related Error"""
    pass

class BookNotFoundError(LibraryError):
    """Raised when a book is not found"""
    pass

class MemberNotFoundError(LibraryError):
    """Raised when member is not found"""
    pass

class BookAlreadyBorrowedError(LibraryError):
    """Raised attempting to borrow an already borrowed book"""
    pass

#---Abstract Class ----
class AbstractBook(ABC):
    @abstractmethod
    def borrow(self, member_id):
        pass

    @abstractmethod
    def return_book(self, member_id):
        pass

#----Book and Member Class--------
class Book(AbstractBook):
    def __init__(self, book_id, title, author, publisher):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.publisher = publisher
        self.is_borrowed = False


    def borrow(self, member_id):
        if self.is_borrowed:
            raise BookAlreadyBorrowedError(f"Book {self.title} is already borrowed")
        self.is_borrowed = True
        print(f"book {self.title} borrowed by member {member_id}")

    def return_book(self, member_id):
        if not self.is_borrowed:
            raise Exception(f"Book {self.title} is not Borrowed")
        self.is_borrowed = False
        print(f"Book {self.title} returned by Member {member_id}")

class Member:
    def __init__(self, member_id, name):
        self.member_id = member_id
        self.name = name

#---Mixin Class For Multiple Inheritence------
class DigitalFeaturesMixin:
    def __init__(self, file_size, file_format):
        self.file_size = file_size
        self.file_format = file_format

    def display_digital_details(self):
        return f"File Size: {self.file_size}MB, Format: {self.file_format}"

class PhysicalFeaturesMixin:
    def __init__(self, weight, dimension):
        self.weight = weight
        self.dimension = dimension

    def display_physical_details(self):
        return f"Weight: {self.weight}kg, Dimension: {self.dimension}"

class DigitalBook(Book, DigitalFeaturesMixin):
    def __init__(self, book_id, title, author, publisher, file_size, file_format):
       Book.__init__(self, book_id, title, author, publisher)
       DigitalFeaturesMixin.__init__(self, file_size, file_format)

class PhysicalBook(Book, PhysicalFeaturesMixin):
    def __init__(self, book_id, title, author, publisher,weight, dimension):
        Book.__init__(self, book_id, title, author, publisher)
        PhysicalFeaturesMixin.__init__(self, weight, dimension)

#-----Logging Decorator-------
def log_operation(func):
    def wrapper(*args, **kwargs):
        print(f"Operation: {func.__name__} called with {args} and kwargs{kwargs}")
        result = func(*args, **kwargs)
        print(f"Operation: {func.__name__} completed.")
        return result
    return wrapper


#---Transaction CLass-----
class Transaction:
    def __init__(self, transaction_id, member_id, book_id, borrow_date, return_date=None):
        self.transaction_id = transaction_id
        self.member_id = member_id
        self.book_id = book_id
        self.borrow_date = borrow_date
        self.return_date = return_date

    def __str__(self) -> str:
        return f"Transaction ID: {self.transaction_id}, Member ID: {self.member_id}, Book ID: {self.book_id}, Borrow Date: {self.borrow_date}, Return Date: {self.return_date}"

#---------Library Management System-----------------

class LibraryManagementSystem:
    def __init__(self):
        self.books = []
        self.members = []
        self.transactions = []

    @log_operation
    def add_book(self, book):
        self.books.append(book)
        print(f"Book {book.title} added to the Library")

    @log_operation
    def add_member(self, member):
        self.members.append(member)
        print(f"Member {member.name} added to the Library")

    
    @log_operation
    def borrow_book(self, member_id, book_id):
        book = self.find_book_by_id(book_id)
        member = self.find_member_by_id(member_id)
        book.borrow(member_id)
        transaction = Transaction(
            transaction_id=len(self.transactions) +1,
            member_id=member_id,
            book_id=book_id,
            borrow_date=datetime.now()
        )

        self.transactions.append(transaction)

        print(f"Transaction Successfull {transaction}")

    @log_operation
    def return_book(self, member_id, book_id):
        book = self.find_book_by_id(book_id)
        book.return_book(member_id)
        for transaction in self.transactions:
            if transaction.book_id == book_id and transaction.return_date is None:
                transaction.return_date = datetime.now()
                print(f"Return recorded for transaction ID: {transaction.transaction_id}")
                break

    
    def find_book_by_id(self, book_id):
        for book in self.books:
            if book.book_id == book_id:
                return book
        raise BookNotFoundError(f"Book with Id {book_id} not found")

    def find_member_by_id(self, member_id):
        for member in self.members:
            if member.member_id == member_id:
                return member
        raise MemberNotFoundError(f"Member with Id {member_id} not found.")


if __name__ == '__main__':
    library = LibraryManagementSystem()

    #Add Books
    book1 = DigitalBook(1, "Python Basics", "John Doe", "TechPress", 5, "PDF")
    book2 = PhysicalBook(2, "Advanced Python", "Jane Smith", "CodeHouse", 1.2, "20x15 cm")
    library.add_book(book1)
    library.add_book(book2)
    print(book1.display_digital_details())
    print(book2.display_physical_details())



    #Add Members 
    member1 = Member(101, "Alice")
    member2 = Member(102, "Bob")
    library.add_member(member1)
    library.add_member(member2)

    #Borrow and return Book
    library.borrow_book(101, 1) #Alice borrow digital book
    library.return_book(101, 1) # Alice return digital book

    library.borrow_book(102, 2) # Bob Borrow physical book
    library.borrow_book(103, 1) # ember with Id 103 not found.
    



    

    





     








        


