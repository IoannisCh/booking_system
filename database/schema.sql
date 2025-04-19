-- schema.sql for MySQL

-- Drop tables if they exist to start fresh (for development purposes)
DROP TABLE IF EXISTS Bookings;
DROP TABLE IF EXISTS Customers;
DROP TABLE IF EXISTS Services;

-- Create Customers table
CREATE TABLE Customers (
    CustomerID INT PRIMARY KEY AUTO_INCREMENT,
    FullName VARCHAR(255) NOT NULL,
    DateOfBirth DATE,
    ContactNumber VARCHAR(20),
    Email VARCHAR(255)
);

-- Create Services table
CREATE TABLE Services (
    ServiceID INT PRIMARY KEY AUTO_INCREMENT,
    ServiceName VARCHAR(255) NOT NULL,
    Description TEXT
    -- You might want to add more details like price, duration, etc. later
);

-- Create Bookings table
CREATE TABLE Bookings (
    BookingID INT PRIMARY KEY AUTO_INCREMENT,
    BookingReference VARCHAR(50) UNIQUE NOT NULL,
    CustomerID INT NOT NULL,
    ServiceID INT NOT NULL,
    BookingStart DATETIME NOT NULL,
    BookingEnd DATETIME NOT NULL,
    BookingDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    BookingStatus VARCHAR(50) DEFAULT 'Pending',
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID),
    FOREIGN KEY (ServiceID) REFERENCES Services(ServiceID)
);