from AbstractSyntaxTree.AbstractSyntaxTreeNode import AbstractSyntaxTreeNode
from AbstractSyntaxTree.EnumAbstractSyntaxTreeNodeType import EnumAbstractSyntaxTreeNodeType
from AbstractSyntaxTree.EnumBinaryOperationType import EnumBinaryOperationType

class BinaryOperationAbstractSyntaxTreeNode(AbstractSyntaxTreeNode):
    def __init__(self, operationType: EnumBinaryOperationType):
        super(BinaryOperationAbstractSyntaxTreeNode, self).__init__(EnumAbstractSyntaxTreeNodeType.BINARYOPERATION)

        self.operationType = operationType

        self.leftSide = None
        self.rightSide = None
