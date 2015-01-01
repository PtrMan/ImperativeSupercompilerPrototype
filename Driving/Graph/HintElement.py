from Driving.Graph.Element import Element
from Driving.Graph.EnumDrivingGraphElementContentType import EnumDrivingGraphElementContentType

class HintElement(Element):
    def __init__(self):
        super(HintElement, self).__init__(EnumDrivingGraphElementContentType.HINT)

        self.hints = []

    class SingleHint(object):
        class EnumType(object):
            # indicates the taken path of a condition
            # .takenPath contains the path which was taken
            # .astElement is the TwoWayIfAbsractSyntaxTreeNode of the condition for the hint
            CONDITIONPATHTAKEN = 1

        def __init__(self, type):
            self.type = type

            self.takenPath = None
            self.astElement = None