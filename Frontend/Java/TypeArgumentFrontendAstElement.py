from Frontend.Java.FrontendAstElement import FrontendAstElement
from Frontend.Java.EnumFrontendAstElementType import EnumFrontendAstElementType

# see in parser
# .type2 is from EnumType
# .reference is the reference if .type2 == REFERENCETYPE
#            if not it may be set, dependng on input
# .inheriation is the inheration string, can be set if .type2 == NONREFERENCETYPE, depending on input
class TypeArgumentFrontendAstElement(FrontendAstElement):
    class EnumType(object):
        REFERENCETYPE = 0
        NONREFERENCETYPE = 1

    # tor called by pyparsing
    def __init__(self, data):
        super(TypeArgumentFrontendAstElement, self).__init__(EnumFrontendAstElementType.TYPEARGUMENT)

        if data[0].type == EnumFrontendAstElementType.REFERENCETYPE:
            self.type2 = TypeArgumentFrontendAstElement.EnumType.REFERENCETYPE
        else:
            self.type2 = TypeArgumentFrontendAstElement.EnumType.NONREFERENCETYPE

        self.reference = None
        self.inheration = None

        if data[0].type == EnumFrontendAstElementType.REFERENCETYPE:
            self.reference = data[0]
        else:
            if len(data) > 1:
                self.inheration = data[1]
                self.reference = data[2]
