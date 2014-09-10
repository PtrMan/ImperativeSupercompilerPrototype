from AbstractSyntaxTree.AbstractSyntaxTreeNode import AbstractSyntaxTreeNode
from AbstractSyntaxTree.EnumAbstractSyntaxTreeNodeType import EnumAbstractSyntaxTreeNodeType

class SequenceAbstractSyntaxTreeNode(AbstractSyntaxTreeNode):
    def __init__(self):
        super(SequenceAbstractSyntaxTreeNode, self).__init__(EnumAbstractSyntaxTreeNodeType.SEQUENCE)
