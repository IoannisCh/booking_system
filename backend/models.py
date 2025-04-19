class Customer:
    def __init__(self, CustomerID, FullName, DateOfBirth, ContactNumber, Email):
        self.CustomerID = CustomerID
        self.FullName = FullName
        self.DateOfBirth = DateOfBirth
        self.ContactNumber = ContactNumber
        self.Email = Email 

class Service:
    def __init__(self, ServiceID, ServiceName, Description):
        self.ServiceID = ServiceID
        self.ServiceName = ServiceName 
        self.Description = Description

class Booking:
    def __init__(self, BookingID, BookingReference, CustomerID, ServiceID, BookingStart, BookingEnd, BookingDate, BookingStatus):
        self.BookingID = BookingID
        self.BookingReference = BookingReference
        self.CustomerID = CustomerID
        self.ServiceID = ServiceID
        self.BookingStart = BookingStart
        self.BookingEnd = BookingEnd
        self.BookingDate = BookingDate
        self.BookingStatus = BookingStatus