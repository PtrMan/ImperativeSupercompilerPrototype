from Frontend.Java.EnumFrontendAstElementType import EnumFrontendAstElementType
from Frontend.Java.FrontendAstElement import FrontendAstElement

class BlockFrontendAstElement(FrontendAstElement):
    # tor called by pyparsing
    def __init__(self, data):
        super(BlockFrontendAstElement, self).__init__(EnumFrontendAstElementType.BLOCK)

        assert len(data) >= 2

        self.elements = []

        i = 1

        while i < len(data)-1:
            self.elements.append(data[i])

            i += 1
