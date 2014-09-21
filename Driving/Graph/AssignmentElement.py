from Driving.Graph.Element import Element
from Driving.Graph.EnumDrivingGraphElementContentType import EnumDrivingGraphElementContentType

class AssignmentElement(Element):
    def __init__(self):
        super(AssignmentElement, self).__init__(EnumDrivingGraphElementContentType.ASSIGNMENT)

        self.leftVariableName = None
        self.rightExpression = None # must be derived from DrivingGraphExpressions.Expression
                                    # is the expression which gets evaluated for the value of the variable
