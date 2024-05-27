# # # app.py

# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:12345@localhost:3306/IntelliCart'
# db = SQLAlchemy(app)

# # Define your SQLAlchemy model here

# from sqlalchemy import text

# def execute_sql_file(filename):
#     with app.app_context():
#         with app.open_resource(filename, mode='r') as f:
#             sql_commands = f.read()
#             for command in sql_commands.split(';'):
#                 if command.strip():
#                     db.session.execute(text(command))
#             db.session.commit()

# if __name__ == '__main__':
#     execute_sql_file('IntelliCart.sql')
#     app.run(debug=True)

# from flask import Flask, request, jsonify
# from flask_sqlalchemy import SQLAlchemy
# import datetime;

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:12345@localhost:3306/IntelliCart'
# db = SQLAlchemy(app)

# # Define the User class
# class User(db.Model):
#     __tablename__ = 'Users'
#     user_id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(255))
#     email = db.Column(db.String(255))
#     password = db.Column(db.String(255))
#     phone = db.Column(db.String(255))
#     created_at = db.Column(db.DateTime)
#     is_admin = db.Column(db.Boolean)

# # Route to create a new user
# @app.route('/users', methods=['POST'])
# def create_user():
#     data = request.json
#     new_user = User(username=data['username'], email=data['email'], password=data['password'], phone=data['phone'], created_at=datetime.now(), is_admin=False)
#     db.session.add(new_user)
#     db.session.commit()
#     return jsonify({'message': 'User created successfully'}), 201



# # Route to delete a user by ID
# @app.route('/users/<int:user_id>', methods=['DELETE'])
# def delete_user(user_id):
#     user = User.query.get(user_id)
#     if not user:
#         return jsonify({'message': 'User not found'}), 404
#     db.session.delete(user)
#     db.session.commit()
#     return jsonify({'message': 'User deleted successfully'}), 200

# # Route to update a user by ID
# @app.route('/users/<int:user_id>', methods=['PUT'])
# def update_user(user_id):
#     user = User.query.get(user_id)
#     if not user:
#         return jsonify({'message': 'User not found'}), 404
    
#     data = request.json
#     if 'username' in data:
#         user.username = data['username']
#     if 'email' in data:
#         user.email = data['email']
#     if 'password' in data:
#         user.password = data['password']
#     if 'phone' in data:
#         user.phone = data['phone']
#     if 'created_at' in data:
#         user.created_at = data['created_at']
#     if 'is_admin' in data:
#         user.is_admin = data['is_admin']
    
#     db.session.commit()
#     return jsonify({'message': 'User updated successfully'}), 200

# if __name__ == '__main__':
#     app.run(debug=True)

# app.py

from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import jwt
import logging
import random
import string
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:12345@localhost:3306/IntelliCart'
db = SQLAlchemy(app)
app.secret_key = 'a21112001m'

# Define your SQLAlchemy model here

from sqlalchemy import text

# Function to execute SQL commands from a file
# def execute_sql_file(filename):
#     with app.app_context():
#         with app.open_resource(filename, mode='r') as f:
#             sql_commands = f.read()
#             for command in sql_commands.split(';'):
#                 if command.strip():
#                     db.session.execute(text(command))
#             db.session.commit()

# Model class for Users
class User(db.Model):
    __tablename__ = 'Users'  # Specify the table name
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.now)
    is_admin = db.Column(db.Boolean)



class Purchase(db.Model):
    __tablename__ = 'Purchases'
    purchase_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'))
    purchase_date = db.Column(db.DateTime, default=datetime.now)
    payment_id = db.Column(db.Integer, unique=True)    


