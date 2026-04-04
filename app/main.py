from fastapi import FastAPI
import psycopg2
import os

app = FastAPI()

DB_HOST = os.getenv("phost")
DB_NAME = os.getenv("pdb")
DB_USER = os.getenv("puser")
DB_PASS = os.getenv("ppassword")

@app.get("/")
def health_check():
    return {"status": "ok"}

@app.get("/create-table")
def create_table():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS test_table (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100)
        );
    """)
    conn.commit()
    cur.close()
    conn.close()
    return {"message": "Table created successfully"}
