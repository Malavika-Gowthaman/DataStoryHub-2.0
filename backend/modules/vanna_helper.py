# import pandas as pd
# from vanna.openai import OpenAI_Chat
# from vanna.chromadb import ChromaDB_VectorStore
# import psycopg2
# import snowflake.connector
# from modules.db_connect import connect_to_postgres, connect_to_snowflake
# from modules import POSGRES_TABLES, SNOWFLAKE_TABLES, SQL_QUESTION_PAIR
# from config import settings
# from modules.prompt_template import build_prompt
# from modules.ddl import extract_schema_postgres, extract_schema_snowflake, extract_postgres_documentation, extract_snowflake_documentation

# #  Define MyVanna class with dialect handling
# class MyVanna(ChromaDB_VectorStore, OpenAI_Chat):
#     def __init__(self, config=None):
#         ChromaDB_VectorStore.__init__(self, config=config)
#         OpenAI_Chat.__init__(self, config=config)
#         self.dialect = None  

#     def set_dialect(self, database):
#         """Sets the correct SQL dialect based on the selected database."""
#         if database == "PostgreSQL":
#             self.dialect = "postgresql"
#         elif database == "Snowflake":
#             self.dialect = "snowflake"
#         else:
#             self.dialect = "postgresql" 

#     def connect(self, dialect: str):
#         """
#         Sets up a database connection and binds run_sql for Vanna.

#         Args:
#             dialect (str): 'postgresql' or 'snowflake'
#         """
#         if dialect == "postgresql":
#             conn = connect_to_postgres()
#         elif dialect == "snowflake":
#             conn = connect_to_snowflake()
#         else:
#             raise ValueError(f"Unsupported dialect: {dialect}")

        
#         def _run_sql(sql):
#             return pd.read_sql(sql, conn)

#         self.run_sql = _run_sql
#         self.conn = conn         



#     def qa_pair_train(self, qa_pairs: dict[str, str]):
#         """
#         add question and answer pair to the vector store
#         """
#         for question, sql in qa_pairs.items():
#             self.add_question_sql(question= question, sql= sql)        


#     def fit_train(self, 
#                   dialect: str,
#                   filter_schema: list[str], 
#                   filter_table: list[str], 
#                   ddl_path: str, 
#                   documentation_path: str,
#                   qa_pairs: dict[str, str]):
#         """
#         Fit and train the LLM with relevant schema, DDL, documentation, and Q&A pairs.

#         Args:
#             filter_schema (list[str]): List of schema names to include.
#             filter_table (list[str]): List of table names to include.
#             ddl_path (str): Path to DDL file.
#             documentation_path (str): Path to system or technical documentation file.
#             business_documentation_path (str): Path to business context documentation file.
#             qa_pairs (dict): Dict of question-answer training examples.
#         """
#         # Set dialect
#         self.set_dialect(dialect.capitalize())
#         self.connect(dialect)
#         # Fetch schema from INFORMATION_SCHEMA
#         try:
#             schema_df = self.run_sql("SELECT * FROM INFORMATION_SCHEMA.COLUMNS")
#         except Exception as e:
#             print(f"[ERROR] Failed to query schema: {e}")
#             return

#         # Filter relevant schemas and tables
#         schema_df.columns = schema_df.columns.str.lower()
#         filtered_schema = schema_df[
#             schema_df['table_schema'].isin([s.lower() for s in filter_schema]) &
#             schema_df['table_name'].isin([t.lower() for t in filter_table])
#         ]

#         # Build training plan from filtered schema
#         try:
#             plan = self.get_training_plan_generic(filtered_schema)
#             self.train(plan=plan)
#         except Exception as e:
#             print(f"[ERROR] Training plan failed: {e}")    

#         # Combine and train DDLs
#         try:
#             for path in ddl_path:
#                 with open(path, "rb") as f:
#                     ddl = f.read().decode("utf-8")
#                     self.train(ddl=ddl)
#         except Exception as e:
#             print(f"[ERROR] Failed to read/train DDLs: {e}")

#         # Combine and train documentation
#         try:
#             for path in documentation_path:
#                 with open(path, "rb") as f:
#                     documentation = f.read().decode("utf-8")
#                     self.train(documentation=documentation)
#         except Exception as e:
#             print(f"[ERROR] Failed to read/train documentation: {e}")

