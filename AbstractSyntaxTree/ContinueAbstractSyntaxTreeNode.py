from AbstractSyntaxTree.AbstractSyntaxTreeNode import AbstractSyntaxTreeNode
from AbstractSyntaxTree.EnumAbstractSyntaxTreeNodeType import EnumAbstractSyntaxTreeNodeType

# neded for simpler evaluation
class ContinueAbstractSyntaxTreeNode(AbstractSyntaxTreeNode):
    def __init__(self):
        super(ContinueAbstractSyntaxTreeNode, self).__init__(EnumAbstractSyntaxTreeNodeType.CONTINUE)
