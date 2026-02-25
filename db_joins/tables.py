
# import psycopg2
# import random
# from faker import Faker
# from datetime import datetime
# import pytz

# IST = pytz.timezone("Asia/Kolkata")

# def ist_timestamp_str():
#     """
#     Returns IST datetime as clean string
#     Example: '2026-02-09 19:25:10'
#     """
#     return datetime.now(IST).strftime("%Y-%m-%d %H:%M:%S").strip()

# # -------------------------------
# # DB CONNECTION
# # -------------------------------
# fake = Faker()

# conn = psycopg2.connect(
#     dbname="Joins",
#     user="postgres",
#     password="anshi",
#     host="localhost",
#     port="5432"
# )
# cur = conn.cursor()

# # -------------------------------
# # CREATE TABLES + TIMESTAMPS
# # -------------------------------
# def create_tables():
#     cur.execute("""
#     CREATE TABLE IF NOT EXISTS users (
#         user_id SERIAL PRIMARY KEY,
#         username VARCHAR(50) UNIQUE NOT NULL,
#         password VARCHAR(255) NOT NULL,
#         role VARCHAR(10),
#         created_at VARCHAR(30),
#         updated_at VARCHAR(30)
#     );

#     CREATE TABLE IF NOT EXISTS audit_logs (
#         log_id SERIAL PRIMARY KEY,
#         username VARCHAR(50),
#         role VARCHAR(10),
#         action TEXT,
#         created_at VARCHAR(30),
#         updated_at VARCHAR(30)
#     );

#     CREATE TABLE IF NOT EXISTS customers (
#         customer_id SERIAL PRIMARY KEY,
#         name VARCHAR(100),
#         email VARCHAR(100) UNIQUE,
#         created_at VARCHAR(30),
#         updated_at VARCHAR(30)
#     );

#     CREATE TABLE IF NOT EXISTS orders (
#         order_id SERIAL PRIMARY KEY,
#         customer_id INT REFERENCES customers(customer_id),
#         order_date DATE,
#         amount NUMERIC(10,2),
#         created_at VARCHAR(30),
#         updated_at VARCHAR(30)
#     );

#     CREATE TABLE IF NOT EXISTS payments (
#         payment_id SERIAL PRIMARY KEY,
#         customer_id INT REFERENCES customers(customer_id),
#         payment_date DATE,
#         payment_mode VARCHAR(50),
#         created_at VARCHAR(30),
#         updated_at VARCHAR(30)
#     );

#     CREATE TABLE IF NOT EXISTS addresses (
#         address_id SERIAL PRIMARY KEY,
#         customer_id INT REFERENCES customers(customer_id),
#         city VARCHAR(50),
#         state VARCHAR(50),
#         country VARCHAR(50),
#         created_at VARCHAR(30),
#         updated_at VARCHAR(30)
#     );

#     CREATE TABLE IF NOT EXISTS support_tickets (
#         ticket_id SERIAL PRIMARY KEY,
#         customer_id INT REFERENCES customers(customer_id),
#         issue VARCHAR(200),
#         ticket_status VARCHAR(50),
#         created_at VARCHAR(30),
#         updated_at VARCHAR(30)
#     );

#     CREATE TABLE IF NOT EXISTS subscriptions (
#         subscription_id SERIAL PRIMARY KEY,
#         customer_id INT REFERENCES customers(customer_id),
#         plan VARCHAR(50),
#         start_date DATE,
#         created_at VARCHAR(30),
#         updated_at VARCHAR(30)
#     );

#     CREATE TABLE IF NOT EXISTS reviews (
#         review_id SERIAL PRIMARY KEY,
#         customer_id INT REFERENCES customers(customer_id),
#         rating INT CHECK (rating BETWEEN 1 AND 5),
#         comments VARCHAR(200),
#         created_at VARCHAR(30),
#         updated_at VARCHAR(30)
#     );
#     """)
    
    
#     conn.commit()

#     # Attach triggers
#     tables = [
#         "users", "audit_logs", "customers", "orders", "payments",
#         "addresses", "support_tickets", "subscriptions", "reviews"
#     ]

