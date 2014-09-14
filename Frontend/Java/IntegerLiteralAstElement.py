from Frontend.Java.FrontendAstElement import FrontendAstElement
from Frontend.Java.EnumFrontendAstElementType import EnumFrontendAstElementType

class IntegerLiteralAstElement(FrontendAstElement):
    def __init__(self, data):
        super(IntegerLiteralAstElement, self).__init__(EnumFrontendAstElementType.INTEGERLITERAL)

        self.integer = int(data[0])
