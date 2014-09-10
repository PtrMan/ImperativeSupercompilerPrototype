from AbstractSyntaxTree.AbstractSyntaxTreeNode import AbstractSyntaxTreeNode
from AbstractSyntaxTree.EnumAbstractSyntaxTreeNodeType import EnumAbstractSyntaxTreeNodeType

# in the body we need a condition for breaking
# the end must be a continue, because driving doesn't implement a implicit continue
# the body are all instructions
class LoopAbstractSyntaxTreeNode(AbstractSyntaxTreeNode):
    def __init__(self):
        super(LoopAbstractSyntaxTreeNode, self).__init__(EnumAbstractSyntaxTreeNodeType.LOOP)
