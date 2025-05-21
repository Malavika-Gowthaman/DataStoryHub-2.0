# from modules.utils import get_keywords_from_db

# _keyword_cache = {}

# def get_cached_keywords(db_type):
#     if db_type not in _keyword_cache:
#         _keyword_cache[db_type] = get_keywords_from_db(db_type)
#     return _keyword_cache[db_type]

# def refresh_keyword_cache(db_type):
#     _keyword_cache[db_type] = get_keywords_from_db(db_type)
    


from modules.utils import get_keywords_from_db

_keyword_cache = {}

def get_cached_keywords(db_type: str, force: bool = False):
    """
    Returns cached keywords for the given db_type.
    If not cached or if force=True, fetches from DB.
    """
    if force or db_type not in _keyword_cache:
        try:
            print(f"[Cache] Fetching keywords from DB for: {db_type}")
            _keyword_cache[db_type] = get_keywords_from_db(db_type)
        except Exception as e:
            print(f"[Cache] Error fetching keywords from DB: {e}")
            return []
    else:
        print(f"[Cache] Returning cached keywords for: {db_type}")
    return _keyword_cache[db_type]


def refresh_keyword_cache(db_type: str):
    """
    Force refresh the keyword cache for a specific db_type.
    """
    try:
        print(f"[Cache] Refreshing cache for: {db_type}")
        _keyword_cache[db_type] = get_keywords_from_db(db_type)
    except Exception as e:
        print(f"[Cache] Failed to refresh cache for {db_type}: {e}")
