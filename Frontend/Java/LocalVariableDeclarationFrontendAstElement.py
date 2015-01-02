from Frontend.Java.FrontendAstElement import FrontendAstElement
from Frontend.Java.EnumFrontendAstElementType import EnumFrontendAstElementType

# .modifiers
# .type2
# .variableDeclaratorsObject    single object, not a list
class LocalVariableDeclarationFrontendAstElement(FrontendAstElement):
    # tor called by pyparsing
    def __init__(self, data):
        super(LocalVariableDeclarationFrontendAstElement, self).__init__(EnumFrontendAstElementType.LOCALVARIABLEDECLARATION)

        self.modifiers = []

        for i in range(0, len(data)-3):
            self.modifiers.append(data[i])

        self.type2 = data[len(data)-1-2]
        self.variableDeclaratorsObject = data[len(data)-1-1]