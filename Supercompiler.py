# small prototype for a supercompiler

from DrivingGraphExpressions.ConstantExpression import ConstantExpression

class Graph(object):
    def __init__(self):
        self.elements = []

    def addElement(self, element):
        self.elements.append(element)

    def resetGraph(self):
        self.elements = []

class GraphElement(object):
    def __init__(self, content):
        self.childIndices = []
        self.content = content


class EnumVariableType(object):
    INTEGER = 0


class Value(object):
    def __init__(self, type):
        self.type = type

        self.valueInt = 0

from Driving.Graph.EnumDrivingGraphElementContentType import EnumDrivingGraphElementContentType
from Driving.Graph.AssignmentElement import AssignmentElement as DrivingGraphAssignmentElement
from Driving.Graph.HintElement import HintElement as DrivingGraphHintElement
from Driving.Graph.Element import Element as DrivingGraphElement


from Driving.DrivingDescriptor import DrivingDescriptor
from Driving.DrivingValue import DrivingValue

from Driving.DrivingVariableContainer import DrivingVariableContainer


class DrivingTrackbackElement(object):
    def __init__(self):
        self.astElement = None
        self.astElementIndex = None

        """:type : list of [DrivingGraphHintElement]"""
        self.hints = []
                        # to the trackback bound hints (which will be undone if the trackback element gets invalidated
                        # this happens in the method .invalidate

        self.scopes = []
        """:type : list of [Scope]"""

    # TODO< params so the hints can be undone
    def invalidate(self, drivingDescriptor: DrivingDescriptor, driving: Supercompiler):
        # TODO< write to the drivingGraph Hints that undo the Hints of the DrivingTrackbackElement >
        pass

from Driving.AbstractSyntaxTreeInterpreter import AbstractSyntaxTreeInterpreter
from Driving.Java.JavaTypeOperationPolicy import JavaTypeOperationPolicy

from AbstractSyntaxTree.EnumAbstractSyntaxTreeNodeType import EnumAbstractSyntaxTreeNodeType
from AbstractSyntaxTree.VariableDeclarationAbstractSyntaxTreeNode import VariableDeclarationAbstractSyntaxTreeNode
from AbstractSyntaxTree.TwoWayIfAbstractSyntaxTreeNode import TwoWayIfAbstractSyntaxTreeNode

from Driving.EnumDrivingVariableConstness import EnumDrivingVariableConstness
from Driving.EnumTypeNature import EnumTypeNature
from Driving.EnumBuildinType import EnumBuildinType
from Driving.DrivingVariable import DrivingVariable
from Driving.BoundTypeInformation import BoundTypeInformation

from Exceptions.DrivingException import DrivingException
from Exceptions.InternalErrorException import InternalErrorException

