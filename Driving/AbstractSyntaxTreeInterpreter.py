from AbstractSyntaxTree.AbstractSyntaxTreeNode import AbstractSyntaxTreeNode
from AbstractSyntaxTree.EnumAbstractSyntaxTreeNodeType import EnumAbstractSyntaxTreeNodeType
from Exceptions.InterpretationException import InterpretationException
from Driving.InterpretedResultValue import InterpretedResultValue
from Driving.DrivingVariableContainer import DrivingVariableContainer
from Driving.ITypeOperationPolicy import ITypeOperationPolicy

## Interprets Nodes from the abstract syntax tree
#
# used to calculate the value for the residuals while driving
class AbstractSyntaxTreeInterpreter(object):
    ## tries to interpret only a single evaluable expression with the current variables and returns the result
    # throws an exception if the interpretation doesn't make sense
    @staticmethod
    def interpretAndCalculateValue(node: AbstractSyntaxTreeNode, variables: DrivingVariableContainer, typeOperationPolicy: ITypeOperationPolicy) -> InterpretedResultValue:
        if node.type == EnumAbstractSyntaxTreeNodeType.IDENTIFIER:
            # try to look up the identifier

            # TODO< recode for real oop code >
            identifierIsKnown = variables.existVariableByName(node.name)
            if not identifierIsKnown:
                raise InterpretationException("identifier {0} is unknown!".format(node.name))

            lookedupVariable = variables.lookupVariableByName(node.name)

            return InterpretedResultValue(lookedupVariable)
        elif node.type == EnumAbstractSyntaxTreeNodeType.BINARYOPERATION:
            leftSideResult = AbstractSyntaxTreeInterpreter.interpretAndCalculateValue(node.leftSide, variables, typeOperationPolicy)
            rightSideResult = AbstractSyntaxTreeInterpreter.interpretAndCalculateValue(node.leftSide, variables, typeOperationPolicy)

            leftSideType = leftSideResult.value.boundTypeInformation
            rightSideType = rightSideResult.value.boundTypeInformation

            # TODO< refactor flag to enum >
            # check if binary operation is allowed with the types
            isOperationUnderPolicyAllowed = typeOperationPolicy.isBinaryOperationAllowed(leftSideType, rightSideType, node.operationType, False)
            if not isOperationUnderPolicyAllowed:
                # TODO< get type string of the two variables >
                raise InterpretationException("Binary operation using types TODO and TODO is invalid!")

            # get result of the operation using the policy
            resultValue = typeOperationPolicy.getValueOfBinaryOperation(leftSideResult.value, rightSideResult.value, node.operationType)

            # return result as InterpretedResultValue
            return InterpretedResultValue(resultValue)

        elif node.type == EnumAbstractSyntaxTreeNodeType.ASSIGNMENTOPERATION:
            if node.leftSide.type != EnumAbstractSyntaxTreeNodeType.IDENTIFIER:
                raise InterpretationException("identifier on the left side of an ASSIGNMENTOPERATION expected!")

            resultOnRightSide = AbstractSyntaxTreeInterpreter.interpretAndCalculateValue(node.rightSide)

            # return result as InterpretedResultValue (with bound variable name)
            result = InterpretedResultValue(resultOnRightSide)
            result.boundedVariableName = node.leftSide.name

            return result
        else:
            raise InterpretationException("Unsupported AbstractSyntaxTree element for Interpretation!")
