from Frontend.Java.FrontendAstElement import FrontendAstElement
from Frontend.Java.EnumFrontendAstElementType import EnumFrontendAstElementType

# .references all (chained) references, are Reference objects
class ReferenceTypeFrontendAstElement(FrontendAstElement):
    class Reference(object):
        def __init__(self, identifier, typeArguments):
            self.identifier = identifier
            self.typeArguments = typeArguments

    # tor called by pyparsing
    def __init__(self, data):
        super(ReferenceTypeFrontendAstElement, self).__init__(EnumFrontendAstElementType.REFERENCETYPE)

        self.references = []

        for i in range(0, len(data)/2):
            identifier = data[i*2 + 0]
            typeArguments = data[i*2 + 1]

            self.references.append(ReferenceTypeFrontendAstElement.Reference(identifier, typeArguments))