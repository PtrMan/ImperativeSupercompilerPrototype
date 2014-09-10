from Driving.EnumTypeNature import EnumTypeNature
from Driving.EnumDrivingVariableConstness import EnumDrivingVariableConstness

# TODO< how to handle residuals and non residuals ??? >
class DrivingValue(object):
    def __init__(self, typeNature: EnumTypeNature):
        self.typeNature = typeNature
        self.buildinType = None  # only valid if self.typeNature == EnumBuildinType.BUILDIN
        self.constness = EnumDrivingVariableConstness.INVALID
        self.objectValues = None
        self.buildinValue = None

    ## gets this object/value as a disjunct object which seperates type information and the value
    #
    # this is later needed because copying the whole object is no solution, because most information is redudant (all up to the value)
    def getAsDisjuctTypeValue(self):
        # for simplicity we just return a copy
        return self._copy()

    def _copy(self):
        result = DrivingValue(self.typeNature)
        result.buildinType = self.buildinType
        result.constness = self.constness

        if result.objectValues == None:
            pass
        else:
            result.objectValues = {}

            for iterationKey in self.objectValues.keys():
                result.objectValues[iterationKey] = self.objectValues[iterationKey].getAsDisjuctTypeValue()

        result.buildinValue = self.buildinValue

        return result