class Supercompiler(object):
    def __init__(self):
        self._drivingGraph = Graph()

        self._ast = None

        # for driving
        self._drivingDescriptors = []

        # class inherited from Driving.ITypeOperationPolicy
        self._typeOperationPolicy = None

    def _drive(self):
        self._drivingGraph.resetGraph()

        self._drivingGraph.addElement(GraphElement(DrivingGraphElement(EnumDrivingGraphElementContentType.NOP)))

        while True:
            pass

            self._driveStep()

    def _driveStep(self):
        assert self._ast != None

        drivingDescriptorIndex = 0

        while drivingDescriptorIndex < len(self._drivingDescriptors):
            assert drivingDescriptorIndex >= 0 and drivingDescriptorIndex < len(self._drivingDescriptors)

            iterationDrivingDescriptor = self._drivingDescriptors[drivingDescriptorIndex]

            astElementType = iterationDrivingDescriptor.astElement.childrens[iterationDrivingDescriptor.astElementIndex].type


            if astElementType == EnumAbstractSyntaxTreeNodeType.LOOP:
                drivingTrackbackElement = DrivingTrackbackElement()
                drivingTrackbackElement.astElement = iterationDrivingDescriptor.astElement
                drivingTrackbackElement.astElementIndex = iterationDrivingDescriptor.astElementIndex + 1

                iterationDrivingDescriptor.traceback.append(drivingTrackbackElement)

                iterationDrivingDescriptor.astElement = iterationDrivingDescriptor.astElement.childrens[iterationDrivingDescriptor.astElementIndex]
                iterationDrivingDescriptor.astElementIndex = 0

            elif astElementType == EnumAbstractSyntaxTreeNodeType.ONEWAYCONDITION:
                # TODO
                pass

            elif astElementType == EnumAbstractSyntaxTreeNodeType.NOP:
                iterationDrivingDescriptor.astElementIndex += 1

                deleteThisDrivingDescriptor = False

                if iterationDrivingDescriptor.astElementIndex >= iterationDrivingDescriptor.astElement.childrens:
                    deleteThisDrivingDescriptor = True

                    if len(iterationDrivingDescriptor.traceback) == 0:
                        # driving finished execution
                        pass
                    else:

                        tracebackObject = iterationDrivingDescriptor.traceback.pop()

                        createdDrivingDescriptor = iterationDrivingDescriptor.copy()
                        createdDrivingDescriptor.astElement = tracebackObject.astElement
                        createdDrivingDescriptor.astElementIndex = tracebackObject.astElementIndex

                        self._drivingDescriptors.append(createdDrivingDescriptor)

                if deleteThisDrivingDescriptor:
                    del self._drivingDescriptors[drivingDescriptorIndex]
                    drivingDescriptorIndex -= 1

            elif astElementType == EnumAbstractSyntaxTreeNodeType.CONTINUE:
                # inform the generalisation that a continue happend, so it can fold it
                # ASK< correct way to inform it? >
                self._drivingGraph.addElement(GraphElement(DrivingGraphElement(EnumDrivingGraphElementContentType.CONTINUE)))
                newOutputgraphIndex = len(self._drivingGraph.elements)-1
                self._drivingGraph.elements[iterationDrivingDescriptor.outputGraphIndex].childIndices.append(newOutputgraphIndex)

                currentAstElement = iterationDrivingDescriptor.astElement

                iterationDrivingDescriptor.astElement = currentAstElement
                iterationDrivingDescriptor.astElementIndex = 0

            elif astElementType == EnumAbstractSyntaxTreeNodeType.ASSIGNMENT:


                # check if left side is a identifier
                # TODO< could also be a object access, array access, etc >
                #       depends also on the used language
                if iterationDrivingDescriptor.astElement.childrens[iterationDrivingDescriptor.astElementIndex].leftSide.type != EnumAbstractSyntaxTreeNodeType.IDENTIFIER:
                    raise DrivingException("Left side of assignment must be an identifier")

                # we only handle variablenames on the left side

                leftSideVariableName = iterationDrivingDescriptor.astElement.childrens[iterationDrivingDescriptor.astElementIndex].leftSide.name

                if iterationDrivingDescriptor.astElement.childrens[iterationDrivingDescriptor.astElementIndex].rightSide.type == EnumAbstractSyntaxTreeNodeType.CONSTANT:
                    rightSideConstantValue = iterationDrivingDescriptor.astElement.childrens[iterationDrivingDescriptor.astElementIndex].rightSide.value

                    # set variable in variable manager to a fixed value or adapt value and set constantness to changable

                    drivingVariable = None
                    variableExistsAlready = iterationDrivingDescriptor.variableContainer.existVariableByName(leftSideVariableName)
                    if variableExistsAlready:
                        drivingVariable = iterationDrivingDescriptor.variableContainer.lookupVariableByName(leftSideVariableName)
                        drivingVariable.value.constness = EnumDrivingVariableConstness.NONCONSTANT
                    else:
                        drivingVariable = DrivingVariable()
                        drivingVariable.name = leftSideVariableName
                        drivingVariable.value = DrivingValue(EnumTypeNature.BUILDIN)
                        # TODO< type depends on left hand side type >
                        drivingVariable.value.boundTypeInformation.buildinType = EnumBuildinType.INT
                        drivingVariable.value.constness = EnumDrivingVariableConstness.CONSTANT

                        iterationDrivingDescriptor.variableContainer.addVariable(drivingVariable)

                    drivingVariable.value.buildinValue = rightSideConstantValue


                    # write out the done variable assignment

                    # write out the assigned variable
                    # NOTE< is it correct to give the whole path in
                    #       actually we want to assign te new value to a residual variable and the variable itself if it is a non-BUILDIN
                    #     >
                    self._writeoutVariableAssignment([leftSideVariableName], drivingVariable.value, iterationDrivingDescriptor.outputGraphIndex)
                else:
                    raise DrivingException("Constant expected")

                iterationDrivingDescriptor.astElementIndex += 1

            elif astElementType == EnumAbstractSyntaxTreeNodeType.ASSIGNMENTOPERATION:
                currentNode = iterationDrivingDescriptor.astElement.childrens[iterationDrivingDescriptor.astElementIndex]

                interpretedResultValue = AbstractSyntaxTreeInterpreter.interpretAndCalculateValue(currentNode, iterationDrivingDescriptor.variableContainer, self._typeOperationPolicy)

                # assert on assignment
                assert interpretedResultValue.boundedVariableName != None

                # assign variable
                # TODO< concrete path to the variable, because of arrays, oop, etc >
                self._assignValueToVariable([interpretedResultValue.boundedVariableName], interpretedResultValue.value, iterationDrivingDescriptor.variableContainer)

                # write out the assigned variable
                # NOTE< is it correct to give the whole path in
                #       actually we want to assign te new value to a residual variable and the variable itself if it is a non-BUILDIN
                #     >
                self._writeoutVariableAssignment([interpretedResultValue.boundedVariableName], interpretedResultValue.value, iterationDrivingDescriptor.outputGraphIndex)

                iterationDrivingDescriptor.astElementIndex += 1

            elif astElementType == EnumAbstractSyntaxTreeNodeType.VARIABLEDECLARATION:
                self._interpretVariableDeclaration(iterationDrivingDescriptor.astElement.childrens[iterationDrivingDescriptor.astElementIndex], iterationDrivingDescriptor)

            elif astElementType == EnumAbstractSyntaxTreeNodeType.TWOWAYIF:
                self._interpretTwoWayIf(iterationDrivingDescriptor.astElement.childrens[iterationDrivingDescriptor.astElementIndex], iterationDrivingDescriptor)

            else:
                raise InternalErrorException("Unreachable!")

            drivingDescriptorIndex += 1

    class EnumTakeOverloadedOperatorsIntoAccount(object):
        YES = 1
        NO = 0

    def _interpretTwoWayIf(self, twoWayIf: TwoWayIfAbstractSyntaxTreeNode, drivingDescriptor: DrivingDescriptor):
        # first we need to evaluate the expression into a boolean value
        # for that we need to check if the <residual> is completly statically evaluable
        # if not, we have to writeout the expression completly

        conditionIsResidualEvaluated = False
        conditionResidualValue = False

        # NOTE< _calculateExpressionAndWriteoutNonresidualsIfNeeded() writes out the non-<residual> allready >
        residualInfoOfEvaluatedExpression = self._calculateExpressionAndWriteoutNonresidualsIfNeeded(twoWayIf.expression, drivingDescriptor.variableContainer)

        if residualInfoOfEvaluatedExpression.isResidual:
            residualValue = residualInfoOfEvaluatedExpression.residual.value

            toCastType = BoundTypeInformation(EnumTypeNature.BUILDIN)
            toCastType.buildinType = "bool"

            # check if the residual value is a bool or implicit castable,
            # we ask the typeOperationPolicy
            # if the expression of an if is implicit castable to bool or have to be a bool
            if self._typeOperationPolicy.isConditionTypeImplicitCastableToBool():
                # we ask if the type is castable to bool
                # must also take eventually overloaded castingoperators into account

                if not self._isTypeCastableToType(residualValue.boundTypeInformation, toCastType, Supercompiler.EnumTakeOverloadedOperatorsIntoAccount.YES):
                    raise DrivingException("Type is not (implicitly) castable to bool!")
            else:
                if residualValue.boundTypeInformation.typeNature != EnumTypeNature.BUILDIN or residualValue.boundTypeInformation.buildinType != "bool":
                    raise DrivingException("Expression in if must be a bool!")

            # decide if cast to bool is needed
            isCastToBoolNeeded = residualValue.boundTypeInformation.typeNature != EnumTypeNature.BUILDIN or residualValue.boundTypeInformation.buildinType != "bool"

            # do cast to bool if neccessary (and allowed)
            castedResidualValue = None
            if isCastToBoolNeeded:
                castedResidualValue = self._typeOperationPolicy.getCastValueToType(residualValue, toCastType)
            else:
                castedResidualValue = residualValue

            # just to make sure we don't accidentially use the value
            del residualValue

            # transfer it into the function body
            conditionIsResidualEvaluated = True
            conditionResidualValue = castedResidualValue.buildinValue
        else:
            # TODO< ensure that the writout contains a assignment to a anonymous boolean variable >
            # TODO< writeout thing to transfer value to bool variable in the writeout >

            # TODO
            assert False, "TODO"

            conditionIsResidualEvaluated = False



        # check condition on <residual> if possible
        #       if it is possible, write out a hint that the if was evaluated with true
        #       and continue with the interpretation of the body as the next step >
        #
        #       if it is not possible, writeout if hint, open the two branches and create two descriptors which continue in the two branches
        #       drop this descriptor

        if conditionIsResidualEvaluated:
            # writeout hint of taken path
            # TODO< check if last element is a hint and append the hint to the hint >
            createdHint = DrivingGraphHintElement.SingleHint(DrivingGraphHintElement.SingleHint.EnumType.CONDITIONPATHTAKEN)
            createdHint.astElement = twoWayIf
            createdHint.takenPath = conditionResidualValue

            hintElement = DrivingGraphHintElement()
            hintElement.hints.append(createdHint)

            self._drivingGraph.addElement(GraphElement(hintElement))


            # push object of hint together with the astnode on a stack
            # NOTE< this is used to write a hint if the scope of the if is exited >
            drivingTrackbackElement = DrivingTrackbackElement()
            drivingTrackbackElement.astElement = drivingDescriptor.astElement
            drivingTrackbackElement.astElementIndex = drivingDescriptor.astElementIndex + 1
            drivingTrackbackElement.hints.append(createdHint)

            drivingDescriptor.traceback.append(drivingTrackbackElement)


            # update sate so the right branch is executed next
            drivingDescriptor.astElementIndex = 0
            if conditionResidualValue:
                drivingDescriptor.astElement = twoWayIf.trueBody
            else:
                drivingDescriptor.astElement = twoWayIf.falseBody

        else:
            # TODO
            assert False, "TODO"

    def _interpretVariableDeclaration(self, variableDeclarationNode: VariableDeclarationAbstractSyntaxTreeNode, drivingDescriptor: DrivingDescriptor):
        # NOTE< only imperative languages where declaration of variables is necessary use this code >

        # TODO< this does handle only <residual>s, we need code for non-residuals >

        # TODO< lookup the top variablecontainer
        #       for now we take the only variable container >
        topVariableContainer = drivingDescriptor.variableContainer

        if topVariableContainer.existVariableByName(variableDeclarationNode.variableName):
            raise DrivingException("Variable definition for variable {0} redefines allready defined variable!".format(variableDeclarationNode.variableName))

        self._declareVariable(variableDeclarationNode.variableName, topVariableContainer)

        if variableDeclarationNode.rightSide != None:
            # interpret the right side

            resultOnRightSideWithResidualInfo = self._calculateExpressionAndWriteoutNonresidualsIfNeeded(variableDeclarationNode.rightSide, topVariableContainer)

            # we only handle the residual case until now
            assert resultOnRightSideWithResidualInfo.isResidual
            resultOnRightSide = resultOnRightSideWithResidualInfo.residual

            assignedVariable = DrivingVariable()
            assignedVariable.name = variableDeclarationNode.variableName
            assignedVariable.value = resultOnRightSide

            self._assignValueToVariable([variableDeclarationNode.variableName], assignedVariable, topVariableContainer)

            # TODO< writeout the variable assignment >
            x = 0

        drivingDescriptor.astElementIndex += 1

    # contains the informations if a variables was only calculated as a <residual>, if so what the residual value is
    # if not it contains the id TODO< is it a id or a key-string or something else > of the variable/object which has written out
    # in the drivingGraph
    class VariableResidualInfo(object):
        def __init__(self, isResidual: bool):
            self.isResidual = isResidual
            self.residual = None # InterpretedResultValue
            self.nonresidualVariableId = None # NOTE< im unsure about the time, is now not used and so not determined >

    # in the case of any nonresiduals it returns the id of the variable
    # it returns also
    def _calculateExpressionAndWriteoutNonresidualsIfNeeded(self, node: AbstractSyntaxTreeNode, variables: DrivingVariableContainer) -> VariableResidualInfo:
        if Supercompiler._doesContainOnlyResiduals(node, variables):
            interpretationResult = AbstractSyntaxTreeInterpreter.interpretAndCalculateValue(node, variables, self._typeOperationPolicy)

            variableResidualInfo = Supercompiler.VariableResidualInfo(True)
            variableResidualInfo.residual = interpretationResult

            return variableResidualInfo
        else:
            # TODO
            assert False, "TODO"

    # checks if all values in the expression or statement of node do have a residual
    @staticmethod
    def _doesContainOnlyResiduals(node: AbstractSyntaxTreeNode, variables: DrivingVariableContainer):
        # TODO

        return True


    # TODO< some mechanism to walk the scopes while searching for the variable
    #       and creation of one if the variable was not found,
    #       or storing it in the top scope >

    def _declareVariable(self, variableName: str, variableContainer: DrivingVariableContainer):
        # is a declaration, can't happen in languages like python

        # a declaration to a variable which exists allready in the scope is invalid
        if variableContainer.existVariableByName(variableName):
            raise DrivingException("Variable definition for variable {0} redefines allready defined variable!".format(variableName))

        createdVariable = DrivingVariable()
        createdVariable.name = variableName
        createdVariable.value = None
        variableContainer.addVariable(createdVariable)

    # TODO< some mechanism to walk the scopes while searching for the variable
    #       and creation of one if the variable was not found,
    #       or storing it in the top scope >

    ## assigns a value to a variable
    #
    # depending on the language policy this does
    # * check if the variable exists
    # * checks if the types are compatible
    # * eventually cast it if types are compatiable but not equal
    # for the final assignment
    def _assignValueToVariable(self, variablePath: [{str, int}], value: DrivingValue, variableContainer: DrivingVariableContainer):
        # TODO< ask language policy about typing and conversion >

        # for now the path must be one element long
        assert len(variablePath) == 1

        # NOTE< for now we assign values even to unknown variables, this is python style and not compatible with c#, java, etc >
        # TODO< ask language policy about semantics of variable assignment to not jet defined variables >

        if variableContainer.existVariableByName(variablePath[0]):
            variableContainer.setVariableByName(variablePath[0], value)
        else:
            createdVariable = DrivingVariable()
            createdVariable.name = variablePath[0]
            createdVariable.value = value
            variableContainer.addVariable(createdVariable)

    def _writeoutVariableAssignment(self, variablePath: [{str, int}], value: DrivingValue, outputGraphIndex: int):
        # for now the path must be one element long
        assert len(variablePath) == 1

        self._drivingGraph.addElement(GraphElement(DrivingGraphAssignmentElement()))
        newOutputgraphIndex = len(self._drivingGraph.elements)-1
        self._drivingGraph.elements[outputGraphIndex].childIndices.append(newOutputgraphIndex)

        self._drivingGraph.elements[newOutputgraphIndex].content.leftVariableName = variablePath[0]

        # for now it must be a buildin value
        assert value.boundTypeInformation.typeNature == EnumTypeNature.BUILDIN
        self._drivingGraph.elements[newOutputgraphIndex].content.rightExpression = ConstantExpression(value.buildinValue)

    def _isTypeCastableToType(self, fromCastType: BoundTypeInformation, toCastType: BoundTypeInformation, EnumTakeOverloadedOperatorsIntoAccount):
        # not implemented yet because it is currently not used
        assert False, "TODO"

