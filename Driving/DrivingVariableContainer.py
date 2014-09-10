from Driving.DrivingVariable import DrivingVariable

# small layer above the lookup and storage of variables while driving
class DrivingVariableContainer(object):
    def __init__(self):
        # TODO< should be a hashtable for faster lookup >
        self.variables = [] # instances of "DrivingVariable"

    # returns the DrivingVariable instance if found
    # throws VariableLookupException if no variable was found
    def lookupVariableByName(self, name: str) -> DrivingVariable:
        for iterationVariable in self.variables:
            if iterationVariable.name == name:
                return iterationVariable

        assert False

    def existVariableByName(self, name: str) -> bool:
        for iterationVariable in self.variables:
            if iterationVariable.name == name:
                return True

        return False

    def addVariable(self, drivingVariable: DrivingVariable):
        self.variables.append(drivingVariable)

    # TODO
    def copy(self):
        assert False

