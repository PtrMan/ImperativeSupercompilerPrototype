from DrivingGraphExpressions.Expression import Expression
from DrivingGraphExpressions.EnumExpressionType import EnumExpressionType

class ConstantExpression(Expression):
    def __init__(self, value):
        super(ConstantExpression, self).__init__(EnumExpressionType.CONSTANT)

        self.value = value
