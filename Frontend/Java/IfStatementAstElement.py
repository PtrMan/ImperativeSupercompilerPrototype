from Frontend.Java.FrontendAstElement import FrontendAstElement
from Frontend.Java.EnumFrontendAstElementType import EnumFrontendAstElementType

class IfStatementAstElement(FrontendAstElement):
    # tor called by pyparsing
    def __init__(self, data):
        super(IfStatementAstElement, self).__init__(EnumFrontendAstElementType.IF)

        self.conditionExpression = data[2]
        self.trueBody = data[4]
        self.elseBody = None

        if len(data) > 5:
            self.elseBody = data[6]
