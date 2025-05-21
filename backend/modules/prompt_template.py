# # prompt_template.py

# def build_prompt(dialect: str, question: str) -> str:
#     return f"""
# You are a SQL assistant. Based on the SQL dialect: {dialect}, generate an optimized SQL query
# to answer the following question:

# "{question}"

# Guidelines:
# - Only apply context mappings if relevant to the question.
# - If the question refers to "Rejected" records and no such status exists in the schema, map it to equivalent statuses like transaction_status_id IN ('TERMINATED', 'REJECTED', 'CANCELLED'), only if the schema supports it.
# - If the question does not mention statuses, do not inject status-based filters.
# - Ensure all filters reflect actual values from the schema and avoid assumptions when not applicable.
# - If the question requires anomaly detection (e.g., "abnormal", "spike", "drop"), use statistical methods like comparing against average ± 2 * standard deviation.
# - If the question contains Choice health or Choice health at home it is pointing Review Choice Health  
# - If the question refers to "Terminated" records and no such status exists in the schema, map it to equivalent statuses like transaction_status_id IN ('TERMINATED', 'TERMINATE', 'TERMINATES'), only if the schema supports it.

# Only return the SQL queries without any explanation.

# """.strip()


# Make sure to:
# - Handle partial name matches using LIKE or ILIKE for user inputs like names.
# - Only return the SQL query without explanation.

# def build_prompt(dialect: str, question: str) -> str:
#     return f"""
# You are a SQL assistant. Based on the SQL dialect: {dialect}, generate optimized SQL queries
# to answer the following question(s):

# "{question}"

# If there are multiple questions, generate a separate SQL query for each, clearly separated using comments
# (e.g., -- Query 1, -- Query 2, etc.).

# Only return the SQL queries without any explanation.
# """.strip()



def build_prompt(dialect: str, question: str) -> str:
    """
    Builds a prompt for an LLM to generate an optimized SQL query
    based on the specified dialect and user question.

    Args:
        dialect (str): SQL dialect (e.g., PostgreSQL, Snowflake)
        question (str): User's natural language query

    Returns:
        str: Formatted prompt for LLM

    Raises:
        ValueError: If required arguments are missing or invalid
    """
    if not dialect or not question:
        raise ValueError("Both 'dialect' and 'question' must be provided.")

    try:
        return f"""
You are a SQL assistant. Based on the SQL dialect: {dialect}, generate an optimized SQL query
to answer the following question:

"{question}"

Guidelines:
- Only apply context mappings if relevant to the question.
- If the question refers to "Rejected" records and no such status exists in the schema, map it to equivalent statuses like transaction_status_id IN ('TERMINATED', 'REJECTED', 'CANCELLED'), only if the schema supports it.
- If the question does not mention statuses, do not inject status-based filters.
- Ensure all filters reflect actual values from the schema and avoid assumptions when not applicable.
- If the question requires anomaly detection (e.g., "abnormal", "spike", "drop"), use statistical methods like comparing against average ± 2 * standard deviation.
- If the question contains Choice health or Choice health at home it is pointing Review Choice Health  
- If the question refers to "Terminated" records and no such status exists in the schema, map it to equivalent statuses like transaction_status_id IN ('TERMINATED', 'TERMINATE', 'TERMINATES'), only if the schema supports it.

Only return the SQL queries without any explanation.
""".strip()
    
    except Exception as e:
        print(f"[PromptBuilder] Error building prompt: {e}")
        raise
