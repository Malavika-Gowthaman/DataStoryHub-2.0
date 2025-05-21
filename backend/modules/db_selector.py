# import re
# from modules.global_cache import get_cached_keywords
# from modules.vanna_helper import normalize_question


# def determine_database(question: str, context: str) -> str:
#     # Normalize and lowercase question and context
#     question = normalize_question(question).lower()
#     context = context.lower()

#     postgres_keywords = set(get_cached_keywords("PostgreSQL"))
#     snowflake_keywords = set(get_cached_keywords("Snowflake"))

#     # Prioritize the question first
#     score_postgres = sum(1 for word in postgres_keywords if word in question)
#     score_snowflake = sum(1 for word in snowflake_keywords if word in question)

#     if score_postgres > score_snowflake:
#         return "PostgreSQL"
#     elif score_snowflake > score_postgres:
#         return "Snowflake"
    
#     # If no strong match in question, fall back to context
#     score_postgres_context = sum(1 for word in postgres_keywords if word in context)
#     score_snowflake_context = sum(1 for word in snowflake_keywords if word in context)

#     if score_postgres_context > score_snowflake_context:
#         return "PostgreSQL"
#     else:
#         return "Snowflake"

import re
from modules.global_cache import get_cached_keywords
from modules.vanna_helper import normalize_question
from exceptions.custom import DataNotFoundException

def determine_database(question: str, context: str) -> str:
    try:
        # Normalize and lowercase question and context
        question = normalize_question(question).lower()
        context = context.lower()

        postgres_keywords = set(get_cached_keywords("PostgreSQL"))
        snowflake_keywords = set(get_cached_keywords("Snowflake"))

        if not postgres_keywords or not snowflake_keywords:
            raise DataNotFoundException("Cached keywords for databases are missing or empty.")

        # Score the question
        score_postgres = sum(1 for word in postgres_keywords if word in question)
        score_snowflake = sum(1 for word in snowflake_keywords if word in question)

        if score_postgres > score_snowflake:
            return "PostgreSQL"
        elif score_snowflake > score_postgres:
            return "Snowflake"

        # If tie or no strong match, score the context
        score_postgres_context = sum(1 for word in postgres_keywords if word in context)
        score_snowflake_context = sum(1 for word in snowflake_keywords if word in context)

        if score_postgres_context > score_snowflake_context:
            return "PostgreSQL"
        elif score_snowflake_context > score_postgres_context:
            return "Snowflake"
        else:
            raise DataNotFoundException("Unable to determine target database from question or context.")

    except Exception as e:
        raise DataNotFoundException(f"Database detection failed: {str(e)}")
