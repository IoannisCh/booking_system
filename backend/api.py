# backend/api.py

from flask import Flask, request, jsonify
from backend.booking_logic import create_booking, get_booking, update_booking, delete_booking
from datetime import datetime

app = Flask(__name__)

@app.route('/bookings', methods=['POST'])
def new_booking():
    data = request.get_json()
    if not data or 'customer' not in data or 'service_id' not in data or 'booking_start' not in data or 'booking_end' not in data:
        return jsonify({'error': 'Missing required data'}), 400

    customer_data = data['customer']
    service_id = data['service_id']
    try:
        booking_start = datetime.strptime(data['booking_start'], '%Y-%m-%d %H:%M:%S')
        booking_end = datetime.strptime(data['booking_end'], '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return jsonify({'error': 'Invalid datetime format'}), 400

    new_booking, error = create_booking(customer_data, service_id, booking_start, booking_end)
    if new_booking:
        return jsonify(new_booking.__dict__), 201
    else:
        return jsonify({'error': error}), 500

@app.route('/bookings/<int:booking_id>', methods=['GET'])
def get_existing_booking(booking_id):
    booking = get_booking(booking_id)
    if booking:
        return jsonify(booking.__dict__), 200
    else:
        return jsonify({'error': 'Booking not found'}), 404

@app.route('/bookings/<int:booking_id>', methods=['PUT'])
def update_existing_booking(booking_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided for update'}), 400

    update_data = {}
    if 'booking_start' in data:
        try:
            update_data['BookingStart'] = datetime.strptime(data['booking_start'], '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return jsonify({'error': 'Invalid booking_start datetime format'}), 400
    if 'booking_end' in data:
        try:
            update_data['BookingEnd'] = datetime.strptime(data['booking_end'], '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return jsonify({'error': 'Invalid booking_end datetime format'}), 400
    if 'booking_status' in data:
        update_data['BookingStatus'] = data['booking_status']

    updated, error = update_booking(booking_id, update_data)
    if updated:
        return jsonify({'message': 'Booking updated successfully'}), 200
    else:
        return jsonify({'error': error}), 404

@app.route('/bookings/<int:booking_id>', methods=['DELETE'])
def delete_existing_booking(booking_id):
    deleted, error = delete_booking(booking_id)
    if deleted:
        return jsonify({'message': 'Booking deleted successfully'}), 200
    else:
        return jsonify({'error': error}), 404

if __name__ == '__main__':
    from backend.database import init_app
    init_app(app)
    app.run(debug=True)