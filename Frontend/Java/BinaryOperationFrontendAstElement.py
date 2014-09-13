from Frontend.Java.FrontendAstElement import FrontendAstElement
from Frontend.Java.EnumFrontendAstElementType import EnumFrontendAstElementType
from AbstractSyntaxTree.EnumBinaryOperationType import EnumBinaryOperationType

class BinaryOperationFrontendAstElement(FrontendAstElement):
    # tor called by pyparsing
    def __init__(self, data):
        super(BinaryOperationFrontendAstElement, self).__init__(EnumFrontendAstElementType.BINARYOPERATION)

        self.leftElement = data[0]
        (self.operationType, self.isAssignment) = BinaryOperationFrontendAstElement.convertOperationStringToOperationTypeAndAssignment(data[1])
        self.rightElement = data[2]

    @staticmethod
    def convertOperationStringToOperationTypeAndAssignment(operationString: str):
        lookupDict = {
            "+" : (EnumBinaryOperationType.ADD, False),
            "+=" : (EnumBinaryOperationType.ADD, True),
            "-" : (EnumBinaryOperationType.SUB, False),
            "-=" : (EnumBinaryOperationType.SUB, True),
            "*" : (EnumBinaryOperationType.MUL, False),
            "*=" : (EnumBinaryOperationType.MUL, True)
            # TODO< more >
        }

        # NOTE< we don't convert the exception here >
        # TODO
        return lookupDict[operationString]