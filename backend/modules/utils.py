# # utils.py
# import os, pickle, time
# from pathlib import Path
# from dotenv import load_dotenv
# import psycopg2, snowflake.connector

# load_dotenv()

# # ---------------------------------------------------------------------------
# # Internal in‑memory cache so the query runs only once per interpreter session
# # ---------------------------------------------------------------------------
# _memory_cache: dict[str, list[str]] = {}

# # ---------------------------------------------------------------------------
# # Helpers
# # ---------------------------------------------------------------------------
# def _cache_path(db_type: str) -> Path:
#     """Return the on‑disk cache file for this db_type."""
#     root = Path(__file__).with_suffix("")          # e.g., …/utils
#     return root.parent / f".keywords-{db_type.lower()}.pkl"

# def _write_cache(path: Path, keywords: list[str]) -> None:
#     path.write_bytes(pickle.dumps({"when": time.time(), "data": keywords}))

# def _read_cache(path: Path) -> list[str] | None:
#     try:
#         payload = pickle.loads(path.read_bytes())
#         return payload["data"]
#     except Exception:
#         return None

# # ---------------------------------------------------------------------------
# # Public API
# # ---------------------------------------------------------------------------
# def get_keywords_from_db(db_type: str) -> list[str]:
#     """
#     Return a list of lowercase table / column names for *db_type*.

#     * Runs the expensive INFORMATION_SCHEMA query only once:
#         1. checks the in‑process memory stash,
#         2. then the on‑disk pickle,
#         3. finally falls back to hitting the database.
#     """
#     # 1️⃣  already fetched during this Python run?
#     if db_type in _memory_cache:
#         return _memory_cache[db_type]

#     # 2️⃣  cached on disk?
#     disk_cache = _cache_path(db_type)
#     if disk_cache.exists():
#         cached = _read_cache(disk_cache)
#         if cached:                        # could be None if corrupted
#             _memory_cache[db_type] = cached
#             return cached

#     # 3️⃣  no cache → query the database **once**
#     keywords: set[str] = set()

#     if db_type == "PostgreSQL":
#         with psycopg2.connect(
#             host=os.getenv("POSTGRES_HOST"),
#             database=os.getenv("POSTGRES_DB"),
#             user=os.getenv("POSTGRES_USER"),
#             password=os.getenv("POSTGRES_PASSWORD"),
#         ) as conn, conn.cursor() as cur:
#             cur.execute("""
#                 SELECT table_name, column_name
#                 FROM information_schema.columns
#                 WHERE table_schema = 'public';
#             """)
#             keywords |= {item.lower() for row in cur for item in row}

#     elif db_type == "Snowflake":
#         with snowflake.connector.connect(
#             user=os.getenv("SNOWFLAKE_USER"),
#             password=os.getenv("SNOWFLAKE_PASSWORD"),
#             account=os.getenv("SNOWFLAKE_ACCOUNT"),
#             database=os.getenv("SNOWFLAKE_DATABASE"),
#             schema=os.getenv("SNOWFLAKE_SCHEMA"),
#         ) as conn, conn.cursor() as cur:
#             cur.execute("SELECT TABLE_NAME, COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS")
#             keywords |= {item.lower() for row in cur for item in row}

#     else:
#         raise ValueError(f"Unsupported db_type: {db_type}")

#     keywords_list = sorted(keywords)      # stable order is nice to have
#     _memory_cache[db_type] = keywords_list
#     _write_cache(disk_cache, keywords_list)
#     return keywords_list


import os
import pickle
import time
from pathlib import Path
from dotenv import load_dotenv
import psycopg2
import snowflake.connector

load_dotenv()

# Internal in-memory cache
_memory_cache: dict[str, list[str]] = {}

def _cache_path(db_type: str) -> Path:
    """Return the on-disk cache file path for this db_type."""
    root = Path(__file__).with_suffix("")  # e.g., …/utils
    return root.parent / f".keywords-{db_type.lower()}.pkl"

def _write_cache(path: Path, keywords: list[str]) -> None:
    """Write keyword list to a pickle file."""
    try:
        path.write_bytes(pickle.dumps({"when": time.time(), "data": keywords}))
    except Exception as e:
        print(f"[ERROR] Failed to write cache to {path}: {e}")

def _read_cache(path: Path) -> list[str] | None:
    """Read keyword list from a pickle file."""
    try:
        payload = pickle.loads(path.read_bytes())
        return payload.get("data")
    except Exception as e:
        print(f"[WARNING] Failed to read cache from {path}: {e}")
        return None

def get_keywords_from_db(db_type: str) -> list[str]:
    """
    Return a list of lowercase table and column names for the specified db_type.

    Caching order:
        1. In-memory
        2. On-disk (.pkl)
        3. Live DB query
    """
    try:
        # 1️⃣ In-memory cache
        if db_type in _memory_cache:
            return _memory_cache[db_type]

        # 2️⃣ On-disk cache
        disk_cache = _cache_path(db_type)
        if disk_cache.exists():
            cached = _read_cache(disk_cache)
            if cached:
                _memory_cache[db_type] = cached
                return cached

        # 3️⃣ Live DB query
        keywords: set[str] = set()

        if db_type == "PostgreSQL":
            try:
                with psycopg2.connect(
                    host=os.getenv("POSTGRES_HOST"),
                    database=os.getenv("POSTGRES_DB"),
                    user=os.getenv("POSTGRES_USER"),
                    password=os.getenv("POSTGRES_PASSWORD"),
                ) as conn, conn.cursor() as cur:
                    cur.execute("""
                        SELECT table_name, column_name
                        FROM information_schema.columns
                        WHERE table_schema = 'public';
                    """)
                    keywords |= {item.lower() for row in cur for item in row}
            except Exception as e:
                raise RuntimeError(f"[PostgreSQL] Failed to query schema: {e}")

        elif db_type == "Snowflake":
            try:
                with snowflake.connector.connect(
                    user=os.getenv("SNOWFLAKE_USER"),
                    password=os.getenv("SNOWFLAKE_PASSWORD"),
                    account=os.getenv("SNOWFLAKE_ACCOUNT"),
                    database=os.getenv("SNOWFLAKE_DATABASE"),
                    schema=os.getenv("SNOWFLAKE_SCHEMA"),
                ) as conn, conn.cursor() as cur:
                    cur.execute("SELECT TABLE_NAME, COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS")
                    keywords |= {item.lower() for row in cur for item in row}
            except Exception as e:
                raise RuntimeError(f"[Snowflake] Failed to query schema: {e}")

        else:
            raise ValueError(f"[ERROR] Unsupported db_type: {db_type}")

        keywords_list = sorted(keywords)
        _memory_cache[db_type] = keywords_list
        _write_cache(disk_cache, keywords_list)

        return keywords_list

    except Exception as e:
        print(f"[get_keywords_from_db] Failed for db_type '{db_type}': {e}")
        return []  # fallback for failure case
