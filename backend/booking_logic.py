# backend/booking_logic.py

# backend/booking_logic.py

from backend.database import get_db
from backend.models import Booking, Customer, Service
import uuid
from datetime import datetime
from flask import Flask
import pymysql  # Add this line

def create_booking(customer_data, service_id, booking_start, booking_end):
    """Creates a new booking in the database."""
    db = get_db()
    if db is None:
        return None, "Database connection failed"

    try:
        # First, create the customer if they don't exist (we'll refine this later)
        cursor = db.cursor()
        sql_customer = "INSERT INTO Customers (FullName, DateOfBirth, ContactNumber, Email) VALUES (%s, %s, %s, %s)"
        customer_values = (customer_data['FullName'], customer_data.get('DateOfBirth'), customer_data.get('ContactNumber'), customer_data.get('Email'))
        cursor.execute(sql_customer, customer_values)
        customer_id = cursor.lastrowid

        # Generate a unique booking reference
        booking_reference = str(uuid.uuid4())

        # Insert the booking details
        sql_booking = "INSERT INTO Bookings (BookingReference, CustomerID, ServiceID, BookingStart, BookingEnd) VALUES (%s, %s, %s, %s, %s)"
        booking_values = (booking_reference, customer_id, service_id, booking_start, booking_end)
        cursor.execute(sql_booking, booking_values)
        booking_id = cursor.lastrowid

        # Retrieve the newly created booking
        return get_booking(booking_id), None

    except Exception as e:
        db.rollback()
        return None, f"Error creating booking: {e}"
    finally:
        cursor.close()

def get_booking(booking_id):
    """Retrieves a booking by its ID."""
    db = get_db()
    if db is None:
        return None

    try:
        cursor = db.cursor(pymysql.cursors.DictCursor) # Fetch results as dictionaries
        sql = "SELECT * FROM Bookings WHERE BookingID = %s"
        cursor.execute(sql, (booking_id,))
        booking_data = cursor.fetchone()
        if booking_data:
            return Booking(**booking_data)
        return None
    except Exception as e:
        print(f"Error retrieving booking: {e}")
        return None
    finally:
        if 'cursor' in locals() and cursor: # Ensure cursor exists before closing
            cursor.close()

def update_booking(booking_id, update_data):
    """Updates an existing booking."""
    db = get_db()
    if db is None:
        return False, "Database connection failed"

    try:
        cursor = db.cursor()
        set_clauses = []
        values = []
        for key, value in update_data.items():
            if key not in ['BookingID', 'CustomerID', 'ServiceID', 'BookingReference', 'BookingDate']: # Prevent updating these directly for now
                set_clauses.append(f"{key} = %s")
                values.append(value)
        values.append(booking_id)
        sql = f"UPDATE Bookings SET {', '.join(set_clauses)} WHERE BookingID = %s"
        cursor.execute(sql, tuple(values))
        if cursor.rowcount > 0:
            return True, None
        else:
            return False, "Booking not found"
    except Exception as e:
        db.rollback()
        return False, f"Error updating booking: {e}"
    finally:
        cursor.close()

def delete_booking(booking_id):
    """Deletes a booking by its ID."""
    db = get_db()
    if db is None:
        return False, "Database connection failed"

    try:
        cursor = db.cursor()
        sql = "DELETE FROM Bookings WHERE BookingID = %s"
        cursor.execute(sql, (booking_id,))
        if cursor.rowcount > 0:
            return True, None
        else:
            return False, "Booking not found"
    except Exception as e:
        db.rollback()
        return False, f"Error deleting booking: {e}"
    finally:
        cursor.close()

# We'll add functions for retrieving services and potentially customers later

if __name__ == '__main__':
    app = Flask(__name__)
    with app.app_context():
        # Example usage (for testing purposes)
        customer_info = {'FullName': 'John Doe', 'DateOfBirth': '1990-01-15', 'ContactNumber': '123-456-7890', 'Email': 'john.doe@example.com'}
        service_id = 1 # Assuming a service with ID 1 exists
        start_time_str = '2025-04-20 10:00:00'
        end_time_str = '2025-04-20 11:00:00'
        start_time = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S')
        end_time = datetime.strptime(end_time_str, '%Y-%m-%d %H:%M:%S')

        new_booking, error = create_booking(customer_info, service_id, start_time, end_time)
        if new_booking:
            print("New booking created:", new_booking.__dict__)
            updated, update_error = update_booking(new_booking.BookingID, {'BookingStatus': 'Confirmed'})
            if updated:
                retrieved_booking = get_booking(new_booking.BookingID)
                print("Booking updated:", retrieved_booking.__dict__)
                deleted, delete_error = delete_booking(new_booking.BookingID)
                if deleted:
                    print("Booking deleted successfully.")
                else:
                    print("Error deleting booking:", delete_error)
            else:
                print("Error updating booking:", update_error)
        else:
            print("Error creating booking:", error)