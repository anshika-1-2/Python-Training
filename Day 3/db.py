import psycopg2

def connect_db():
    """Connect to the PostgreSQL database server."""
    conn = None
    try:
        # Define connection parameters
        conn = psycopg2.connect(
            host="localhost",          
            database="sample_db",    
            user="postgres",   
            password="anshi",  
            port="5432"                
        )
        print("Connected to the PostgreSQL database successfully!")
        return conn

    except (psycopg2.DatabaseError, Exception) as error:
        print(f"Error connecting to the database: {error}")
        if conn:
            conn.close()
        return None

if __name__ == '__main__':
    connection = connect_db()
    if connection:
        connection.close()
        print("Database connection closed.")



def execute_query(connection, query):
    """Execute an SQL query and fetch all results if applicable."""
    if connection is None:
        return

    cursor = connection.cursor()
    try:
        cursor.execute(query)
        # If the query is a SELECT statement, retrieve the results
        if query.strip().upper().startswith("SELECT"):
            records = cursor.fetchall()
            return records
        # If the query is an INSERT, UPDATE, or DELETE, commit changes
        else:
            connection.commit()
            print("Query executed and changes committed.")

    except (psycopg2.DatabaseError, Exception) as error:
        print(f"Error executing query: {error}")
        connection.rollback() # Rollback the transaction on error

    finally:
        cursor.close()

if __name__ == '__main__':
    connection = connect_db()
    if connection:
        # Example SELECT query
        data = execute_query(connection, "SELECT * FROM products;")
        if data:
            print("Data from database:")
            for row in data:
                print(row)

        # Example INSERT query (assuming 'products' exists with appropriate columns)
        # execute_query(connection, "INSERT INTO products (name, price) VALUES ('Product Name', 99.99);")

        connection.close()
        print("Database connection closed.")
