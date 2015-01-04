from Driving.DrivingDescriptorVariableScopeRedirector import DrivingDescriptorVariableScopeRedirector
from Driving.DrivingVariable import DrivingVariable
from Driving.Scope import Scope
from Exceptions.VariableLookupException import VariableLookupException

class DrivingDescriptor(object):
    def __init__(self):
        self.astElement = None  # the current abstract syntax element which is "executed" next
        self.astElementIndex = None

        self.outputGraphIndex = None  # index of the root Graph element where the next nodes are appended

        # note that the index _can_ be outside the valid range, if so the execution/driving needs to break out of the next layer and so on
        # [DrivingTrackbackElement]
        self.traceback = []


        # used by the driving mechanism to lookup and store variables
        self.variableRedirector = DrivingDescriptorVariableScopeRedirector(self)

    def copy(self):
        createdDescriptor = DrivingDescriptor()
        createdDescriptor.astElement = self.astElement
        createdDescriptor.astElementIndex = self.astElementIndex
        createdDescriptor.outputGraphIndex = self.outputGraphIndex
        createdDescriptor.traceback = self.traceback.copy()

        return createdDescriptor

    # searches for the first scope and inserts there a variable with that name and that value
    #
    # doesn't look in the topmost scope if a variable with the same name does allready exist
    def declareVariable(self, variablename: str, drivingVariable: DrivingVariable):
        # TODO
        assert False, "TODO"
        

    # searches for the topmost scope with the variablename
    #
    # throws an exception if it wasn't found
    def setVariableByName(self, name: str, variable: DrivingVariable):
        # TODO
        assert False, "TODO"

    # throws an exception if the variable was not found
    def lookupVariable(self, variablename: str) -> DrivingVariable:
        assert len(self.traceback) > 0
        trackbackI = len(self.traceback)-1

        while True:
            if trackbackI < 0:
                raise VariableLookupException(variablename)

            iterationTrackbackElement = self.traceback[trackbackI]

            lookupResult = DrivingDescriptor._lookupScopesByVariablename(variablename, iterationTrackbackElement.scopes)

            if lookupResult == None:
                trackbackI -= 1
                continue

            return lookupResult

    # returns none if it couldn't find the Variable
    @staticmethod
    def _lookupScopesByVariablename(variablename: str, scopes: [Scope]) -> DrivingVariable:
        if len(scopes) == 0:
            return None

        scopeI = len(scopes) - 1

        while True:
            if scopeI < 0:
                return None

            iterationScope = scopes[scopeI]

            if iterationScope.scopeType == Scope.EnumScopeType.TERMINALSCOPE:
                raise VariableLookupException(variablename)
            elif iterationScope.scopeType == Scope.EnumScopeType.FUNCTIONSCOPE or iterationScope.scopeType == Scope.EnumScopeType.NORMALSCOPE:
                if not iterationScope.variableContainer.existVariableByName(variablename):
                    scopeI -= 1
                    continue

                return iterationScope.variableContainer.lookupVariableByName(variablename)
            elif iterationScope.scopeType == Scope.EnumScopeType.NOSCOPE:
                scopeI -= 1
                continue

        assert False, "Unreachable"
