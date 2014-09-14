from DrivingGraphExpressions.Expression import Expression
from DrivingGraphExpressions.EnumExpressionType import EnumExpressionType

class VariableIdentifierExpression(Expression):
    def __init__(self, name):
        super(VariableIdentifierExpression, self).__init__(EnumExpressionType.VARIABLEIDENTIFIER)

        self.variableName = name
