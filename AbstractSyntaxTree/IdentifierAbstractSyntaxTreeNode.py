from AbstractSyntaxTree.AbstractSyntaxTreeNode import AbstractSyntaxTreeNode
from AbstractSyntaxTree.EnumAbstractSyntaxTreeNodeType import EnumAbstractSyntaxTreeNodeType

class IdentifierAbstractSyntaxTreeNode(AbstractSyntaxTreeNode):
    def __init__(self, name):
        super(IdentifierAbstractSyntaxTreeNode, self).__init__(EnumAbstractSyntaxTreeNodeType.IDENTIFIER)

        self.name = name
