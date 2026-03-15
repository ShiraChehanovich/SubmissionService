class NotFoundException(Exception):
    error_code: int = 404

    def __init__(self, message: str = "Submission not found"):
        self.message = message
        super().__init__(message)

