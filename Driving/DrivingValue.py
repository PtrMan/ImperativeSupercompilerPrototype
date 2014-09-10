from Driving.EnumTypeNature import EnumTypeNature
from Driving.EnumDrivingVariableConstness import EnumDrivingVariableConstness
from Driving.BoundTypeInformation import BoundTypeInformation

# TODO< how to handle residuals and non residuals ??? >
class DrivingValue(object):
    def __init__(self, typeNature: EnumTypeNature):
        self.boundTypeInformation = BoundTypeInformation(typeNature)
        self.constness = EnumDrivingVariableConstness.INVALID
        self.objectValues = None
        self.buildinValue = None

    ## gets this object/value as a disjunct object which seperates type information and the value
    #
    def getAsDisjuctTypeValue(self):
        result = DrivingValue(self.typeNature)
        # bound type information is not copied because even referenced values don't change their type
        # the type is changed with the construction of a new value
        result.boundTypeInformation = self.boundTypeInformation
        result.constness = self.constness

        if result.objectValues == None:
            pass
        else:
            result.objectValues = {}

            for iterationKey in self.objectValues.keys():
                result.objectValues[iterationKey] = self.objectValues[iterationKey].getAsDisjuctTypeValue()

        result.buildinValue = self.buildinValue

        return result
