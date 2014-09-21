from AbstractSyntaxTree.AbstractSyntaxTreeNode import AbstractSyntaxTreeNode
from AbstractSyntaxTree.EnumAbstractSyntaxTreeNodeType import EnumAbstractSyntaxTreeNodeType

# only valid for languages where a variable declaration is defined
class TwoWayIfAbstractSyntaxTreeNode(AbstractSyntaxTreeNode):
    def __init__(self):
        super(TwoWayIfAbstractSyntaxTreeNode, self).__init__(EnumAbstractSyntaxTreeNodeType.TWOWAYIF)

        self.expression = None
        self.trueBody = None
        self.falseBody = None # can also be None if it is a one way
