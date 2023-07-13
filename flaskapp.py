from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="AAav@7978",
    database="registration_app"  # Specify the database name
)

# Create the table if it doesn't exist
cursor = db.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        phone VARCHAR(15) NOT NULL,
        address VARCHAR(255) NOT NULL,
        city VARCHAR(100) NOT NULL,
        country VARCHAR(100) NOT NULL
    )
""")
db.commit()

# Routes
@app.route('/')
def index():
    try:
        # Retrieve all users from the database
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        print(users)  # Added print statement to check fetched user data
        return render_template('index.html', users=users)
    except Exception as e:
        print("Error retrieving users:", str(e))
        return "An error occurred while retrieving users."


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Extract values from the registration form
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        city = request.form['city']
        country = request.form['country']

        # Insert the user data into the database
        cursor = db.cursor()
        query = "INSERT INTO users (name, email, phone, address, city, country) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (name, email, phone, address, city, country)
        cursor.execute(query, values)
        db.commit()

        # Redirect to the home page
        return redirect('/')
    return render_template('registerdbms.html')

@app.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit(user_id):
    if request.method == 'POST':
        # Extract values from the edit form
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        city = request.form['city']
        country = request.form['country']

        # Update the user data in the database
        cursor = db.cursor()
        query = "UPDATE users SET name=%s, email=%s, phone=%s, address=%s, city=%s, country=%s WHERE id=%s"
        values = (name, email, phone, address, city, country, user_id)
        cursor.execute(query, values)
        db.commit()

        # Redirect to the home page
        return redirect('/')
    else:
        # Fetch the user data from the database for pre-filling the edit form
        cursor = db.cursor()
        query = "SELECT * FROM users WHERE id = %s"
        values = (user_id,)
        cursor.execute(query, values)
        user = cursor.fetchone()
        return render_template('edit.html', user=user)

@app.route('/delete/<int:user_id>')
def delete(user_id):
    # Delete the user data from the database
    cursor = db.cursor()
    query = "DELETE FROM users WHERE id = %s"
    values = (user_id,)
    cursor.execute(query, values)
    db.commit()

    # Redirect to the home page
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
