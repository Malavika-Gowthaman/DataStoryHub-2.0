import os
from pathlib import Path
from modules.db_connect import get_postgres_tables, get_snowflake_tables

BASE_DIR = Path(__file__).absolute().parent.parent

#place tables here
# POSGRES_TABLES = ["account_usage_patterns","accounts","customers", 
#                   "transactions","credit_scores", "alerts","fraudulent_transactions","investment_portfolios",
#                   "loan_applications","merchant_details"]
# SNOWFLAKE_TABLES = []

POSGRES_TABLES = get_postgres_tables()
SNOWFLAKE_TABLES = get_snowflake_tables()

SQL_QUESTION_PAIR = {"Find out which transaction mode (Online, In-Store, ATM) is most commonly used by customers who have received at least one fraud alert.": "SELECT t.transaction_mode, COUNT(*) AS mode_count FROM  transactions t JOIN  alerts a ON t.account_id = a.customer_id WHERE a.alert_type = 'Fraud Alert' GROUP BY  t.transaction_mode ORDER BY mode_count DESC LIMIT 1;",
                      "Find customers who have spent more than 50% of their current account balance . List their name, account balance, and total spending.": "SELECT transaction_id, updated_at FROM transactions WHERE updated_by = 'AUTOHUB_TRANSCATIONAL_REPORT_LOAD' AND transaction_status_id = 'status_001';",
        "Retrieve the details of the longest-running transaction that is still in progress.": "SELECT transaction_id, start_date_time, DATEDIFF('second', start_date_time, CURRENT_TIMESTAMP) AS duration FROM transactions WHERE Transaction_status_id = 'status_001' ORDER BY duration DESC LIMIT 1;"
        }