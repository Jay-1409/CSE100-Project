import re
from flask import Flask, render_template, request, redirect, url_for
import csv

app = Flask(__name__)

# Function to validate password strength
def validate_password(password):
    # Check if password contains at least one uppercase letter, one digit, and one special character
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."
    elif not re.search(r"\d", password):
        return False, "Password must contain at least one digit."
    elif not re.search(r"[!@#$%^&*()\-_=+{};:,<.>]", password):
        return False, "Password must contain at least one special character."
    else:
        return True, "Password is valid."
    pass

# Function to sign up users and save data to CSV file
def sign_up(username, password, email, phone_no, age):
    with open('users.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, password, email, phone_no, age])

# Function to check if login credentials are valid
def login(username, password):
    try:
        with open('users.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == username and row[1] == password:
                    return True
                return False
    except FileNotFoundError:
        return False
    except Exception as e:
        return False


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        phone_no = request.form['phone_no']
        age = request.form['age']
        
        # Validate password
        is_valid, message = validate_password(password)
        if not is_valid:
            return render_template('signup.html', message=message)
        
        # Call the sign_up function with form data
        sign_up(username, password, email, phone_no, age)
        return redirect(url_for('index'))  # Redirect to the index page after sign up
    else:
        return render_template('signup.html')

@app.route('/login', methods=['POST'])
def user_login():
    username = request.form['username']
    password = request.form['password']
    
    # Check if login credentials are valid
    if login(username, password):
        return render_template('/home.html') # Redirect to the index page after login
    else:
        return render_template('/login.html', message='Incorrect username or password.')

if __name__ == '__main__':
    app.run(debug=True)

