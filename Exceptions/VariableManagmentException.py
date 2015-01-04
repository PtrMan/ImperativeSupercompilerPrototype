class VariableManagmentException(Exception):
    class EnumType(object):
        DECLARE = 0
        LOOKUP = 1

    def __init__(self, type: VariableManagmentException.EnumType, message: str):
        self.message = message
        self.type = type

    def __str__(self):
        return repr(self.type) + repr(self.message)

    @staticmethod
    def _convertTypeToString(type):
        if type == VariableManagmentException.EnumType.DECLARE:
            return "DECLARE"
        elif type == VariableManagmentException.EnumType.LOOKUP:
            return "LOOKUP"
