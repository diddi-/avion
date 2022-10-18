class HttpException(Exception):
    """ This is a base exception for API errors.
    HttpExceptions will be translated in to proper return codes by flask error handler. """
    def __init__(self, return_code: int = 500, message: str = "Unknown error"):
        self.return_code = return_code
        self.message = message
        super().__init__(message)
