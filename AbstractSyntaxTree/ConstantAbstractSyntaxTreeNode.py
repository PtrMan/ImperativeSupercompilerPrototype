from AbstractSyntaxTree.AbstractSyntaxTreeNode import AbstractSyntaxTreeNode
from AbstractSyntaxTree.EnumAbstractSyntaxTreeNodeType import EnumAbstractSyntaxTreeNodeType

class ConstantAbstractSyntaxTreeNode(AbstractSyntaxTreeNode):
    def __init__(self):
        super(ConstantAbstractSyntaxTreeNode, self).__init__(EnumAbstractSyntaxTreeNodeType.CONSTANT)

        self.value = None # type is "Value"
