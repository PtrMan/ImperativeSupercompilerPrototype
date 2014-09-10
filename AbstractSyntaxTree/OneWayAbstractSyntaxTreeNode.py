from AbstractSyntaxTree.AbstractSyntaxTreeNode import AbstractSyntaxTreeNode
from AbstractSyntaxTree.EnumAbstractSyntaxTreeNodeType import EnumAbstractSyntaxTreeNodeType

class OneWayAbstractSyntaxTreeNode(AbstractSyntaxTreeNode):
    def __init__(self):
        super(OneWayAbstractSyntaxTreeNode, self).__init__(EnumAbstractSyntaxTreeNodeType.ONEWAYCONDITION)

        self.conditionAstElement = None