#     for table in tables:
#         cur.execute(f"""
#         DROP TRIGGER IF EXISTS trg_{table}_updated ON {table};
#         CREATE TRIGGER trg_{table}_updated
#         BEFORE UPDATE ON {table}
#         FOR EACH ROW
#         EXECUTE FUNCTION update_timestamp();
#         """)

#     conn.commit()

# # -------------------------------
# # AUDIT LOG
# # -------------------------------
# def log_action(username, role, action):
#     cur.execute("""
#         INSERT INTO audit_logs (username, role, action)
#         VALUES (%s, %s, %s)
#     """, (username, role, action))
#     conn.commit()

# -------------------------------
# AUTH
# -------------------------------
# def create_user(username, password, role, creator):
#     cur.execute("""
#         INSERT INTO users (username, password, role)
#         VALUES (%s, %s, %s)
#     """, (username, password, role))
#     conn.commit()
#     log_action(creator["username"], creator["role"], f"CREATE_USER:{username}")

# def login(username, password):
#     cur.execute("""
#         SELECT user_id, username, role
#         FROM users WHERE username=%s AND password=%s
#     """, (username, password))
#     user = cur.fetchone()
#     if user:
#         log_action(username, user[2], "LOGIN")
#     return user

# # -------------------------------
# # INSERT RANDOM DATA (ADMIN)
# # -------------------------------
# def insert_random_data(n, user):
#     for _ in range(n):
#         cur.execute("""
#             INSERT INTO customers (name, email)
#             VALUES (%s, %s)
#         """, (fake.name(), fake.unique.email()))
#     conn.commit()
#     log_action(user["username"], user["role"], "INSERT_RANDOM_DATA")

# # -------------------------------
# # MAIN
# # -------------------------------
# def main():
#     create_tables()

#     username = input("Username: ")
#     password = input("Password: ")

#     data = login(username, password)
#     if not data:
#         print("Invalid login")
#         return

#     user = {"id": data[0], "username": data[1], "role": data[2]}
#     print(f"Logged in as {user['role']}")

#     if user["role"] == "ADMIN":
#         print("1. Create User\n2. Insert Random Data\n3. View Audit Logs")
#         choice = input("Choose: ")

#         if choice == "1":
#             u = input("Username: ")
#             p = input("Password: ")
#             r = input("Role (ADMIN/USER): ").upper()
#             create_user(u, p, r, user)

#         elif choice == "2":
#             n = int(input("Records: "))
#             insert_random_data(n, user)

#         elif choice == "3":
#             cur.execute("SELECT * FROM audit_logs ORDER BY created_at DESC")
#             for row in cur.fetchall():
#                 print(row)

# # -------------------------------
# # RUN
# # -------------------------------
# if __name__ == "__main__":
#     main()
#     cur.close()
#     conn.close()


import psycopg2
import random
from faker import Faker
from datetime import datetime
import pytz

# =========================================
# CONFIG
# =========================================
fake = Faker()
IST = pytz.timezone("Asia/Kolkata")

