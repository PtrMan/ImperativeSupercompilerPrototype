from Driving.ITypeOperationPolicy import ITypeOperationPolicy
from Driving.BoundTypeInformation import BoundTypeInformation
from Driving.DrivingValue import DrivingValue
from AbstractSyntaxTree.EnumBinaryOperationType import EnumBinaryOperationType
from Driving.EnumTypeNature import EnumTypeNature
from Driving.EnumBuildinType import EnumBuildinType
from Driving.EnumDrivingVariableConstness import EnumDrivingVariableConstness
from Exceptions.InvalidLanguageOperation import InvalidLanguageOperation

class JavaTypeOperationPolicy(ITypeOperationPolicy):
    def isBinaryOperationAllowed(self, leftSide: BoundTypeInformation, rightSide: BoundTypeInformation, operationType: EnumBinaryOperationType, isAssignment: bool) -> bool:
        if leftSide.typeNature == EnumTypeNature.BUILDIN and rightSide.typeNature == EnumTypeNature.BUILDIN:
            if leftSide.buildinType == EnumBuildinType.INT and leftSide.buildinType == EnumBuildinType.INT:
                return True

            return False
        else:
            return False

    def getValueOfBinaryOperation(self, leftSide: DrivingValue, rightSide: DrivingValue, operationType: EnumBinaryOperationType) -> DrivingValue:
        if leftSide.boundTypeInformation.typeNature == EnumTypeNature.BUILDIN and rightSide.boundTypeInformation.typeNature == EnumTypeNature.BUILDIN:
            if leftSide.boundTypeInformation.buildinType == EnumBuildinType.INT and leftSide.boundTypeInformation.buildinType == EnumBuildinType.INT:
                resultRawValue = 0

                if operationType == EnumBinaryOperationType.ADD:
                    resultRawValue = leftSide.buildinValue + rightSide.buildinValue
                elif operationType == EnumBinaryOperationType.SUB:
                    resultRawValue = leftSide.buildinValue - rightSide.buildinValue
                elif operationType == EnumBinaryOperationType.MUL:
                    resultRawValue = leftSide.buildinValue * rightSide.buildinValue
                elif operationType == EnumBinaryOperationType.DIV:
                    resultRawValue = leftSide.buildinValue / rightSide.buildinValue
                else:
                    raise InvalidLanguageOperation("binary", "Invalid operation on (int|int)")

                resultDrivingValue = DrivingValue(EnumTypeNature.BUILDIN)
                resultDrivingValue.buildinValue = resultRawValue
                resultDrivingValue.constness = EnumDrivingVariableConstness.CONSTANT

                return resultDrivingValue
            else:
                # TODO< description >
                raise InvalidLanguageOperation("binary", "")

        raise InvalidLanguageOperation("binary", "Unhandled case, Internal Error")