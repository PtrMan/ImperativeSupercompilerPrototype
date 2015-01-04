
class Scope(object):
    class EnumScopeType(object):
        NOSCOPE = 0
        NORMALSCOPE = 1 # any other oop scope
        OBJECTSCOPE = 2 # scope of a object, the object holds all variables of the object of the call
        TERMINALSCOPE = 3 # name lookup terminates here
        FUNCTIONSCOPE = 4 # scope of the functionbody


    def __init__(self, scopeType: Scope.EnumScopeType):
        self.scopeType = scopeType
        self.variableContainer = None
        """:type : [DrivingVariableContainer]"""
