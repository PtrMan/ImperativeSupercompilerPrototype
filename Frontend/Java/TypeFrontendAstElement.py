from Frontend.Java.FrontendAstElement import FrontendAstElement
from Frontend.Java.EnumFrontendAstElementType import EnumFrontendAstElementType

# NOTE< I hope this import is correct >
from Libs.pyparsing import basestring


# .type2 from EnumType
# .basicType
# .referenceType
# .arrayLevel
class TypeFrontendAstElement(FrontendAstElement):
    class EnumType(object):
        BASICTYPE = 0
        REFERENCETYPE = 1

    # tor called by pyparsing
    def __init__(self, data):
        super(TypeFrontendAstElement, self).__init__(EnumFrontendAstElementType.TYPE)

        # python 2.x
        isBasicType = isinstance(data[0], basestring)

        self.basicType = None
        self.referenceType = None

        if isBasicType:
            self.basicType = data[0]
        else:
            self.referenceType = data[0]

        self.arrayLevel = (len(data)-1) / 2