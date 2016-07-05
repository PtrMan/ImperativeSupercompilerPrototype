from Driving.Graph.Element import Element
from Driving.Graph.EnumDrivingGraphElementContentType import EnumDrivingGraphElementContentType

class AssignmentElement(Element):
    def __init__(self):
        super(AssignmentElement, self).__init__(EnumDrivingGraphElementContentType.ASSIGNMENT)

        self.leftDrivingValue = None
        self.rightDrivingValue = None

        self.rightNonresidualIndex = None # index of the nonresidual value on the right side