#         # Train on Q&A pairs
#         try:
#             self.qa_pair_train(qa_pairs=qa_pairs)
#         except Exception as e:
#             print(f"[ERROR] Failed to train Q&A pairs: {e}")

#         print(f"[INFO] Vanna training complete for dialect: {dialect}")         
               

# #  Initialize Vanna with LLM access
# vn = MyVanna(config={
#     'api_key': settings.OPENAI_API_KEY,
#     'model': 'gpt-4o',
#     'allow_llm_to_see_data': True
# })

# # vn.fit_train(dialect="postgresql",
# #     filter_schema=["public"], 
# #     filter_table= POSGRES_TABLES,
# #     ddl_path=["docs/ddl(financial).txt"],
# #     documentation_path=["docs/documentations(financial).txt"],
# #     qa_pairs=SQL_QUESTION_PAIR
# #     )

# vn.fit_train(dialect="snowflake",
#     filter_schema=["CHOICE_HEALTH_AT_HOME"],
#     filter_table= SNOWFLAKE_TABLES,
#     ddl_path=["docs/ddl.txt"],
#     documentation_path=["docs/documentation.txt"],
#     qa_pairs=SQL_QUESTION_PAIR
#     )

# # def load_docs_from_db(database: str = "PostgreSQL") -> str:
# #     if database == "PostgreSQL":
# #         ddl = extract_schema_postgres()
# #         docs = extract_postgres_documentation()
# #         return ddl + "\n\n" + docs
# #     elif database == "Snowflake":
# #         ddl = extract_schema_snowflake()
# #         docs = extract_snowflake_documentation()
# #         return ddl + "\n\n" + docs
# #     else:
# #         return ""
# #  Load schema descriptions
# # def load_docs():
# #     doc_files = ["docs/sqlddl.txt","docs/sqldocumentation.txt","docs/ddl.txt", "docs/documentations.txt", "docs/ddl(financial).txt", "docs/documentations(financial).txt","docs/q&a.txt"]
# #     content = ""
# #     for file in doc_files:
# #         with open(file, "r") as f:
# #             content += f.read() + "\n"
# #     return content

# # #  Train AI with schema and documentation
# # vn.add_ddl(load_docs())
# # vn.add_ddl(extract_schema_postgres())  # or "Snowflake"
# # # vn.add_ddl(extract_schema_snowflake())  # or "Snowflake"
# # vn.add_ddl(extract_postgres_documentation())  # or "Snowflake"
# # vn.add_ddl(extract_snowflake_documentation())  # or "Snowflake"



# # vn.add_ddl(load_docs_from_db(database="PostgreSQL"))  # or "Snowflake"
# # vn.add_ddl(load_docs_from_db(database="Snowflake"))




# #  Function to execute SQL query
# def execute_sql_query(database, sql_query):
#     try:
#         conn = connect_to_postgres() if database == "PostgreSQL" else connect_to_snowflake()
#         df = pd.read_sql(sql_query, conn)  # Run query
#         conn.close()
#         return df
#     except Exception as e:
#         print(f"Database error: {e}")
#         return pd.DataFrame()  # Return empty DataFrame on error

# #  Ask AI a question (Handles Dialect & Database)
# # def ask_question(database, question, allow_llm_to_see_data=True):
# #     """
# #     Generates SQL based on the user question and executes it on the selected database.
# #     """
# #     #  Set dialect dynamically
# #     vn.set_dialect(database)

# #     #  Modify the question to include dialect info
# #     formatted_question = f"Generate a {vn.dialect} SQL query for: {question}"

# #     #  Generate SQL query
# #     sql_query, _, _ = vn.ask(formatted_question, print_results=False)  # Remove `sql_dialect`

# #     #  Execute the SQL query based on the selected database
# #     df = execute_sql_query(database, sql_query)
# #     return sql_query, df
# # At the top of vanna_helper.py
#  # Adjust import path as needed

# def normalize_question(raw_question: str) -> str:
#     correction_prompt = f"""
# You are a helpful assistant. Your task is to fix and clarify a user’s question related to data, even if it contains typos, slang, or vague phrasing.

# Fix the following question and return a clear version:
# "{raw_question}"

# Corrected:
# """.strip()

