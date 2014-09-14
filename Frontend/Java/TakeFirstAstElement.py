from Frontend.Java.FrontendAstElement import FrontendAstElement
from Frontend.Java.EnumFrontendAstElementType import EnumFrontendAstElementType

class TakeFirstAstElement(FrontendAstElement):
    # tor called by pyparsing
    def __init__(self, data):
        super(TakeFirstAstElement, self).__init__(EnumFrontendAstElementType.TAKEFIRST)

        self.element = data[0]
