from Frontend.Java.FrontendAstElement import FrontendAstElement
from Frontend.Java.EnumFrontendAstElementType import EnumFrontendAstElementType

class VariableDeclaratorFrontendAstElement(FrontendAstElement):
    # tor called by pyparsing
    def __init__(self, data):
        super(VariableDeclaratorFrontendAstElement, self).__init__(EnumFrontendAstElementType.VARIABALEDECLARATOR)

        self.declarationVariablename = data[0]

        self.hasBrackets = False
        self.variableInitializer = None # is None if no initializer was given

        if len(data) == 1:
            return

        followIndex = 1

        if data[followIndex] == "[":
            self.hasBrackets = True

            followIndex += 2

        if data[followIndex] == "=":
            self.variableInitializer = data[followIndex+1]
