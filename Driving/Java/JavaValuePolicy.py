from Driving.BoundTypeInformation import BoundTypeInformation
from Driving.DrivingValue import DrivingValue
from Driving.EnumTypeNature import EnumTypeNature
from Driving.IValuePolicy import IValuePolicy
from Exceptions.InternalErrorException import InternalErrorException


class JavaValuePolicy(IValuePolicy):
    def isStandardValueAssignedForType(self, type: BoundTypeInformation):
        if type.typeNature == EnumTypeNature.BUILDIN:
           return True
        else:
            # assigned to null
            return True

    ## call is only valid if .isStandardValueAssignedForType() returned true
    def getStandardValueForType(self, type: BoundTypeInformation):
        if type.typeNature == EnumTypeNature.BUILDIN:
            # it is a non-reference, so the standard value depend on the type

            resultValue = DrivingValue.createWithGivenBoundTypeInformation(type)

            # TODO< set residual value? >
            if type.buildinType == "int":
                resultValue = DrivingValue.createWithGivenBoundTypeInformation(type)

                nonresidualValue = DrivingValue.Value(EnumTypeNature.USERDEFINED)
                nonresidualValue.builtinValue = 0
                resultValue.nonresidualValue.append(nonresidualValue)
            else:
                raise InternalErrorException("buildinType '{0}' is not jet handled!".format(type.buildinType))

            return resultValue

        else:
            # it is a reference, so the standard value is null, which is None in python

            resultValue = DrivingValue.createWithGivenBoundTypeInformation(type)

            nonresidualValue = DrivingValue.Value(EnumTypeNature.USERDEFINED)
            nonresidualValue.userDefinedValue = None # is null for java
            resultValue.nonresidualValue.append(nonresidualValue)

            # TODO< set residual value? >

            return resultValue