from AbstractSyntaxTree.AbstractSyntaxTreeNode import AbstractSyntaxTreeNode
from AbstractSyntaxTree.EnumAbstractSyntaxTreeNodeType import EnumAbstractSyntaxTreeNodeType

class NonscopedSequenceAbstractSyntaxTreeNode(AbstractSyntaxTreeNode):
    def __init__(self):
        super(NonscopedSequenceAbstractSyntaxTreeNode, self).__init__(EnumAbstractSyntaxTreeNodeType.NONSCOPEDSEQUENCE)
