import psycopg2

conn = psycopg2.connect(dbname="postgres", user="postgres", password="postgres", host="localhost")
conn.autocommit = True
cur = conn.cursor()
cur.execute("SELECT 1 FROM pg_database WHERE datname='darkatlas_test'")
if not cur.fetchone():
    cur.execute("CREATE DATABASE darkatlas_test")
    print("Created darkatlas_test database.")
else:
    print("darkatlas_test already exists.")
conn.close()
