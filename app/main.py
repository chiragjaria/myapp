from fastapi import FastAPI
import psycopg2
import os
import logging
from datetime import datetime

# Timestamped logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

app = FastAPI()

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

@app.get("/")
def health_check():
    logger.info("Health check called")
    return {"status": "ok", "version": "v2"}

@app.get("/create-table/{table_name}")        # ← table name in URL
def create_table(table_name: str):
    logger.info(f"Request received to create table: {table_name}")
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        cur = conn.cursor()
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                created_at TIMESTAMP DEFAULT NOW()
            );
        """)
        conn.commit()
        cur.close()
        conn.close()
        logger.info(f"Table '{table_name}' created successfully at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        return {
            "message": f"Table '{table_name}' created successfully",
            "table_name": table_name,
            "version": "v2",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    except Exception as e:
        logger.error(f"Failed to create table '{table_name}': {str(e)}")
        return {"error": str(e)}
