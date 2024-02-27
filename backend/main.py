# Import necessary modules from Flask framework
from flask import request, jsonify
from config import app, db
from models import Contact


@app.route('/contacts', methods=['GET'])
def get_contacts():
    # Get all contacts from the database
    contacts = Contact.query.all()

    json_contacts = list(map(lambda contact: contact.to_json(), contacts))

    return jsonify({"contacts": json_contacts})


@app.route('/create_contact', methods=['POST'])
def create_contact():
    # Get the data from the request
    data = request.get_json()

    # Create a new contact object using the data
    new_contact = Contact(
        first_name=data['firstName'], last_name=data['lastName'], email=data['email'])

    # If first_name, last_name or email is not provided, return an error
    if not new_contact.first_name or not new_contact.last_name or not new_contact.email:
        return jsonify({"error": "First name, last name and email are required"}), 400

    try:
        # Add the contact to the database
        db.session.add(new_contact)
        db.session.commit()
    except Exception as e:
        # If an error occurs, return an error
        return jsonify({"error": str(e)}), 400

    return jsonify({"message": "Contact created successfully"}), 201


@app.route('/update_contact/<int:user_id>', methods=['PUT'])
def update_contact(user_id):

    # Get the contact from the database
    contact = Contact.query.get(user_id)

    # If the contact does not exist, return an error
    if not contact:
        return jsonify({"error": "Contact not found"}), 404

    # Get the data from the request
    data = request.json

    # Update the contact with the new data
    contact.first_name = data.get('firstName', contact.first_name)
    contact.last_name = data.get('lastName', contact.last_name)
    contact.email = data.get('email', contact.email)

    try:
        # Update the contact in the database
        db.session.commit()
    except Exception as e:
        # If an error occurs, return an error
        return jsonify({"error": str(e)}), 400

    return jsonify({"message": "Contact updated successfully"}), 200


@app.route('/delete_contact/<int:user_id>', methods=['DELETE'])
def delete_contact(user_id):
    # Get the contact from the database
    contact = Contact.query.get(user_id)

    # If the contact does not exist, return an error
    if not contact:
        return jsonify({"error": "Contact not found"}), 404

    try:
        # Delete the contact from the database
        db.session.delete(contact)
        db.session.commit()
    except Exception as e:
        # If an error occurs, return an error
        return jsonify({"error": str(e)}), 400

    return jsonify({"message": "Contact deleted successfully"}), 200


if __name__ == '__main__':
    # Create a context for the Flask application to work within
    with app.app_context():
        # Create all database tables based on defined models using SQLAlchemy
        db.create_all()

    # Run the Flask application in debug mode
    app.run(debug=True)
