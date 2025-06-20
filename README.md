# Library Management System First Run For SQL
An Library Management System created by ashes using MYSQL, MongoDB, Json and XML. 

Database codes that I used in MYSQL to create:

CREATE DATABASE library_db;
USE library_db;
 
CREATE TABLE Books (
    Book_ID INT PRIMARY KEY AUTO_INCREMENT,
    Title VARCHAR(255),
    Author VARCHAR(255),
    Genre VARCHAR(100),
    ISBN VARCHAR(20),
    Copies_Available INT,
    Metadata JSON
);
 
CREATE TABLE Students (
    Student_ID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100),
    Email VARCHAR(100),
    Major VARCHAR(100)
);
 
CREATE TABLE Borrowing (
    Borrow_ID INT PRIMARY KEY AUTO_INCREMENT,
    Book_ID INT,
    Student_ID INT,
    Borrow_Date DATE,
    Return_Date DATE,
    Status VARCHAR(20),
    FOREIGN KEY (Book_ID) REFERENCES Books(Book_ID),
    FOREIGN KEY (Student_ID) REFERENCES Students(Student_ID)
);
 
CREATE TABLE Librarians (
    Librarian_ID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100),
    Email VARCHAR(100)
);
 
-- Trigger: Update book copies when borrowed
DELIMITER //
CREATE TRIGGER after_borrow_insert
AFTER INSERT ON Borrowing
FOR EACH ROW
BEGIN
  UPDATE Books SET Copies_Available = Copies_Available - 1 WHERE Book_ID = NEW.Book_ID;
END;
//
DELIMITER ;
 
-- Trigger: Update book copies when returned
DELIMITER //
CREATE TRIGGER after_borrow_update
AFTER UPDATE ON Borrowing
FOR EACH ROW
BEGIN
  IF NEW.Status = 'Returned' AND OLD.Status = 'Borrowed' THEN
    UPDATE Books SET Copies_Available = Copies_Available + 1 WHERE Book_ID = NEW.Book_ID;
  END IF;
END;
//
DELIMITER ;
 
-- Stored Procedure: List overdue books
DELIMITER //
CREATE PROCEDURE GetOverdueBooks()
BEGIN
  SELECT * FROM Borrowing
  WHERE Return_Date < CURDATE() AND Status = 'Borrowed';
END;
//
DELIMITER ;

Database codes that I used in MYSQL to insert:

INSERT INTO Books (Title, Author, Genre, ISBN, Copies_Available)
VALUES ('1984', 'George Orwell', 'Dystopian', '1234567890', 5);
 
INSERT INTO Students (Name, Email, Major)
VALUES ('Alice Smith', 'alice@example.com', 'Computer Science');
 
INSERT INTO Books (Title, Author, Genre, ISBN, Copies_Available) VALUES
('The Quantum Detective', 'Rena Shah', 'Sci-Fi Mystery', '9781234560012', 4),
('Cacti and Other Warriors', 'Luis Ortega', 'Botany Fiction', '9781234560029', 2),
('Banana Republic Philosophy', 'Amy Goldman', 'Satire', '9781234560036', 6),
('The Last Algorithm', 'Dan Hacker', 'Tech Thriller', '9781234560043', 3),
('Moonlight Over Mumbai', 'Priya Mehta', 'Romance', '9781234560050', 5),
('Chaos in the Capital', 'George King', 'Political Drama', '9781234560067', 7),
('Wind Code Chronicles', 'Lin Tao', 'Historical Fantasy', '9781234560074', 2),
('Broken Strings', 'Jasper Cole', 'Musical Memoir', '9781234560081', 4),
('Icebergs and Ideologies', 'Sara Kwon', 'Climate Fiction', '9781234560098', 1),
('The Infinite Backpack', 'Max Riverstone', 'Adventure', '9781234560104', 8);
 
 
INSERT INTO Students (Name, Email, Major) VALUES
('Alice McCarthy', 'alice.mc@example.com', 'Computer Science'),
('Brian Osei', 'brian.osei@example.com', 'Mechanical Engineering'),
('Chen Li', 'chen.li@example.com', 'Physics'),
('Dalia Ferreira', 'dalia.ferreira@example.com', 'Biology'),
('Ethan Wells', 'ethan.wells@example.com', 'Literature'),
('Farah Naz', 'farah.naz@example.com', 'Mathematics'),
('George Mendez', 'george.mendez@example.com', 'Art History'),
('Hyejin Park', 'hyejin.park@example.com', 'Chemistry'),
('Ismail Al-Tariq', 'ismail.tariq@example.com', 'International Relations'),
('Jade Robinson', 'jade.robinson@example.com', 'Environmental Studies');
 
 
INSERT INTO Borrowing (Book_ID, Student_ID, Borrow_Date, Return_Date, Status) VALUES
(1, 2, '2024-12-01', '2024-12-15', 'Borrowed'),
(3, 4, '2024-11-20', '2024-12-05', 'Borrowed'),
(5, 6, '2025-01-10', '2025-01-25', 'Borrowed'),
(7, 8, '2025-02-01', '2025-02-14', 'Borrowed'),
(2, 9, '2025-03-01', '2025-03-15', 'Borrowed');
 
 
INSERT INTO Borrowing (Book_ID, Student_ID, Borrow_Date, Return_Date, Status) VALUES
(4, 1, '2025-04-20', '2025-05-04', 'Returned'),
(6, 3, '2025-04-28', '2025-05-12', 'Borrowed'),
(8, 5, '2025-04-29', '2025-05-13', 'Borrowed'),
(9, 7, '2025-04-15', '2025-04-29', 'Returned'),
(10, 10, '2025-04-27', '2025-05-11', 'Borrowed');