#     try:
#         corrected_question, _, _ = vn.ask(correction_prompt, print_results=False)
#         return corrected_question.strip().replace('"', '')
#     except Exception as e:
#         print(f"Error normalizing question: {e}")
#         return raw_question

# # # Enhanced database detector
# # def determine_database(question: str, context: str) -> str:
# #     # Normalize the question first
# #     cleaned_question = normalize_question(question)
# #     full_text = f"{context}\nUser: {cleaned_question}".lower()
    
# #     postgres_keywords = [
# #         "revenue", "net income", "employees", "EPS", "total assets", 
# #         "year", "company", "financial", "negative", "highest",
# #         "fraud", "credit score", "loan approval", "investment",
# #         "balance", "spending", "customer", "account",
# #         "transaction amount", "approval status"
# #     ]
    
# #     snowflake_keywords = [
# #         "json data", "functional blocks", "transactions", "user actions",
# #         "interventions", "progress", "logs", "workflow", "queue",
# #         "raw data", "analytics", "warehouse", "big data", "reporting"
# #     ]
    
# #     if any(word in full_text for word in postgres_keywords):
# #         return "PostgreSQL"
# #     elif any(word in full_text for word in snowflake_keywords):
# #         return "Snowflake"
    
# #     return "Snowflake"  # Default fallback

# def prompt_from_template(database: str, user_question: str):
#     """
#     Uses Python-based prompt template to generate SQL from user question.
    
#     Args:
#         database (str): 'PostgreSQL' or 'Snowflake'
#         user_question (str): The user's natural language question.
    
#     Returns:
#         tuple: (generated SQL string, result DataFrame)

#     Fixes user question, uses Python-based prompt template, and generates SQL.
#     """
#     # Normalize the question
#     clean_question = normalize_question(user_question)

#     # Set dialect in Vanna
#     vn.set_dialect(database)


#     # Build prompt from external template function
#     prompt = build_prompt(dialect=vn.dialect, question=clean_question)

#     # Generate SQL query using the prompt
#     sql_query, _, _ = vn.ask(prompt, print_results=False)

#     # Execute the SQL and return result
#     df = execute_sql_query(database, sql_query)
#     return sql_query, df




import pandas as pd
from vanna.openai import OpenAI_Chat
from vanna.chromadb import ChromaDB_VectorStore
import psycopg2
import snowflake.connector
from modules.db_connect import connect_to_postgres, connect_to_snowflake
from modules import POSGRES_TABLES, SNOWFLAKE_TABLES, SQL_QUESTION_PAIR
from config import settings
from modules.prompt_template import build_prompt
from modules.ddl import extract_schema_postgres, extract_schema_snowflake, extract_postgres_documentation, extract_snowflake_documentation

