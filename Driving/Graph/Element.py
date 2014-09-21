from Driving.Graph.EnumDrivingGraphElementContentType import EnumDrivingGraphElementContentType

class Element(object):
    def __init__(self, type: EnumDrivingGraphElementContentType):
        self.type = type
