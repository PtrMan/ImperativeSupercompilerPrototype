from Driving.EnumTypeNature import EnumTypeNature
from Driving.EnumDrivingVariableConstness import EnumDrivingVariableConstness
from Driving.BoundTypeInformation import BoundTypeInformation

# TODO< how to handle residuals and non residuals ??? >

# a variable is mapped by its name to a Driving value
#
# the value can be changed at different times, but we need to store all nonresidual changes, because they can be accessed at a later time
# there exists only one "time" for the residual value
class DrivingValue(object):
    class Value(object):
        class EnumType(object):
            BUILTIN = 0
            USERDEFINED = 1

        def __init__(self, type: DrivingValue.Value.EnumType):
            self.type = type
            self.builtinValue = None
            self.userDefinedValue = None

    def __init__(self, typeNature: EnumTypeNature):
        self.boundTypeInformation = BoundTypeInformation(typeNature)
        self.constness = EnumDrivingVariableConstness.INVALID

        self.residualValue = None # Value
        self.nonresidualValue = [] # [Value]  is an array because the value(s) have to be accessable at a later time

    @staticmethod
    def createWithGivenBoundTypeInformation(boundTypeInformation: BoundTypeInformation):
        createdDrivingValue = DrivingValue(None)

        createdDrivingValue.boundTypeInformation = boundTypeInformation
        createdDrivingValue.constness = EnumDrivingVariableConstness.INVALID

        return createdDrivingValue



    ## gets this object/value as a disjunct object which seperates type information and the value
    #
    ### old code, was for some reason never used
    ###def getAsDisjuctTypeValue(self):
    ###    result = DrivingValue(self.typeNature)
    ###    # bound type information is not copied because even referenced values don't change their type
    ###    # the type is changed with the construction of a new value
    ###    result.boundTypeInformation = self.boundTypeInformation
    ###    result.constness = self.constness
    ###
    ###    if result.objectValues == None:
    ###        pass
    ###    else:
    ###        result.objectValues = {}
    ###
    ###        for iterationKey in self.objectValues.keys():
    ###            result.objectValues[iterationKey] = self.objectValues[iterationKey].getAsDisjuctTypeValue()
    ###
    ###    result.buildinValue = self.buildinValue
    ###
    ###    return result
