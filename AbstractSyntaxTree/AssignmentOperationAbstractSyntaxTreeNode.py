from AbstractSyntaxTree.AbstractSyntaxTreeNode import AbstractSyntaxTreeNode
from AbstractSyntaxTree.EnumAbstractSyntaxTreeNodeType import EnumAbstractSyntaxTreeNodeType
from AbstractSyntaxTree.EnumBinaryOperationType import EnumBinaryOperationType

class AssignmentOperationAbstractSyntaxTreeNode(AbstractSyntaxTreeNode):
    def __init__(self, operation: EnumBinaryOperationType):
        super(AssignmentOperationAbstractSyntaxTreeNode, self).__init__(EnumAbstractSyntaxTreeNodeType.ASSIGNMENTOPERATION)

        self.operation = operation

        self.leftSide = None # instance of AbstractSyntaxTreeNode
        self.rightSide = None # instance of AbstractSyntaxTreeNode
