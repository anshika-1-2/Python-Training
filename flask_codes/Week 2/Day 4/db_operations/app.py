from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)

# Connect to the database
conn = psycopg2.connect(database="flask_sample", 
                        user="postgres",
                        password="anshi", 
                        host="localhost", 
                        port="5432")

# create a cursor
cur = conn.cursor()

cur.execute(
    '''CREATE TABLE IF NOT EXISTS products (id serial \
    PRIMARY KEY, name varchar(100), price float);''')

# Insert some data into the table
cur.execute(
    '''INSERT INTO products (name, price) VALUES \
    ('Apple', 1.99), ('Orange', 0.99), ('Banana', 0.59);''')

# commit the changes
conn.commit()

# close the cursor and connection
cur.close()
conn.close()


@app.route('/')
def index():
    # Connect to the database
    """
    Renders the index.html template with all products from the products table.

    Connects to the database, creates a cursor, selects all products from the table,
    fetches the data, closes the cursor and connection, and renders the template with the
    data.

    Returns:
        str: The rendered template as a string.
    """
    conn = psycopg2.connect(database="flask_sample", 
                        user="postgres",
                        password="anshi", 
                        host="localhost", 
                        port="5432")

    # create a cursor
    cur = conn.cursor()

    # Select all products from the table
    cur.execute('''SELECT * FROM products''')

    # Fetch the data
    data = cur.fetchall()

    # close the cursor and connection
    cur.close()
    conn.close()

    return render_template('index.html', data=data)


@app.route('/create', methods=['POST'])
def create():
    """
    Handles POST requests to /create.

    Connects to the database, creates a cursor, gets the name and price from the form,
    inserts the data into the table, commits the changes, closes the cursor and connection,
    and redirects to the home page.

    Returns:
        str: The redirected URL as a string.
    """
    conn = psycopg2.connect(database="flask_sample", 
                        user="postgres",
                        password="anshi", 
                        host="localhost", 
                        port="5432")

    cur = conn.cursor()

    # Get the data from the form
    name = request.form['name']
    price = request.form['price']

    # Insert the data into the table
    cur.execute(
        '''INSERT INTO products \
        (name, price) VALUES (%s, %s)''',
        (name, price))

    # commit the changes
    conn.commit()

    # close the cursor and connection
    cur.close()
    conn.close()

    return redirect(url_for('index'))


@app.route('/update', methods=['POST'])
def update():
    """
    Handles POST requests to /update.

    Connects to the database, creates a cursor, gets the name, price, and id from the form,
    updates the data in the table, commits the changes, and redirects to the home page.

    Returns:
        str: The redirected URL as a string.
    """
    conn = psycopg2.connect(database="flask_sample", 
                        user="postgres",
                        password="anshi", 
                        host="localhost", 
                        port="5432")

    cur = conn.cursor()

    # Get the data from the form
    name = request.form['name']
    price = request.form['price']
    id = request.form['id']

    # Update the data in the table
    cur.execute(
        '''UPDATE products SET name=%s,\
        price=%s WHERE id=%s''', (name, price, id))

    # commit the changes
    conn.commit()
    return redirect(url_for('index'))


@app.route('/delete', methods=['POST'])
def delete():
    """
    Handles POST requests to /delete.

    Connects to the database, creates a cursor, gets the id from the form,
    deletes the data from the table, commits the changes, and redirects to the home page.

    Returns:
        str: The redirected URL as a string.
    """
    conn = psycopg2.connect(database="flask_sample", 
                        user="postgres",
                        password="anshi", 
                        host="localhost", 
                        port="5432")

    cur = conn.cursor()

    # Get the data from the form
    id = request.form['id']

    # Delete the data from the table
    cur.execute('''DELETE FROM products WHERE id=%s''', (id,))

    # commit the changes
    conn.commit()

    # close the cursor and connection
    cur.close()
    conn.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
      