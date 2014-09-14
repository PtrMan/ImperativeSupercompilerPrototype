from Frontend.Java.FrontendAstElement import FrontendAstElement
from Frontend.Java.EnumFrontendAstElementType import EnumFrontendAstElementType

class VariableDeclarationFrontendAstElement(FrontendAstElement):
    # tor called by pyparsing
    def __init__(self, data):
        super(VariableDeclarationFrontendAstElement, self).__init__(EnumFrontendAstElementType.VARIABALEDECLARATIONS)

        self.modifiers = []
        self.variableDeclarators = []
        self.javaType = data[0]

        i = 0

        # NOTE< we don't check here for duplicated modifiers >
        while True:
            if VariableDeclarationFrontendAstElement.isModifier(data[i]):
                self.modifiers.append(data[i])
            else:
                break

            i += 1

        i += 1




        self.variableDeclarators = data[i:len(data)-1]

    @staticmethod
    def isModifier(input: FrontendAstElement):
        return input.type == EnumFrontendAstElementType.MODIFIER