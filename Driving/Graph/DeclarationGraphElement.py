from Driving.BoundTypeInformation import BoundTypeInformation
from Driving.Graph.Element import Element
from Driving.Graph.EnumDrivingGraphElementContentType import EnumDrivingGraphElementContentType

class DeclarationGraphElement(Element):
    def __init__(self, variableType: BoundTypeInformation, variableName: str, drivingValue: DrivingValue):
        super(DeclarationGraphElement, self).__init__(EnumDrivingGraphElementContentType.DECLARATION)

        self.variableType = variableType
        self.variableName = variableName
        self.drivingValue = drivingValue