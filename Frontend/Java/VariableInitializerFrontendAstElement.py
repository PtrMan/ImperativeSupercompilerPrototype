from Frontend.Java.FrontendAstElement import FrontendAstElement
from Frontend.Java.EnumFrontendAstElementType import EnumFrontendAstElementType

class VariableInitializerFrontendAstElement(FrontendAstElement):
    # tor called by pyparsing
    def __init__(self, data):
        super(VariableInitializerFrontendAstElement, self).__init__(EnumFrontendAstElementType.VARIABALEINITIALIZER)

        self.withInitialisationArray = data[0] == "{"

        self.expression = None # is none if it is with a initialisationArray

        if self.withInitialisationArray:
            assert data[len(data)-1] == "}"

            self.initialisationArray = data[1:len(data)-1-1+1]
        else:
            self.expression = data[0]