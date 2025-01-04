from flask import Flask, render_template, request, g
import sqlite3
import os

app = Flask(__name__)

# Directory to your database files
DATABASES_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance')

# Function to dynamically select the database based on city
def get_db(city):
    if city.lower() == 'chicago':
        db_path = os.path.join(DATABASES_DIR, 'chicago.db')
    elif city.lower() == 'new york city':
        db_path = os.path.join(DATABASES_DIR, 'newyork.db')
    elif city.lower() == 'houston':
        db_path = os.path.join(DATABASES_DIR, 'houston.db')
    elif city.lower() == 'los angeles':
        db_path = os.path.join(DATABASES_DIR, 'los_angeles.db')
    elif city.lower() == 'phoenix':
        db_path = os.path.join(DATABASES_DIR, 'phoenix.db')
    elif city.lower() == 'philadelphia':
        db_path = os.path.join(DATABASES_DIR, 'philadelphia.db')
    else:
        db_path = None

    if db_path and os.path.exists(db_path):
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = sqlite3.connect(db_path)
            db.row_factory = sqlite3.Row  # Allows accessing columns by name
        return db
    return None

# Close the database connection when the request ends
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def home():
    return render_template('fooddonation.html')

@app.route('/register')
def register():
    return render_template('Register.html')  

@app.route('/donate')
def donate():
    return render_template('Donate.html')

# Route to handle the search by city
@app.route('/search', methods=['GET'])
def search():
    city = request.args.get('city')
    if not city:
        return render_template('search_results.html', results=None)

    # Get the database connection based on the city
    db = get_db(city)
    if db is None:
        return render_template('search_results.html', results=None)

    # Fetch results from the selected database
    cur = db.execute("SELECT * FROM FoodBanksRestaurants WHERE City = ?", (city,))
    results = cur.fetchall()

    return render_template('search_results.html', results=results)

# Additional pages, like About and Contact, if needed
@app.route('/about')
def about():
    return render_template('About.html')

@app.route('/contact')
def contact():
    return render_template('Contact.html')

if __name__ == '__main__':
    app.run(debug=True)
