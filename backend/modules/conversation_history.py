# Conversation_history.py

import psycopg2
import pandas as pd
from datetime import datetime
from modules.db_connect import connect_to_history_postgres

# ---------------------------------------
# Create the Table if it doesn't exist
# ---------------------------------------
def create_conversation_history_table(conn):
    try:
        cursor = conn.cursor()
        print("[DEBUG] Creating conversation_history table...")
        cursor.execute(""" 
            CREATE TABLE IF NOT EXISTS public.conversation_history (
                id SERIAL PRIMARY KEY,
                user_question TEXT,
                sql_query TEXT,
                query_result TEXT,
                summary TEXT,
                followup_questions TEXT,
                execution_time FLOAT,
                timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        print("[INFO] Table created successfully or already exists.")
    except Exception as e:
        print("[ERROR] Failed to create table:", e)
        conn.rollback()


# ---------------------------------------
# Store Conversation History
# ---------------------------------------
def store_conversation_history(conn, question, sql_query, result_df, summary=None, followup_questions=None, execution_time=None):
    try:
        cursor = conn.cursor()
        print("[DEBUG] Inserting conversation history...")

        insert_query = """
        INSERT INTO public.conversation_history 
        (user_question, sql_query, query_result, summary, followup_questions, execution_time, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        result_str = result_df.to_csv(index=False) if not result_df.empty else "No results"
        followup_str = "\n".join(followup_questions) if isinstance(followup_questions, list) else (followup_questions or "None")
        timestamp = datetime.now()

        cursor.execute(insert_query, (question, sql_query, result_str, summary or "", followup_str, execution_time, timestamp))
        conn.commit()
        print("[INFO] Conversation stored successfully into PostgreSQL!")
        cursor.close()
    except Exception as e:
        print("[ERROR] Storing conversation history failed:", e)
        conn.rollback()


# ---------------------------------------
# Retrieve Conversation History
# ---------------------------------------
def get_conversation_history(conn):
    try:
        query = "SELECT * FROM public.conversation_history ORDER BY timestamp DESC LIMIT 10;"
        df = pd.read_sql(query, conn)

        # Add formatted time column for display
        df["asked_at"] = pd.to_datetime(df["timestamp"]).dt.strftime("%Y-%m-%d %H:%M:%S")
        
        return df
    except Exception as e:
        print(f"[ERROR] Failed to retrieve conversation history: {e}")
        return pd.DataFrame()