#  Define MyVanna class with dialect handling
class MyVanna(ChromaDB_VectorStore, OpenAI_Chat):
    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        OpenAI_Chat.__init__(self, config=config)
        self.dialect = None  

    def set_dialect(self, database):
        """Sets the correct SQL dialect based on the selected database."""
        if database == "PostgreSQL":
            self.dialect = "postgresql"
        elif database == "Snowflake":
            self.dialect = "snowflake"
        else:
            self.dialect = "postgresql" 

    def connect(self, dialect: str):
        """
        Sets up a database connection and binds run_sql for Vanna.

        Args:
            dialect (str): 'postgresql' or 'snowflake'
        """
        try:
            if dialect == "postgresql":
                conn = connect_to_postgres()
            elif dialect == "snowflake":
                conn = connect_to_snowflake()
            else:
                raise ValueError(f"Unsupported dialect: {dialect}")
        except Exception as e:
            print(f"[ERROR] Failed to connect to database ({dialect}): {e}")
            raise

        def _run_sql(sql):
            try:
                return pd.read_sql(sql, conn)
            except Exception as e:
                print(f"[ERROR] SQL execution failed: {e}")
                return pd.DataFrame()

        self.run_sql = _run_sql
        self.conn = conn         

    def qa_pair_train(self, qa_pairs: dict[str, str]):
        """
        add question and answer pair to the vector store
        """
        for question, sql in qa_pairs.items():
            try:
                self.add_question_sql(question= question, sql= sql)
            except Exception as e:
                print(f"[ERROR] Failed to add QA pair ({question}): {e}")       

    def fit_train(self, 
                  dialect: str,
                  filter_schema: list[str], 
                  filter_table: list[str], 
                  ddl_path: list[str], 
                  documentation_path: list[str],
                  qa_pairs: dict[str, str]):
        """
        Fit and train the LLM with relevant schema, DDL, documentation, and Q&A pairs.
        """
        # Set dialect
        try:
            self.set_dialect(dialect.capitalize())
            self.connect(dialect)
        except Exception as e:
            print(f"[ERROR] Setup failed: {e}")
            return

        # Fetch schema from INFORMATION_SCHEMA
        try:
            schema_df = self.run_sql("SELECT * FROM INFORMATION_SCHEMA.COLUMNS")
            if schema_df.empty:
                print("[WARNING] Schema query returned no results.")
        except Exception as e:
            print(f"[ERROR] Failed to query schema: {e}")
            return

        # Filter relevant schemas and tables
        try:
            schema_df.columns = schema_df.columns.str.lower()
            filtered_schema = schema_df[
                schema_df['table_schema'].isin([s.lower() for s in filter_schema]) &
                schema_df['table_name'].isin([t.lower() for t in filter_table])
            ]
        except Exception as e:
            print(f"[ERROR] Filtering schema failed: {e}")
            return

        # Build training plan from filtered schema
        try:
            plan = self.get_training_plan_generic(filtered_schema)
            self.train(plan=plan)
        except Exception as e:
            print(f"[ERROR] Training plan failed: {e}")    

        # Combine and train DDLs
        for path in ddl_path:
            try:
                with open(path, "rb") as f:
                    ddl = f.read().decode("utf-8")
                    self.train(ddl=ddl)
            except Exception as e:
                print(f"[ERROR] Failed to read/train DDL file '{path}': {e}")

        # Combine and train documentation
        for path in documentation_path:
            try:
                with open(path, "rb") as f:
                    documentation = f.read().decode("utf-8")
                    self.train(documentation=documentation)
            except Exception as e:
                print(f"[ERROR] Failed to read/train documentation file '{path}': {e}")

        # Train on Q&A pairs
        try:
            self.qa_pair_train(qa_pairs=qa_pairs)
        except Exception as e:
            print(f"[ERROR] Failed to train Q&A pairs: {e}")

        print(f"[INFO] Vanna training complete for dialect: {dialect}")         

# Initialize Vanna with LLM access
vn = MyVanna(config={
    'api_key': settings.OPENAI_API_KEY,
    'model': 'gpt-4o',
    'allow_llm_to_see_data': True
})

vn.fit_train(dialect="snowflake",
    filter_schema=["CHOICE_HEALTH_AT_HOME"],
    filter_table= SNOWFLAKE_TABLES,
    ddl_path=["docs/ddl.txt"],
    documentation_path=["docs/documentation.txt"],
    qa_pairs=SQL_QUESTION_PAIR
    )

def execute_sql_query(database, sql_query):
    try:
        conn = connect_to_postgres() if database == "PostgreSQL" else connect_to_snowflake()
        df = pd.read_sql(sql_query, conn)  # Run query
        conn.close()
        return df
    except Exception as e:
        print(f"[ERROR] Database error during query execution: {e}")
        return pd.DataFrame()  # Return empty DataFrame on error

def normalize_question(raw_question: str) -> str:
    correction_prompt = f"""
You are a helpful assistant. Your task is to fix and clarify a user’s question related to data, even if it contains typos, slang, or vague phrasing.

Fix the following question and return a clear version:
"{raw_question}"

Corrected:
""".strip()

    try:
        corrected_question, _, _ = vn.ask(correction_prompt, print_results=False)
        return corrected_question.strip().replace('"', '')
    except Exception as e:
        print(f"[ERROR] Error normalizing question: {e}")
        return raw_question

def prompt_from_template(database: str, user_question: str):
    """
    Uses Python-based prompt template to generate SQL from user question.
    """
    try:
        clean_question = normalize_question(user_question)
        vn.set_dialect(database)
        prompt = build_prompt(dialect=vn.dialect, question=clean_question)
        sql_query, _, _ = vn.ask(prompt, print_results=False)
        df = execute_sql_query(database, sql_query)
        return sql_query, df
    except Exception as e:
        print(f"[ERROR] Failed to generate or execute SQL query: {e}")
        return "", pd.DataFrame()
