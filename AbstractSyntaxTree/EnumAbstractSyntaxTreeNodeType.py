class EnumAbstractSyntaxTreeNodeType(object):
    LOOP = 0
    ONEWAYCONDITION = 1
    CONTINUE = 2
    NOP = 3  # for testing
    ROOT = 4 # pseudo, only the top element can be a root element
    ASSIGNMENT = 5
    CONSTANT = 6
    IDENTIFIER = 7
    SEQUENCE = 8
    ASSIGNMENTOPERATION = 9