from Frontend.Java.FrontendAstElement import FrontendAstElement
from Frontend.Java.EnumFrontendAstElementType import EnumFrontendAstElementType

class VariableDeclaratorsFrontendAstElement(FrontendAstElement):
    # tor called by pyparsing
    def __init__(self, data):
        super(VariableDeclaratorsFrontendAstElement, self).__init__(EnumFrontendAstElementType.VARIABLEDECLARATORS)

        self.declarators = [data[0]]

        if len(data) > 1:
            i = 0

            while i < (len(data)-1)/2:
                self.declarators.append(data[1+2*i])

                i += 1