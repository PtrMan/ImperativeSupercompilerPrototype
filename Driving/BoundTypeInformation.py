from Driving.EnumTypeNature import EnumTypeNature

## type information in the sense that it is attached to an variable and not a part of a database with inheritance information, etc.
#
class BoundTypeInformation(object):
    def __init__(self, typeNature: EnumTypeNature):
        self.typeNature = typeNature
        self.buildinType = None  # only valid if self.typeNature == EnumBuildinType.BUILDIN, is a string, is the type of the host language
        self.userdefinedType = None # type in the host language/environment, is a string, is used for lookup with a mechanism