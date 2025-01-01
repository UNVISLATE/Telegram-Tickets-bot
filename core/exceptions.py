class AppException(Exception):
    def __init__(self, message, *args):
        self.message = message

    def __str__(self):
        return f"{self.__class__.__name__}: {self.message}"

class SetupError(AppException): ...