from Driving.DrivingValue import DrivingValue

## hold the result of a invokation to AbstractSyntaxTreeInterpreter. ...
#
# must be in a class because the result can stand alone or be bound to a vriable which will ater be assigned the value
class InterpretedResultValue(object):
    def __init__(self, value: DrivingValue):
        # is the variablename the value will be assigned to
        # can be None if it is not assigned to a variable
        self.boundedVariableName = None

        self.value = value

