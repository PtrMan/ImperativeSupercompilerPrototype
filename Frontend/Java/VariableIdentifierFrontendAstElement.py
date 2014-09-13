from Frontend.Java.FrontendAstElement import FrontendAstElement
from Frontend.Java.EnumFrontendAstElementType import EnumFrontendAstElementType

class VariableIdentifierFrontendAstElement(FrontendAstElement):
    # tor called by pyparsing
    def __init__(self, data):
        super(VariableIdentifierFrontendAstElement, self).__init__(EnumFrontendAstElementType.VARIABALEIDENTIFIER)

        self.variableName = data[0]
