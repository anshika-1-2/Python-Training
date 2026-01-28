import psycopg2
import random
from faker import Faker

fake = Faker()
conn = psycopg2.connect(
    dbname="Joins",
    user="postgres",
    password="anshi",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

# -------------------------------
# Create tables
# -------------------------------
def create_tables(cur):
    create_tables_sql = """
    CREATE TABLE IF NOT EXISTS customers (
        customer_id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL
    );

    CREATE TABLE IF NOT EXISTS orders (
        order_id SERIAL PRIMARY KEY,
        customer_id INT NOT NULL,
        order_date DATE,
        amount NUMERIC(10,2),
        CONSTRAINT fk_customer_orders
            FOREIGN KEY (customer_id)
            REFERENCES customers(customer_id)
            ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS payments (
        payment_id SERIAL PRIMARY KEY,
        customer_id INT NOT NULL,
        payment_date DATE,
        payment_mode VARCHAR(50),
        CONSTRAINT fk_customer_payments
            FOREIGN KEY (customer_id)
            REFERENCES customers(customer_id)
            ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS addresses (
        address_id SERIAL PRIMARY KEY,
        customer_id INT NOT NULL,
        city VARCHAR(50),
        state VARCHAR(50),
        country VARCHAR(50),
        CONSTRAINT fk_customer_addresses
            FOREIGN KEY (customer_id)
            REFERENCES customers(customer_id)
            ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS support_tickets (
        ticket_id SERIAL PRIMARY KEY,
        customer_id INT NOT NULL,
        issue VARCHAR(200),
        ticket_status VARCHAR(50),
        CONSTRAINT fk_customer_tickets
            FOREIGN KEY (customer_id)
            REFERENCES customers(customer_id)
            ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS subscriptions (
        subscription_id SERIAL PRIMARY KEY,
        customer_id INT NOT NULL,
        plan VARCHAR(50),
        start_date DATE,
        CONSTRAINT fk_customer_subscriptions
            FOREIGN KEY (customer_id)
            REFERENCES customers(customer_id)
            ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS reviews (
        review_id SERIAL PRIMARY KEY,
        customer_id INT NOT NULL,
        rating INT CHECK (rating BETWEEN 1 AND 5),
        comments VARCHAR(200),
        CONSTRAINT fk_customer_reviews
            FOREIGN KEY (customer_id)
            REFERENCES customers(customer_id)
            ON DELETE CASCADE
    );
    """
create_tables(cur)
conn.commit()

# -------------------------------
# Insert Random Data Function
# -------------------------------
def insert_random_data(n):
    """
    Insert random data into the tables.

    Args:
        n (int): The number of records to insert into each table.

    Returns:
        None
    """
    customer_ids = []

    # ---- Customers ----
    for _ in range(n):
        cur.execute("""
            INSERT INTO customers (name, email)
            VALUES (%s, %s)
            RETURNING customer_id;
        """, (fake.name(), fake.unique.email()))
        customer_ids.append(cur.fetchone()[0])

    # ---- Orders ----
    for _ in range(n):
        cur.execute("""
            INSERT INTO orders (customer_id, order_date, amount)
            VALUES (%s, %s, %s);
        """, (
            random.choice(customer_ids),
            fake.date_between(start_date='-1y', end_date='today'),
            round(random.uniform(100, 5000), 2)
        ))

    # ---- Payments ----
    for _ in range(n):
        cur.execute("""
            INSERT INTO payments (customer_id, payment_date, payment_mode)
            VALUES (%s, %s, %s);
        """, (
            random.choice(customer_ids),
            fake.date_between(start_date='-1y', end_date='today'),
            random.choice(["UPI", "Credit Card", "Debit Card", "Net Banking", "Cash"])
        ))

    # ---- Addresses ----
    for _ in range(n):
        cur.execute("""
            INSERT INTO addresses (customer_id, city, state, country)
            VALUES (%s, %s, %s, %s);
        """, (
            random.choice(customer_ids),
            fake.city(),
            fake.state(),
            fake.country()
        ))

    # ---- Support Tickets ----
    for _ in range(n):
        cur.execute("""
            INSERT INTO support_tickets (customer_id, issue, ticket_status)
            VALUES (%s, %s, %s);
        """, (
            random.choice(customer_ids),
            fake.sentence(nb_words=6),
            random.choice(["Open", "In Progress", "Resolved", "Closed"])
        ))

    # ---- Subscriptions ----
    for _ in range(n):
        cur.execute("""
            INSERT INTO subscriptions (customer_id, plan, start_date)
            VALUES (%s, %s, %s);
        """, (
            random.choice(customer_ids),
            random.choice(["Free", "Basic", "Premium", "Enterprise"]),
            fake.date_between(start_date='-2y', end_date='today')
        ))

    # ---- Reviews ----
    for _ in range(n):
        cur.execute("""
            INSERT INTO reviews (customer_id, rating, comments)
            VALUES (%s, %s, %s);
        """, (
            random.choice(customer_ids),
            random.randint(1, 5),
            fake.sentence(nb_words=8)
        ))

    conn.commit()
    print(f"✅ Successfully inserted {n} records into each table.")

if __name__ == "__main__":
    n = int(input("Enter number of records to insert per table: "))
    insert_random_data(n)

cur.close()
conn.close()
