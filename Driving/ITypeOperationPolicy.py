from Driving.BoundTypeInformation import BoundTypeInformation
from Driving.DrivingValue import DrivingValue
from AbstractSyntaxTree.EnumBinaryOperationType import EnumBinaryOperationType

## policy of the valid operations on typed values and the results/types
#
# is not a policy in the sense of Policy based design
#
# Every language (Java, C#, Python, etc) implements another policy of the allowed operations and the resulting values and types
# So for every language a new class of this class must be inherited, which implements all methods
class ITypeOperationPolicy(object):
    # TODO< take assignemnt out >
    # \param isAssignment if its true its in the form A ?= B, where ? is any binary operation
    def isBinaryOperationAllowed(self, leftSide: BoundTypeInformation, rightSide: BoundTypeInformation, operationType: EnumBinaryOperationType, isAssignment: bool) -> bool:
        raise NotImplementedError()

    ## returns the type of the value of the operation
    #
    # throws exception if binary operation is not possible, should never happen because the code checks allready with isBinaryOperationAllowed
    #def getTypeOfBinaryOperation(self, leftSide: BoundTypeInformation, rightSide: BoundTypeInformation, operationType: EnumBinaryOperationType) -> BoundTypeInformation:
    #    raise NotImplementedError()

    ## calculates the exact value after applying the operation on the two input values
    def getValueOfBinaryOperation(self, leftSide: DrivingValue, rightSide: DrivingValue, operationType: EnumBinaryOperationType) -> DrivingValue:
        raise NotImplementedError()

    ## asks if a value of a condition expression is implicitly castable to bool
    def isConditionTypeImplicitCastableToBool(self) -> bool:
        raise NotImplementedError()

    ## gets the value of an implicit cast, throws something if the cast is not possible
    def getValueOfImplicitCastToBuildinType(self, value: DrivingValue, castToType: BoundTypeInformation):
        raise NotImplementedError()

    def isAssignmentOperationAllowed(self, leftSide: BoundTypeInformation, rightSide: BoundTypeInformation):
        raise NotImplementedError()
