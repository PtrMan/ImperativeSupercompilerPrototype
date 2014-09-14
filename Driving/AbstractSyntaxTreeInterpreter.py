from AbstractSyntaxTree.AbstractSyntaxTreeNode import AbstractSyntaxTreeNode
from AbstractSyntaxTree.EnumAbstractSyntaxTreeNodeType import EnumAbstractSyntaxTreeNodeType
from Exceptions.InterpretationException import InterpretationException
from Driving.InterpretedResultValue import InterpretedResultValue
from Driving.DrivingVariableContainer import DrivingVariableContainer
from Driving.ITypeOperationPolicy import ITypeOperationPolicy
from Driving.DrivingValue import DrivingValue
from Driving.EnumTypeNature import EnumTypeNature

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
                raise InterpretationException("Variablename with identifier {0} is unknown!".format(node.name))

            lookedupVariable = variables.lookupVariableByName(node.name)

            interpretedResultValue = InterpretedResultValue(lookedupVariable)
            interpretedResultValue.boundedVariableName = node.name
            return interpretedResultValue

        elif node.type == EnumAbstractSyntaxTreeNodeType.BINARYOPERATION or node.type == EnumAbstractSyntaxTreeNodeType.ASSIGNMENTOPERATION:
            leftSideResult = AbstractSyntaxTreeInterpreter.interpretAndCalculateValue(node.leftSide, variables, typeOperationPolicy)
            rightSideResult = AbstractSyntaxTreeInterpreter.interpretAndCalculateValue(node.leftSide, variables, typeOperationPolicy)

            leftSideType = leftSideResult.value.value.boundTypeInformation
            rightSideType = rightSideResult.value.value.boundTypeInformation

            isWithAssignment = node.type == EnumAbstractSyntaxTreeNodeType.ASSIGNMENTOPERATION

            # check if binary operation is allowed with the types
            isOperationUnderPolicyAllowed = typeOperationPolicy.isBinaryOperationAllowed(leftSideType, rightSideType, node.operationType, isWithAssignment)
            if not isOperationUnderPolicyAllowed:
                # TODO< get type string of the two variables >
                raise InterpretationException("Binary operation using types TODO and TODO is invalid!")

            # get result of the operation using the policy
            resultValue = typeOperationPolicy.getValueOfBinaryOperation(leftSideResult.value.value, rightSideResult.value.value, node.operationType)

            # return result as InterpretedResultValue
            interpretedResultValue = InterpretedResultValue(resultValue)
            if isWithAssignment:
                if leftSideResult.boundedVariableName == None:
                    # TODO< string of operation >
                    raise InterpretationException("left side of binary operation with assignment TODO must a variable")

                leftSideVariableName = leftSideResult.boundedVariableName

                interpretedResultValue.boundedVariableName = leftSideVariableName

            return interpretedResultValue

        elif node.type == EnumAbstractSyntaxTreeNodeType.ASSIGNMENT:
            if node.leftSide.type != EnumAbstractSyntaxTreeNodeType.IDENTIFIER:
                raise InterpretationException("identifier on the left side of an ASSIGNMENTOPERATION expected!")

            resultOnRightSide = AbstractSyntaxTreeInterpreter.interpretAndCalculateValue(node.rightSide)

            # return result as InterpretedResultValue (with bound variable name)
            result = InterpretedResultValue(resultOnRightSide)
            result.boundedVariableName = node.leftSide.name

            return result

        elif node.type == EnumAbstractSyntaxTreeNodeType.INTEGERLITERAL:
            value = DrivingValue(EnumTypeNature.BUILDIN)
            value.boundTypeInformation.buildinType = "int"
            value.buildinValue = node.integer

            return InterpretedResultValue(value)

        else:
            raise InterpretationException("Unsupported AbstractSyntaxTree element for Interpretation!")
