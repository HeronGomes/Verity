# exception/exceptions.py

class llm_exception(Exception):
    def __init__(self, message, status_code):
        super().__init__(message,status_code)
        self.status_code = status_code
        self.message = message

    def __str__(self):
        return f"llm_exception: {self.message} (Status code: {self.status_code})"
