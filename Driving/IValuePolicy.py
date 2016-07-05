from Driving.BoundTypeInformation import BoundTypeInformation

## policy for the declaration of variables of a type (some languages set the value of a type to a standardvalue)
#
#
class IValuePolicy(object):
    def isStandardValueAssignedForType(self, type: BoundTypeInformation):
        raise NotImplementedError()

    ## call is only valid if .isStandardValueAssignedForType() returned true
    def getStandardValueForType(self, type: BoundTypeInformation):
        raise NotImplementedError()
