class InvalidLanguageOperation(Exception):
    def __init__(self, ordinarityType: str, message: str):
        self.ordinaryType = ordinarityType
        self.message = message

    def __str__(self):
        return repr(self.ordinaryType + ":" + self.message)