conn = psycopg2.connect(
    dbname="Joins",
    user="postgres",
    password="anshi",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# =========================================
# TIMESTAMP UTILITY (STRING + STRIP)
# =========================================
def ist_now_str():
    return datetime.now(IST).strftime("%Y-%m-%d %H:%M:%S").strip()

# =========================================
# CREATE TABLES
# =========================================
def create_tables():
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE,
        password VARCHAR(255),
        role VARCHAR(10),
        created_at VARCHAR(30),
        updated_at VARCHAR(30),
        is_deleted BOOLEAN DEFAULT FALSE
    );

    CREATE TABLE IF NOT EXISTS audit_logs (
        log_id SERIAL PRIMARY KEY,
        username VARCHAR(50),
        role VARCHAR(10),
        action TEXT,
        created_at VARCHAR(30),
        updated_at VARCHAR(30)
    );

    CREATE TABLE IF NOT EXISTS customers (
        customer_id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        email VARCHAR(100) UNIQUE,
        created_at VARCHAR(30),
        updated_at VARCHAR(30),
        is_deleted BOOLEAN DEFAULT FALSE
    );

    CREATE TABLE IF NOT EXISTS orders (
        order_id SERIAL PRIMARY KEY,
        customer_id INT REFERENCES customers(customer_id),
        order_date DATE,
        amount NUMERIC(10,2),
        created_at VARCHAR(30),
        updated_at VARCHAR(30),
        is_deleted BOOLEAN DEFAULT FALSE
    );

    CREATE TABLE IF NOT EXISTS payments (
        payment_id SERIAL PRIMARY KEY,
        customer_id INT REFERENCES customers(customer_id),
        payment_date DATE,
        payment_mode VARCHAR(50),
        created_at VARCHAR(30),
        updated_at VARCHAR(30),
        is_deleted BOOLEAN DEFAULT FALSE
    );

    CREATE TABLE IF NOT EXISTS addresses (
        address_id SERIAL PRIMARY KEY,
        customer_id INT REFERENCES customers(customer_id),
        city VARCHAR(50),
        state VARCHAR(50),
        country VARCHAR(50),
        created_at VARCHAR(30),
        updated_at VARCHAR(30),
        is_deleted BOOLEAN DEFAULT FALSE
    );

    CREATE TABLE IF NOT EXISTS support_tickets (
        ticket_id SERIAL PRIMARY KEY,
        customer_id INT REFERENCES customers(customer_id),
        issue VARCHAR(200),
        ticket_status VARCHAR(50),
        created_at VARCHAR(30),
        updated_at VARCHAR(30),
        is_deleted BOOLEAN DEFAULT FALSE
    );

    CREATE TABLE IF NOT EXISTS subscriptions (
        subscription_id SERIAL PRIMARY KEY,
        customer_id INT REFERENCES customers(customer_id),
        plan VARCHAR(50),
        start_date DATE,
        created_at VARCHAR(30),
        updated_at VARCHAR(30),
        is_deleted BOOLEAN DEFAULT FALSE
    );

    CREATE TABLE IF NOT EXISTS reviews (
        review_id SERIAL PRIMARY KEY,
        customer_id INT REFERENCES customers(customer_id),
        rating INT CHECK (rating BETWEEN 1 AND 5),
        comments VARCHAR(200),
        created_at VARCHAR(30),
        updated_at VARCHAR(30),
        is_deleted BOOLEAN DEFAULT FALSE
    );
    """)
    conn.commit()

# =========================================
# AUDIT LOGGING
# =========================================
def log_action(username, role, action):
    ts = ist_now_str()
    cur.execute("""
        INSERT INTO audit_logs
        (username, role, action, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s)
    """, (username, role, action, ts, ts))
    conn.commit()

# =========================================
# AUTH
# =========================================
def create_user(username, password, role, creator):
    ts = ist_now_str()
    cur.execute("""
        INSERT INTO users
        (username, password, role, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s)
    """, (username, password, role, ts, ts))
    conn.commit()
    log_action(creator["username"], creator["role"], f"CREATE_USER:{username}")

def login(username, password):
    cur.execute("""
        SELECT user_id, username, role
        FROM users
        WHERE username=%s AND password=%s AND is_deleted=FALSE
    """, (username, password))
    user = cur.fetchone()
    if user:
        log_action(username, user[2], "LOGIN")
    return user

# =========================================
# INSERT RANDOM DATA (ADMIN)
# =========================================
def insert_random_data(n, user):
    ts = ist_now_str()
    customer_ids = []

    for _ in range(n):
        cur.execute("""
            INSERT INTO customers
            (name, email, created_at, updated_at, is_deleted)
            VALUES (%s, %s, %s, %s, FALSE)
            RETURNING customer_id
        """, (fake.name(), fake.unique.email(), ts, ts))
        customer_ids.append(cur.fetchone()[0])

    for _ in range(n):
        cid = random.choice(customer_ids)

        cur.execute("""
            INSERT INTO orders
            (customer_id, order_date, amount, created_at, updated_at, is_deleted)
            VALUES (%s, %s, %s, %s, %s, FALSE)
        """, (cid, fake.date_between('-1y','today'),
              round(random.uniform(100,5000),2), ts, ts))

        cur.execute("""
            INSERT INTO payments
            (customer_id, payment_date, payment_mode, created_at, updated_at, is_deleted)
            VALUES (%s, %s, %s, %s, %s, FALSE)
        """, (cid, fake.date_between('-1y','today'),
              random.choice(["UPI","Card","Cash"]), ts, ts))

        cur.execute("""
            INSERT INTO addresses
            (customer_id, city, state, country, created_at, updated_at, is_deleted)
            VALUES (%s, %s, %s, %s, %s, %s, FALSE)
        """, (cid, fake.city(), fake.state(),
              fake.country(), ts, ts))

        cur.execute("""
            INSERT INTO support_tickets
            (customer_id, issue, ticket_status, created_at, updated_at, is_deleted)
            VALUES (%s, %s, %s, %s, %s, FALSE)
        """, (cid, fake.sentence(6),
              random.choice(["Open","Closed"]), ts, ts))

        cur.execute("""
            INSERT INTO subscriptions
            (customer_id, plan, start_date, created_at, updated_at, is_deleted)
            VALUES (%s, %s, %s, %s, %s, FALSE)
        """, (cid, random.choice(["Free","Basic","Premium"]),
              fake.date_between('-2y','today'), ts, ts))

        cur.execute("""
            INSERT INTO reviews
            (customer_id, rating, comments, created_at, updated_at, is_deleted)
            VALUES (%s, %s, %s, %s, %s, FALSE)
        """, (cid, random.randint(1,5),
              fake.sentence(8), ts, ts))

    conn.commit()
    log_action(user["username"], user["role"], "INSERT_RANDOM_DATA")

# =========================================
# SOFT DELETE (ADMIN)
# =========================================
def soft_delete_record(table, id_col, record_id, user):
    if user["role"] != "ADMIN":
        print("❌ Only ADMIN can delete")
        return

    cur.execute(f"""
        UPDATE {table}
        SET is_deleted=TRUE, updated_at=%s
        WHERE {id_col}=%s
    """, (ist_now_str(), record_id))
    conn.commit()
    log_action(user["username"], user["role"], f"SOFT_DELETE:{table}:{record_id}")

# =========================================
# ENTER QUERY (ROLE BASED)
# =========================================
def enter_query(user):
    query = input("Enter SQL query: ").strip()
    qtype = query.split()[0].upper()

    if user["role"] == "USER" and qtype != "SELECT":
        print("❌ USERS can only run SELECT queries")
        log_action(user["username"], user["role"], f"BLOCKED_QUERY:{query}")
        return

    try:
        cur.execute(query)
        if qtype == "SELECT":
            for row in cur.fetchall():
                print(row)
        else:
            conn.commit()
        log_action(user["username"], user["role"], f"EXECUTED_QUERY:{query}")
    except Exception as e:
        conn.rollback()
        print("❌ Error:", e)
        log_action(user["username"], user["role"], f"FAILED_QUERY:{query}")

# =========================================
# VIEW AUDIT LOGS
# =========================================
def view_audit_logs():
    cur.execute("SELECT * FROM audit_logs ORDER BY created_at DESC")
    for row in cur.fetchall():
        print(row)

# =========================================
# MAIN
# =========================================
def main():
    create_tables()

    username = input("Username: ")
    password = input("Password: ")

    data = login(username, password)
    if not data:
        print("❌ Invalid login")
        return

    user = {"id": data[0], "username": data[1], "role": data[2]}
    print(f"\nLogged in as {user['role']}")

    if user["role"] == "ADMIN":
        print("""
1. Create User
2. Insert Random Data
3. View Audit Logs
4. Enter Your Query
""")
        ch = input("Choose: ")

        if ch == "1":
            u = input("Username: ")
            p = input("Password: ")
            r = input("Role (ADMIN/USER): ").upper()
            create_user(u, p, r, user)

        elif ch == "2":
            n = int(input("Records per table: "))
            insert_random_data(n, user)

        elif ch == "3":
            view_audit_logs()

        elif ch == "4":
            enter_query(user)

    else:
        print("\n1. Enter Your Query (SELECT only)")
        if input("Choose: ") == "1":
            enter_query(user)

# =========================================
# RUN
# =========================================
if __name__ == "__main__":
    main()
    cur.close()
    conn.close()
