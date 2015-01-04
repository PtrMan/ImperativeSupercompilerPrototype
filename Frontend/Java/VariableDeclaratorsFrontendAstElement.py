from Frontend.Java.FrontendAstElement import FrontendAstElement
from Frontend.Java.EnumFrontendAstElementType import EnumFrontendAstElementType

class VariableDeclaratorsFrontendAstElement(FrontendAstElement):
    # tor called by pyparsing
    def __init__(self, data):
        super(VariableDeclaratorsFrontendAstElement, self).__init__(EnumFrontendAstElementType.VARIABLEDECLARATORS)

        self.declarators = []

        i = 0

        while i < (len(data)-1)/2+1:
            self.declarators.append(data[2*i])

            i += 1