def generate_jwt(user_id, purchase_id):
    payload = {
        'user_id': user_id,
        'purchase_id': purchase_id,
        'exp': datetime.utcnow() + timedelta(hours=1)  # Token expires in 1 hour
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    return token


def create_purchase(user_id):
    new_purchase = Purchase(user_id=user_id, purchase_date=datetime.now())
    db.session.add(new_purchase)
    db.session.commit()
    return new_purchase.purchase_id


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    if user and user.password == data['password']:
        purchase_id = create_purchase(user.user_id)
        token = generate_jwt(user.user_id, purchase_id)
        return jsonify({'token': token}), 200
    return jsonify({'message': 'Invalid credentials'}), 401



# API endpoint to create a new user
@app.route('/users/adduser', methods=['POST'])
def create_user():
    data = request.json
    new_user = User(username=data['username'], email=data['email'], password=data['password'], phone=data['phone'], created_at=datetime.now(), is_admin=False)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

# Route to get all users
import logging

@app.route('/users/getusers', methods=['GET'])
def get_users():
    try:
        # Fetch users from the database
        users = User.query.all()
        
        # Log the number of users retrieved
        app.logger.info(f"Retrieved {len(users)} users from the database")
        
        # Create a list to store user data
        result = []
        for user in users:
            user_data = {
                'user_id': user.user_id,
                'username': user.username,
                'email': user.email,
                'phone': user.phone
            }
            result.append(user_data)
        
        # Log the user data before returning
        app.logger.debug(f"User data: {result}")
        
        # Return the user data as JSON
        return jsonify(result), 200
    
    except Exception as e:
        # Log any exceptions that occur during data retrieval
        app.logger.error(f"An error occurred: {str(e)}")
        return jsonify({'error': 'An error occurred while fetching users'}), 500
    

# Route to delete a user by ID
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 200 


# Route to update a user by ID
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    data = request.json
    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        user.email = data['email']
    if 'password' in data:
        user.password = data['password']
    if 'phone' in data:
        user.phone = data['phone']
    if 'is_admin' in data:
        user.is_admin = data['is_admin']
    
    db.session.commit()
    return jsonify({'message': 'User updated successfully'}), 200

from flask import session

import random
import string
import uuid

# Route for guest login
@app.route('/guest/login', methods=['POST'])
def guest_login():
  
    # Create a new user in the database
    new_user = User(username="", email="", password="", created_at=datetime.now(), is_admin=False)
    db.session.add(new_user)
    db.session.commit()

    # Create a new purchase for the guest user
    purchase_id = create_purchase(new_user.user_id)

    # Generate a JWT token for the guest user
    token = generate_jwt(new_user.user_id, purchase_id)

    # Return only the token
    return jsonify({'token': token}), 200

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        user_data = {
            'user_id': user.user_id,
            'username': user.username,
            'email': user.email,
            'phone': user.phone,
            'created_at': user.created_at,
            'is_admin': user.is_admin
        }
        return jsonify(user_data), 200
    else:
        return jsonify({'message': 'User not found'}), 404

from flask import Flask, request, jsonify, send_file, session, url_for
import qrcode
import jwt
import uuid
import io

@app.route('/generate_qr', methods=['GET'])
def generate_qr():
    session_id = str(uuid.uuid4())
    token = generate_jwt("", session_id)  # User ID is initially empty
    token_url = url_for('qr_login', token=token, _external=True)
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(token_url)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    buf = io.BytesIO()
    img.save(buf)
    buf.seek(0)
    return send_file(buf, mimetype='image/png')


@app.route('/qr_login/<token>/<int:user_id>', methods=['GET'])
def qr_login(token, user_id):
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        session_id = payload['purchase_id']  # Assuming session_id is stored in purchase_id for this example
        
        # Create a purchase for the user
        purchase_id = create_purchase(user_id)
        
        # Generate a new JWT token for the session with the user_id
        user_token = generate_jwt(user_id, purchase_id)
        
        # Set the user_id in the session to log in the user
        session['user_id'] = user_id
        
        # Redirect to the homepage or dashboard after login
        return redirect(url_for('dashboard', token=user_token))
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'QR code has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid QR code'}), 401







@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.commit()
    db.session.remove()


if __name__ == '__main__':
    # execute_sql_file('IntelliCart.sql')
    app.run(debug=True)

