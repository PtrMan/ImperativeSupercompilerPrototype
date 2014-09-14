from AbstractSyntaxTree.AbstractSyntaxTreeNode import AbstractSyntaxTreeNode
from AbstractSyntaxTree.EnumAbstractSyntaxTreeNodeType import EnumAbstractSyntaxTreeNodeType
from Driving.BoundTypeInformation import BoundTypeInformation

# only valid for languages where a variable declaration is defined
class VariableDeclarationAbstractSyntaxTreeNode(AbstractSyntaxTreeNode):
    def __init__(self, boundType: BoundTypeInformation, variableName: str):
        super(VariableDeclarationAbstractSyntaxTreeNode, self).__init__(EnumAbstractSyntaxTreeNodeType.VARIABLEDECLARATION)

        self.boundType = boundType # type is BoundTypeInformation, must be defined
        self.variableName = variableName # str: is the variablename, must be defined

        self.rightSide = None # is a DrivingGraphEpression, can be defined