# example without parser
from AbstractSyntaxTree.SequenceAbstractSyntaxTreeNode import SequenceAbstractSyntaxTreeNode
from AbstractSyntaxTree.IdentifierAbstractSyntaxTreeNode import IdentifierAbstractSyntaxTreeNode
from AbstractSyntaxTree.AssignmentAbstractSyntaxTreeNode import AssignmentAbstractSyntaxTreeNode
from AbstractSyntaxTree.ConstantAbstractSyntaxTreeNode import ConstantAbstractSyntaxTreeNode
from AbstractSyntaxTree.LoopAbstractSyntaxTreeNode import LoopAbstractSyntaxTreeNode
from AbstractSyntaxTree.AssignmentOperationAbstractSyntaxTreeNode import AssignmentOperationAbstractSyntaxTreeNode
from AbstractSyntaxTree.ContinueAbstractSyntaxTreeNode import ContinueAbstractSyntaxTreeNode

from AbstractSyntaxTree.EnumBinaryOperationType import EnumBinaryOperationType

supercompiler = Supercompiler()
supercompiler._ast = SequenceAbstractSyntaxTreeNode()

from Frontend.Java.Parser import Parser

parser = Parser()

supercompiler._ast.childrens = parser._init()

"""
supercompiler._ast.childrens.append(AssignmentAbstractSyntaxTreeNode())
supercompiler._ast.childrens[0].leftSide = IdentifierAbstractSyntaxTreeNode("a")
supercompiler._ast.childrens[0].rightSide = ConstantAbstractSyntaxTreeNode()
supercompiler._ast.childrens[0].rightSide.value = 5

supercompiler._ast.childrens.append(AssignmentAbstractSyntaxTreeNode())
supercompiler._ast.childrens[1].leftSide = IdentifierAbstractSyntaxTreeNode("b")
supercompiler._ast.childrens[1].rightSide = ConstantAbstractSyntaxTreeNode()
supercompiler._ast.childrens[1].rightSide.value = 0

supercompiler._ast.childrens.append(LoopAbstractSyntaxTreeNode())

supercompiler._ast.childrens[2].childrens.append(AssignmentOperationAbstractSyntaxTreeNode(EnumBinaryOperationType.ADD))

supercompiler._ast.childrens[2].childrens[0].leftSide = IdentifierAbstractSyntaxTreeNode("b")
supercompiler._ast.childrens[2].childrens[0].rightSide = IdentifierAbstractSyntaxTreeNode("a")

supercompiler._ast.childrens[2].childrens.append(ContinueAbstractSyntaxTreeNode())


#supercompiler._ast = LoopAbstractSyntaxTreeNode()
#supercompiler._ast.childrens.append(ContinueAbstractSyntaxTreeNode())
"""

supercompiler._drivingDescriptors.append(DrivingDescriptor())
supercompiler._drivingDescriptors[0].astElement = supercompiler._ast
supercompiler._drivingDescriptors[0].astElementIndex = 0
supercompiler._drivingDescriptors[0].outputGraphIndex = 0

supercompiler._typeOperationPolicy = JavaTypeOperationPolicy()

supercompiler._drive()

# simple example todo

# int a = 5;
# int b = 0;
#
# while(True) {
#    if (a == 0)
#       break
#    b += a;
#    a -= 1;
# }

# results in
# a = 5
# b = 0
# b += 5
# a -= 1
# b += 4
# a -= 1
# b += 3
# a -= 1
# b += 2
# a -= 1
# b += 1
# a -= 1
