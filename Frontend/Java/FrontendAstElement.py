from Frontend.Java.EnumFrontendAstElementType import EnumFrontendAstElementType

## Ast Element of the Frontend
#
# will be used for tree rewriting to the Ast which is used by the Supercompiler
class FrontendAstElement(object):
    def __init__(self, type: EnumFrontendAstElementType):
        self.type = type
