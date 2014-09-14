from Frontend.Java.FrontendAstElement import FrontendAstElement
from Frontend.Java.EnumFrontendAstElementType import EnumFrontendAstElementType

class ModifierFrontendAstElement(FrontendAstElement):
    # tor called by pyparsing
    def __init__(self, data):
        super(ModifierFrontendAstElement, self).__init__(EnumFrontendAstElementType.MODIFIER)

        self.text = data[0]