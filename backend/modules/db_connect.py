# import psycopg2
# import snowflake.connector
# from config import settings

# # Connect to PostgreSQL
# def connect_to_postgres(allow_llm_to_see_data=True):
#     return psycopg2.connect(
#         host=settings.POSTGRES_HOST,
#         dbname=settings.POSTGRES_DB,
#         user=settings.POSTGRES_USER,
#         password=settings.POSTGRES_PASSWORD,
#         port=settings.POSTGRES_PORT
#     )

# # Connect to Snowflake
# def connect_to_snowflake(allow_llm_to_see_data=True):
#     return snowflake.connector.connect(
#         account=settings.SNOWFLAKE_ACCOUNT,
#         user=settings.SNOWFLAKE_USER,
#         password=settings.SNOWFLAKE_PASSWORD,
#         database=settings.SNOWFLAKE_DATABASE,
#         schema=settings.SNOWFLAKE_SCHEMA
#     )

# # Connect to PostgreSQL for History Logging
# def connect_to_history_postgres():
#     print("[DEBUG] Connecting to History DB:", settings.PG_DB)
#     try:
#         conn = psycopg2.connect(
#             host=settings.PG_HOST,
#             database=settings.PG_DB,
#             user=settings.PG_USER,
#             password=settings.PG_PASSWORD,
#             port=settings.PG_PORT
#         )
#         print("[DEBUG] Connected successfully to", settings.PG_DB)
#         return conn
#     except Exception as e:
#         print("[ERROR] Failed to connect to History DB:", e)
#         return None
    
# def get_postgres_tables():
#     try:
#         conn = connect_to_postgres()
#         cur = conn.cursor()
#         cur.execute("""
#             SELECT table_name 
#             FROM information_schema.tables 
#             WHERE table_schema = 'public' AND table_type='BASE TABLE';
#         """)
#         tables = [row[0] for row in cur.fetchall()]
#         cur.close()
#         conn.close()
#         return tables
#     except Exception as e:
#         print(f"Error fetching PostgreSQL tables: {e}")
#         return []

# def get_snowflake_tables():
#     try:
#         ctx = connect_to_snowflake()
#         cs = ctx.cursor()
#         cs.execute("SHOW TABLES")
#         tables = [row[1] for row in cs.fetchall()]  # row[1] = table_name
#         cs.close()
#         ctx.close()
#         return tables
#     except Exception as e:
#         print(f"Error fetching Snowflake tables: {e}")
#         return []


import psycopg2
import snowflake.connector
from config import settings
from exceptions.custom import DatabaseConnectionException, DataNotFoundException

# Connect to PostgreSQL
def connect_to_postgres(allow_llm_to_see_data=True):
    try:
        return psycopg2.connect(
            host=settings.POSTGRES_HOST,
            dbname=settings.POSTGRES_DB,
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            port=settings.POSTGRES_PORT
        )
    except Exception as e:
        raise DatabaseConnectionException(f"Failed to connect to PostgreSQL: {str(e)}")

# Connect to Snowflake
def connect_to_snowflake(allow_llm_to_see_data=True):
    try:
        return snowflake.connector.connect(
            account=settings.SNOWFLAKE_ACCOUNT,
            user=settings.SNOWFLAKE_USER,
            password=settings.SNOWFLAKE_PASSWORD,
            database=settings.SNOWFLAKE_DATABASE,
            schema=settings.SNOWFLAKE_SCHEMA
        )
    except Exception as e:
        raise DatabaseConnectionException(f"Failed to connect to Snowflake: {str(e)}")

# Connect to PostgreSQL for History Logging
def connect_to_history_postgres():
    print("[DEBUG] Connecting to History DB:", settings.PG_DB)
    try:
        conn = psycopg2.connect(
            host=settings.PG_HOST,
            database=settings.PG_DB,
            user=settings.PG_USER,
            password=settings.PG_PASSWORD,
            port=settings.PG_PORT
        )
        print("[DEBUG] Connected successfully to", settings.PG_DB)
        return conn
    except Exception as e:
        raise DatabaseConnectionException(f"Failed to connect to History PostgreSQL DB: {str(e)}")

# Fetch table names from PostgreSQL
def get_postgres_tables():
    try:
        conn = connect_to_postgres()
        cur = conn.cursor()
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_type='BASE TABLE';
        """)
        tables = [row[0] for row in cur.fetchall()]
        cur.close()
        conn.close()

        if not tables:
            raise DataNotFoundException("No PostgreSQL tables found.")
        return tables
    except (DatabaseConnectionException, DataNotFoundException):
        raise
    except Exception as e:
        raise DataNotFoundException(f"Error fetching PostgreSQL tables: {str(e)}")

# Fetch table names from Snowflake
def get_snowflake_tables():
    try:
        ctx = connect_to_snowflake()
        cs = ctx.cursor()
        cs.execute("SHOW TABLES")
        tables = [row[1] for row in cs.fetchall()]  # row[1] = table_name
        cs.close()
        ctx.close()

        if not tables:
            raise DataNotFoundException("No Snowflake tables found.")
        return tables
    except (DatabaseConnectionException, DataNotFoundException):
        raise
    except Exception as e:
        raise DataNotFoundException(f"Error fetching Snowflake tables: {str(e)}")
