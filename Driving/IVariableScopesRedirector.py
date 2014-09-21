from Driving.DrivingVariable import DrivingVariable

## class for the decoupling of variablelookup and definition
#
# With the help of this class the driving part and the interpreter doesn't need to know anything how the variables are managed
class IVariableScopesRedirector(object):
    # throws an exception if the variable was not found
    def lookupVariable(self, variablename: str) -> DrivingVariable:
        raise NotImplementedError()

    def setVariableByName(self, name: str, variable: DrivingVariable):
        raise NotImplementedError()

    def declareVariable(self, name: str, drivingVariable: DrivingVariable):
        raise NotImplementedError()
