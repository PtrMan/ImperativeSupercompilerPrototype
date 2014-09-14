from DrivingGraphExpressions.Expression import Expression
from DrivingGraphExpressions.EnumExpressionType import EnumExpressionType

class BinaryExpression(Expression):
    def __init__(self, left, right, operationType):
        super(BinaryExpression, self).__init__(EnumExpressionType.BINARY)

        self.operationType = operationType
        self.left = left
        self.right = right
