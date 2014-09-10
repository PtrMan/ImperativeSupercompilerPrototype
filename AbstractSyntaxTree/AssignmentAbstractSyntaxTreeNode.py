from AbstractSyntaxTree.AbstractSyntaxTreeNode import AbstractSyntaxTreeNode
from AbstractSyntaxTree.EnumAbstractSyntaxTreeNodeType import EnumAbstractSyntaxTreeNodeType

class AssignmentAbstractSyntaxTreeNode(AbstractSyntaxTreeNode):
    def __init__(self):
        super(AssignmentAbstractSyntaxTreeNode, self).__init__(EnumAbstractSyntaxTreeNodeType.ASSIGNMENT)

        self.leftSide = None # instance of AbstractSyntaxTreeNode
        self.rightSide = None # instance of AbstractSyntaxTreeNode
