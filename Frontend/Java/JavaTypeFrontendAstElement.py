from Frontend.Java.FrontendAstElement import FrontendAstElement
from Frontend.Java.EnumFrontendAstElementType import EnumFrontendAstElementType

class JavaTypeFrontendAstElement(FrontendAstElement):
    def __init__(self, data):
        super(JavaTypeFrontendAstElement, self).__init__(EnumFrontendAstElementType.JAVATYPE)

        self.typeIdentiferElement = data[0]
        self.typeHasArray = len(data) > 1 # if the array literals are behind this is true