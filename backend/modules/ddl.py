from modules.db_connect import connect_to_postgres, connect_to_snowflake

def extract_schema_postgres():
    ddl_text = ""
    try:
        conn = connect_to_postgres()
        cursor = conn.cursor()

        # Fetch all table names
        cursor.execute("""
            SELECT table_schema, table_name
            FROM information_schema.tables
            WHERE table_type = 'BASE TABLE' AND table_schema NOT IN ('pg_catalog', 'information_schema');
        """)
        tables = cursor.fetchall()

        for schema, table in tables:
            ddl_text += f"-- Table: {schema}.{table}\n"
            cursor.execute(f"""
                SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_schema = %s AND table_name = %s;
            """, (schema, table))
            columns = cursor.fetchall()
            ddl_text += f"CREATE TABLE {schema}.{table} (\n"
            ddl_text += ",\n".join([f"  {col} {dtype}" for col, dtype in columns])
            ddl_text += "\n);\n\n"

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"PostgreSQL schema extraction error: {e}")
    return ddl_text


def extract_schema_snowflake():
    ddl_text = ""
    try:
        conn = connect_to_snowflake()
        cursor = conn.cursor()

        # Fetch all tables
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()

        for table in tables:
            table_name = table[1]         # name
            database_name = table[2]      # database_name
            schema_name = table[3]        # schema_name
            full_table_name = f'"{database_name}"."{schema_name}"."{table_name}"'

            ddl_text += f"-- Table: {full_table_name}\n"
            try:
                cursor.execute(f'DESC TABLE {full_table_name}')
                columns = cursor.fetchall()
                ddl_text += f"CREATE TABLE {full_table_name} (\n"
                ddl_text += ",\n".join([f'  "{col[0]}" {col[1]}' for col in columns])
                ddl_text += "\n);\n\n"
            except Exception as e:
                ddl_text += f"-- Failed to describe {full_table_name}: {e}\n\n"
            with open("docs/generated_ddl.txt", "w") as f:
                f.write(ddl_text)    

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Snowflake schema extraction error: {e}")
    return ddl_text

def extract_postgres_documentation():
    documentation = ""
    try:
        conn = connect_to_postgres()
        cursor = conn.cursor()

        # Get table comments
        cursor.execute("""
            SELECT n.nspname as schema, c.relname as table, d.description
            FROM pg_class c
            JOIN pg_namespace n ON n.oid = c.relnamespace
            LEFT JOIN pg_description d ON d.objoid = c.oid AND d.objsubid = 0
            WHERE c.relkind = 'r' 
            AND n.nspname NOT IN ('pg_catalog', 'information_schema')
            ORDER BY n.nspname, c.relname;
        """)
        table_comments = cursor.fetchall()

        # Get column comments
        cursor.execute("""
            SELECT n.nspname as schema, c.relname as table, a.attname as column, d.description
            FROM pg_class c
            JOIN pg_namespace n ON n.oid = c.relnamespace
            JOIN pg_attribute a ON a.attrelid = c.oid
            LEFT JOIN pg_description d ON d.objoid = c.oid AND d.objsubid = a.attnum
            WHERE c.relkind = 'r'
            AND n.nspname NOT IN ('pg_catalog', 'information_schema')
            AND a.attnum > 0
            ORDER BY n.nspname, c.relname, a.attnum;
        """)
        column_comments = cursor.fetchall()

        # Build documentation in the specified format
        for schema, table, comment in table_comments:
            if comment:
                # Find all columns for this table
                table_columns = [col for (sch, tbl, col, desc) in column_comments 
                               if sch == schema and tbl == table and desc]
                
                doc_entry = f"Table Name: {schema}.{table}\n"
                doc_entry += f"Description: {comment}\n"
                if table_columns:
                    doc_entry += "Key Columns: " + ", ".join(table_columns) + "\n"
                doc_entry += "\n"
                documentation += doc_entry
            with open("docs/generated_docp.txt", "w") as f:
                f.write(documentation)

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"PostgreSQL documentation extraction error: {e}")
    return documentation

def extract_snowflake_documentation():
    documentation = ""
    try:
        conn = connect_to_snowflake()
        cursor = conn.cursor()

        # Get all tables across all schemas
        cursor.execute("SHOW TABLES IN ACCOUNT")
        tables = cursor.fetchall()

        for table in tables:
            table_name = table[1]         # name
            database_name = table[2]      # database_name
            schema_name = table[3]        # schema_name
            full_table_name = f"{database_name}.{schema_name}.{table_name}"

            # Get table comment
            cursor.execute(f"""
                SELECT COMMENT 
                FROM {database_name}.INFORMATION_SCHEMA.TABLES
                WHERE TABLE_SCHEMA = '{schema_name}' 
                AND TABLE_NAME = '{table_name}'
            """)
            table_comment = cursor.fetchone()[0] if cursor.rowcount > 0 else None

            # Get column comments
            cursor.execute(f"""
                SELECT COLUMN_NAME, COMMENT
                FROM {database_name}.INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_SCHEMA = '{schema_name}'
                AND TABLE_NAME = '{table_name}'
                AND COMMENT IS NOT NULL
            """)
            column_comments = cursor.fetchall()

            if table_comment or column_comments:
                doc_entry = f"Table Name: {full_table_name}\n"
                if table_comment:
                    doc_entry += f"Description: {table_comment}\n"
                if column_comments:
                    key_columns = [col[0] for col in column_comments]
                    doc_entry += "Key Columns: " + ", ".join(key_columns) + "\n"
                doc_entry += "\n"
                documentation += doc_entry
            with open("docs/generated_documents.txt", "w") as f:
                f.write(documentation)

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Snowflake documentation extraction error: {e}")
    return documentation