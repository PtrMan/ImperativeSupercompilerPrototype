from Frontend.Java.FrontendAstElement import FrontendAstElement
from Frontend.Java.EnumFrontendAstElementType import EnumFrontendAstElementType

class IdentifierFrontendAstElement(FrontendAstElement):
    # tor called by pyparsing
    def __init__(self, data):
        super(IdentifierFrontendAstElement, self).__init__(EnumFrontendAstElementType.IDENTIFIER)

        self.identifierAsString = data[0]
