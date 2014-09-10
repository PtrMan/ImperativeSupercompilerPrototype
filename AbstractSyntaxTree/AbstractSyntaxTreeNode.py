from AbstractSyntaxTree.EnumAbstractSyntaxTreeNodeType import EnumAbstractSyntaxTreeNodeType

class AbstractSyntaxTreeNode(object):
    def __init__(self, type:EnumAbstractSyntaxTreeNodeType):
        self.type = type

        self.childrens = []