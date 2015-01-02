from Frontend.Java.FrontendAstElement import FrontendAstElement
from Frontend.Java.EnumFrontendAstElementType import EnumFrontendAstElementType

# contains a list of TypeArgumentFrontendAstElement in
# .listOfElements
class TypeArgumentsFrontendAstElement(FrontendAstElement):
    # tor called by pyparsing
    def __init__(self, data):
        super(TypeArgumentsFrontendAstElement, self).__init__(EnumFrontendAstElementType.TYPEARGUMENTS)

        self.listOfElements = [data[0]]

        i = 0
        while i < (len(data)-1) / 2:
            self.listOfElements.append(data[1+2*i])

            i += 1