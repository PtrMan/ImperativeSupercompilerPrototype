from Driving.IVariableScopesRedirector import IVariableScopesRedirector
from Driving.DrivingDescriptor import DrivingDescriptor
from Driving.DrivingVariable import DrivingVariable

class DrivingDescriptorVariableScopeRedirector(IVariableScopesRedirector):
    def __init__(self, drivingDescriptor: DrivingDescriptor):
        self._drivingDescriptor = drivingDescriptor

    def lookupVariable(self, variablename: str) -> DrivingVariable:
        return self._drivingDescriptor.lookupVariable(variablename)

    def setVariableByName(self, name: str, variable: DrivingVariable):
        self._drivingDescriptor.setVariableByName(name, variable)

    def declareVariable(self, name: str, drivingVariable: DrivingVariable):
        self._drivingDescriptor.declareVariable(name, drivingVariable)