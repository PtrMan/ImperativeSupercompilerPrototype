from Frontend.Java.FrontendAstElement import FrontendAstElement
from Frontend.Java.EnumFrontendAstElementType import EnumFrontendAstElementType

class VariableModifierFrontendAstElement(FrontendAstElement):
    class EnumType(object):
        FINAL = 0
        ANNOTATION = 1

    # tor called by pyparsing
    def __init__(self, data):
        super(VariableModifierFrontendAstElement, self).__init__(EnumFrontendAstElementType.VARIABLEMODIFIER)

        if data[0] == "final":
            self.type = VariableModifierFrontendAstElement.EnumType.FINAL
        else:
            self.type = VariableModifierFrontendAstElement.EnumType.ANNOTATION
            # TODO< store reference to the annotation >
