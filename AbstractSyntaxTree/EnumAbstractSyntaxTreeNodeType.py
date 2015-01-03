class EnumAbstractSyntaxTreeNodeType(object):
    LOOP = 0
    ONEWAYCONDITION = 1 # deprecated
    CONTINUE = 2
    NOP = 3  # for testing
    ROOT = 4 # pseudo, only the top element can be a root element
    ASSIGNMENT = 5
    CONSTANT = 6
    IDENTIFIER = 7
    SEQUENCE = 8 # opens new scope
    ASSIGNMENTOPERATION = 9
    BINARYOPERATION = 10
    VARIABLEDECLARATION = 11
    INTEGERLITERAL = 12
    TWOWAYIF = 13
    NONSCOPEDSEQUENCE = 14 # opens no new scope