# Library Management System (Python CLI + MySQL + MongoDB + JSON/XML)

import mysql.connector
import pymongo
import json
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

# MySQL SETUP 

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Dracominefol77.',
    'database': 'library_db'
}

mysql_conn = mysql.connector.connect(**db_config)
cursor = mysql_conn.cursor(dictionary=True)

# MongoDB SETUP 

mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["library"]
mongo_reviews = mongo_db["book_reviews"]

# FUNCTIONS for search, borrow/return and view operations

def search_books(title):
    print(f"DEBUG: Searching for books with title containing: {title}")
    query = "SELECT * FROM Books WHERE Title LIKE %s"
    cursor.execute(query, (f"%{title}%",))
    results = cursor.fetchall()
    if not results:
        print("No books found.")
    else:
        for row in results:
            print(row)

def borrow_book(book_id, student_id):
    borrow_date = datetime.now()
    return_date = borrow_date + timedelta(days=14)

    query = """
        INSERT INTO Borrowing (Book_ID, Student_ID, Borrow_Date, Return_Date, Status)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (book_id, student_id, borrow_date, return_date, 'Borrowed'))

    

    mysql_conn.commit()
    print("Book borrowed successfully.")

def return_book(borrow_id):
    cursor.execute("UPDATE Borrowing SET Status = 'Returned' WHERE Borrow_ID = %s", (borrow_id,))

    

    mysql_conn.commit()
    print("Book returned.")

def get_overdue_books_stored_proc():
    print("Overdue books (via stored procedure):")
    cursor.callproc("GetOverdueBooks")
    for result in cursor.stored_results():
        for row in result.fetchall():
            print(row)

def add_book_metadata(book_id, publisher, edition, summary):
    metadata = json.dumps({
        "publisher": publisher,
        "edition": edition,
        "summary": summary
    })
    cursor.execute("UPDATE Books SET Metadata = %s WHERE Book_ID = %s", (metadata, book_id))
    mysql_conn.commit()

def export_borrowings_to_xml():
    cursor.execute("SELECT * FROM Borrowing")
    borrowings = cursor.fetchall()
    root = ET.Element("Borrowings")
    for b in borrowings:
        record = ET.SubElement(root, "Borrowing")
        for key, value in b.items():
            ET.SubElement(record, key).text = str(value)
    tree = ET.ElementTree(root)
    tree.write("borrowings.xml")
    print("Exported to borrowings.xml")

def add_student_review(book_id, student_id, rating, review):
    feedback = {
        "book_id": book_id,
        "student_id": student_id,
        "rating": rating,
        "review": review,
        "timestamp": datetime.now()
    }
    mongo_reviews.insert_one(feedback)
    print("Review submitted.")

# CLI 

def main():
    while True:
        print("\n1. Search Book\n2. Borrow Book\n3. Return Book\n4. Add Book Metadata\n5. Export Borrowings to XML\n6. Add Review\n7. View Overdue via Stored Procedure\n0. Exit")
        choice = input("Select option: ")

        if choice == '1':
            title = input("Enter book title to search: ")
            search_books(title)
            input("\nPress Enter to return to the menu...")
        elif choice == '2':
            book_id = int(input("Book ID: "))
            student_id = int(input("Student ID: "))
            borrow_book(book_id, student_id)
        elif choice == '3':
            borrow_id = int(input("Borrow ID: "))
            return_book(borrow_id)
        elif choice == '4':
            book_id = int(input("Book ID: "))
            publisher = input("Publisher: ")
            edition = input("Edition: ")
            summary = input("Summary: ")
            add_book_metadata(book_id, publisher, edition, summary)
        elif choice == '5':
            export_borrowings_to_xml()
        elif choice == '6':
            book_id = int(input("Book ID: "))
            student_id = int(input("Student ID: "))
            rating = int(input("Rating (1-5): "))
            review = input("Write your review: ")
            add_student_review(book_id, student_id, rating, review)
        elif choice == '7':
            get_overdue_books_stored_proc()
        elif choice == '0':
            break
        else:
            print("Invalid option.")

if __name__ == '__main__':
    main()