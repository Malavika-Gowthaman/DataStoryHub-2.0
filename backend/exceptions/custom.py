# # exceptions/custom.py

# """
# Custom exceptions for ChatDB / NL-to-SQL
# """

# class IrrelevantPromptException(Exception):
#     def __init__(self, msg="The question does not relate to available data."):
#         self.msg = msg

#     def __str__(self):
#         return "IrrelevantPromptException"


# class InvalidSQLException(Exception):
#     def __init__(self, msg="The generated SQL is invalid or failed to execute."):
#         self.msg = msg

#     def __str__(self):
#         return "InvalidSQLException"


# class RephraseException(Exception):
#     def __init__(self, msg="Please rephrase your question."):
#         self.msg = msg

#     def __str__(self):
#         return "RephraseException"


class IrrelevantPromptException(Exception):
    def __init__(self, msg="The question does not relate to available data.", original_error=None):
        self.msg = msg
        self.original_error = original_error  # Capture the original error if any

    def __str__(self):
        return f"IrrRelevantPromptException: {self.msg}, Original Error: {self.original_error}"


class InvalidSQLException(Exception):
    def __init__(self, msg="The generated SQL is invalid or failed to execute.", original_error=None):
        self.msg = msg
        self.original_error = original_error

    def __str__(self):
        return f"InvalidSQLException: {self.msg}, Original Error: {self.original_error}"


class RephraseException(Exception):
    def __init__(self, msg="Please rephrase your question.", original_error=None):
        self.msg = msg
        self.original_error = original_error

    def __str__(self):
        return f"RephraseException: {self.msg}, Original Error: {self.original_error}"


# New Exception Classes

class DatabaseConnectionException(Exception):
    def __init__(self, msg="Failed to connect to the database.", error_code=5001, original_error=None):
        self.msg = msg
        self.error_code = error_code
        self.original_error = original_error

    def __str__(self):
        return f"Error {self.error_code}: {self.msg}, Original Error: {self.original_error}"


class DataNotFoundException(Exception):
    def __init__(self, msg="Requested data not found in the database.", error_code=4001):
        self.msg = msg
        self.error_code = error_code

    def __str__(self):
        return f"Error {self.error_code}: {self.msg}"


class InvalidInputException(Exception):
    def __init__(self, msg="The input provided is invalid or improperly formatted.", error_code=4002):
        self.msg = msg
        self.error_code = error_code

    def __str__(self):
        return f"Error {self.error_code}: {self.msg}"


class UnauthorizedAccessException(Exception):
    def __init__(self, msg="User does not have the required permissions.", error_code=4010):
        self.msg = msg
        self.error_code = error_code

    def __str__(self):
        return f"Error {self.error_code}: {self.msg}"


class TimeoutException(Exception):
    def __init__(self, msg="The request timed out.", error_code=4080):
        self.msg = msg
        self.error_code = error_code

    def __str__(self):
        return f"Error {self.error_code}: {self.msg}"


class InternalServerErrorException(Exception):
    def __init__(self, msg="An internal server error occurred.", error_code=5000):
        self.msg = msg
        self.error_code = error_code

    def __str__(self):
        return f"Error {self.error_code}: {self.msg}"


class KeywordFetchError(Exception):
    """Raised when keyword fetching from the database fails."""
    pass


