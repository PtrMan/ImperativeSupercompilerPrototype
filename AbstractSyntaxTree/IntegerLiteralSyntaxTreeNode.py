__author__ = 'r0b3'

from AbstractSyntaxTree.AbstractSyntaxTreeNode import AbstractSyntaxTreeNode
from AbstractSyntaxTree.EnumAbstractSyntaxTreeNodeType import EnumAbstractSyntaxTreeNodeType

class IntegerLiteralSyntaxTreeNode(AbstractSyntaxTreeNode):
    def __init__(self, integer):
        super(IntegerLiteralSyntaxTreeNode, self).__init__(EnumAbstractSyntaxTreeNodeType.INTEGERLITERAL)

        self.integer = integer