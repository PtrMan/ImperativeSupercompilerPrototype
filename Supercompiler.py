# small prototype for a supercompiler

# TODO
# - how to handle types in typed languages/interpreted languages (assignment, etc)
#   needs a implementable variable type conversion system

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


class EnumDrivingGraphElementContentType(object):
    NOP = 0
    CONTINUE = 1 # if an explicit or implicit continue of a loop was executed, is actually a nop
    ASSIGNMENT = 2

class EnumVariableType(object):
    INTEGER = 0


class Value(object):
    def __init__(self, type):
        self.type = type

        self.valueInt = 0

class DrivingGraphElement(object):
    def __init__(self, type):
        self.type = type

class DrivingGraphAssignmentElement(DrivingGraphElement):
    def __init__(self):
        super(DrivingGraphAssignmentElement, self).__init__(EnumDrivingGraphElementContentType.ASSIGNMENT)

        self.leftVariableName = None
        self.rightExpression = None # must be derived from DrivingGraphExpressions.Expression
                                    # is the expression which gets evaluated for the value of the variable







#class RootAbstractSyntaxTreeNode(AbstractSyntaxTreeNode):
#    def __init__(self):
#        super(RootAbstractSyntaxTreeNode, self).__init__(EnumAbstractSyntaxTreeNodeType.ROOT)






from Driving.DrivingValue import DrivingValue

from Driving.DrivingVariableContainer import DrivingVariableContainer

class DrivingDescriptor(object):
    def __init__(self):
        self.astElement = None  # the current abstract syntax element which is "executed" next
        self.astElementIndex = None

        # used to store and lookup variables
        # which are instances of "DrivingVariable"
        self.variableContainer = DrivingVariableContainer()
        self.outputGraphIndex = None  # index of the root Graph element where the next nodes are appended

        # tupes of the form (astElement, astElementIndex)
        # note that the index _can_ be outside the valid range, if so the execution/driving needs to break out of the next layer and so on
        self.traceback = []

    def copy(self):
        createdDescriptor = DrivingDescriptor()
        createdDescriptor.astElement = self.astElement
        createdDescriptor.astElementIndex = self.astElementIndex
        createdDescriptor.variableContainer = self.variableContainer.copy()
        createdDescriptor.outputGraphIndex = self.outputGraphIndex
        createdDescriptor.traceback = self.traceback

        return createdDescriptor

from Driving.AbstractSyntaxTreeInterpreter import AbstractSyntaxTreeInterpreter
from Driving.Java.JavaTypeOperationPolicy import JavaTypeOperationPolicy
from AbstractSyntaxTree.EnumAbstractSyntaxTreeNodeType import EnumAbstractSyntaxTreeNodeType
from Driving.EnumDrivingVariableConstness import EnumDrivingVariableConstness
from Driving.EnumTypeNature import EnumTypeNature
from Driving.EnumBuildinType import EnumBuildinType
from Driving.DrivingVariable import DrivingVariable

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



            if iterationDrivingDescriptor.astElement.childrens[iterationDrivingDescriptor.astElementIndex].type == EnumAbstractSyntaxTreeNodeType.LOOP:
                iterationDrivingDescriptor.traceback.append((iterationDrivingDescriptor.astElement, iterationDrivingDescriptor.astElementIndex + 1))

                iterationDrivingDescriptor.astElement = iterationDrivingDescriptor.astElement.childrens[iterationDrivingDescriptor.astElementIndex]
                iterationDrivingDescriptor.astElementIndex = 0

            elif iterationDrivingDescriptor.astElement.childrens[iterationDrivingDescriptor.astElementIndex].type == EnumAbstractSyntaxTreeNodeType.ONEWAYCONDITION:
                # TODO
                pass

            elif iterationDrivingDescriptor.astElement.childrens[iterationDrivingDescriptor.astElementIndex].type == EnumAbstractSyntaxTreeNodeType.NOP:
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
                        createdDrivingDescriptor.astElement = tracebackObject[0]
                        createdDrivingDescriptor.astElementIndex = tracebackObject[1]

                        self._drivingDescriptors.append(createdDrivingDescriptor)

                if deleteThisDrivingDescriptor:
                    del self._drivingDescriptors[drivingDescriptorIndex]
                    drivingDescriptorIndex -= 1

            elif iterationDrivingDescriptor.astElement.childrens[iterationDrivingDescriptor.astElementIndex].type == EnumAbstractSyntaxTreeNodeType.CONTINUE:
                # inform the generalisation that a continue happend, so it can fold it
                # ASK< correct way to inform it? >
                self._drivingGraph.addElement(GraphElement(DrivingGraphElement(EnumDrivingGraphElementContentType.CONTINUE)))
                newOutputgraphIndex = len(self._drivingGraph.elements)-1
                self._drivingGraph.elements[iterationDrivingDescriptor.outputGraphIndex].childIndices.append(newOutputgraphIndex)

                currentAstElement = iterationDrivingDescriptor.astElement

                iterationDrivingDescriptor.astElement = currentAstElement
                iterationDrivingDescriptor.astElementIndex = 0

            elif iterationDrivingDescriptor.astElement.childrens[iterationDrivingDescriptor.astElementIndex].type == EnumAbstractSyntaxTreeNodeType.ASSIGNMENT:


                # check if left side is a identifier
                # TODO< could also be a object access, array access, etc >
                #       depends also on the used language
                if iterationDrivingDescriptor.astElement.childrens[iterationDrivingDescriptor.astElementIndex].leftSide.type != EnumAbstractSyntaxTreeNodeType.IDENTIFIER:
                    # TODO< throw exception
                    assert False

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
                    # TODO< throw exception
                    assert False

                iterationDrivingDescriptor.astElementIndex += 1

            elif iterationDrivingDescriptor.astElement.childrens[iterationDrivingDescriptor.astElementIndex].type == EnumAbstractSyntaxTreeNodeType.ASSIGNMENTOPERATION:
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

            else:
                assert False

            drivingDescriptorIndex += 1

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

supercompiler._drivingDescriptors.append(DrivingDescriptor())
supercompiler._drivingDescriptors[0].astElement = supercompiler._ast
supercompiler._drivingDescriptors[0].astElementIndex = 0
supercompiler._drivingDescriptors[0].outputGraphIndex = 0

supercompiler._typeOperationPolicy = JavaTypeOperationPolicy()

supercompiler._drive()

# simple example todo

# a = 5
# b = 0
# while True:
#    if a == 0:
#       break
#    b += a
#    a -= 1

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
