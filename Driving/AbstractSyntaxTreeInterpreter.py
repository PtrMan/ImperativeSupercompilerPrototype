from AbstractSyntaxTree.AbstractSyntaxTreeNode import AbstractSyntaxTreeNode
from AbstractSyntaxTree.EnumAbstractSyntaxTreeNodeType import EnumAbstractSyntaxTreeNodeType
from Exceptions.InterpretationException import InterpretationException
from Driving.InterpretedResultValue import InterpretedResultValue
from Driving.DrivingVariableContainer import DrivingVariableContainer

## Interprets Nodes from the abstract syntax tree
#
# used to calculate the value for the residuals while driving
class AbstractSyntaxTreeInterpreter(object):
    ## tries to interpret only a single evaluable expression with the current variables and returns the result
    # throws an exception if the interpretation doesn't make sense
    @staticmethod
    def interpretAndCalculateValue(node: AbstractSyntaxTreeNode, variables: DrivingVariableContainer) -> InterpretedResultValue:
        if node.type == EnumAbstractSyntaxTreeNodeType.IDENTIFIER:
            # try to look up the identifier

            # TODO< recode for real oop code >
            identifierIsKnown = variables.existVariableByName(node.name)
            if not identifierIsKnown:
                raise InterpretationException("identifier {0} is unknown!".format(node.name))

            lookedupVariable = variables.lookupVariableByName(node.name)

            return InterpretedResultValue(lookedupVariable)

        elif node.type == EnumAbstractSyntaxTreeNodeType.ASSIGNMENTOPERATION:
            if node.leftSide.type != EnumAbstractSyntaxTreeNodeType.IDENTIFIER:
                raise InterpretationException("identifier on the left side of an ASSIGNMENTOPERATION expected!")

            resultOnRightSide = AbstractSyntaxTreeInterpreter.interpretAndCalculateValue(node.rightSide)

            # TODO
        else:
            raise InterpretationException("Unsupported AbstractSyntaxTree element for Interpretation!")
