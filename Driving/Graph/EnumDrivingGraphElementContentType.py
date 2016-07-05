
class EnumDrivingGraphElementContentType(object):
    NOP = 0
    CONTINUE = 1 # if an explicit or implicit continue of a loop was executed, is actually a nop
    ASSIGNMENT = 2
    HINT = 3 # is a DrivingGraphHintElement, which can contain one or many hints
    DECLARATION = 4 # is a (local) variable declaration