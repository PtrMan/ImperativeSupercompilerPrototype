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

class EnumAbstractSyntaxTreeNodeType(object):
    LOOP = 0
    ONEWAYCONDITION = 1
    CONTINUE = 2
    NOP = 3  # for testing
    ROOT = 4 # pseudo, only the top element can be a root element
    ASSIGNMENT = 5
    CONSTANT = 6
    IDENTIFIER = 7
    SEQUENCE = 8

class EnumBinaryOperationType:
    ADD = 0
    SUB = 1
    MUL = 2
    DIV = 3

class AbstractSyntaxTreeNode(object):
    def __init__(self, type):
        self.type = type

        self.childrens = []

class SequenceAbstractSyntaxTreeNode(AbstractSyntaxTreeNode):
    def __init__(self):
        super(SequenceAbstractSyntaxTreeNode, self).__init__(EnumAbstractSyntaxTreeNodeType.SEQUENCE)

# in the body we need a condition for breaking
# the body are all instructions
class LoopAbstractSyntaxTreeNode(AbstractSyntaxTreeNode):
    def __init__(self):
        super(LoopAbstractSyntaxTreeNode, self).__init__(EnumAbstractSyntaxTreeNodeType.LOOP)


class OneWayAbstractSyntaxTreeNode(AbstractSyntaxTreeNode):
    def __init__(self):
        super(OneWayAbstractSyntaxTreeNode, self).__init__(EnumAbstractSyntaxTreeNodeType.ONEWAYCONDITION)

        self.conditionAstElement = None


# neded for simpler evaluation
class ContinueAbstractSyntaxTreeNode(AbstractSyntaxTreeNode):
    def __init__(self):
        super(ContinueAbstractSyntaxTreeNode, self).__init__(EnumAbstractSyntaxTreeNodeType.CONTINUE)

class RootAbstractSyntaxTreeNode(AbstractSyntaxTreeNode):
    def __init__(self):
        super(RootAbstractSyntaxTreeNode, self).__init__(EnumAbstractSyntaxTreeNodeType.ROOT)

class AssignmentAbstractSyntaxTreeNode(AbstractSyntaxTreeNode):
    def __init__(self):
        super(AssignmentAbstractSyntaxTreeNode, self).__init__(EnumAbstractSyntaxTreeNodeType.ASSIGNMENT)

        self.leftSide = None # instance of AbstractSyntaxTreeNode
        self.rightSide = None # instance of AbstractSyntaxTreeNode

class AssignmentOperationAbstractSyntaxTreeNode(AbstractSyntaxTreeNode):
    def __init__(self, operation: EnumBinaryOperationType):
        super(AssignmentOperationAbstractSyntaxTreeNode, self).__init__(EnumAbstractSyntaxTreeNodeType.ASSIGNMENTOPERATION)

        self.operation = operation

        self.leftSide = None # instance of AbstractSyntaxTreeNode
        self.rightSide = None # instance of AbstractSyntaxTreeNode


class ConstantAbstractSyntaxTreeNode(AbstractSyntaxTreeNode):
    def __init__(self):
        super(ConstantAbstractSyntaxTreeNode, self).__init__(EnumAbstractSyntaxTreeNodeType.CONSTANT)

        self.value = None # type is "Value"

class IdentifierAbstractSyntaxTreeNode(AbstractSyntaxTreeNode):
    def __init__(self, name):
        super(IdentifierAbstractSyntaxTreeNode, self).__init__(EnumAbstractSyntaxTreeNodeType.IDENTIFIER)

        self.name = name

class EnumDrivingVariableConstness(object):
    CONSTANT = 0
    NONCONSTANT = 1
    INVALID = 2 # if it is a object it doesn'T have directly this property

class EnumTypeNature:
    BUILDIN = 0 # it is a build in value, like int, float, double, etc.
    USERDEFINED = 1

class EnumBuildinType:
    INT = 0

# TODO< how to handle residuals and non residuals ??? >
class DrivingValue(object):
    def __init__(self, typeNature: EnumTypeNature):
        self.typeNature = typeNature
        self.buildinType = None # only valid if self.typeNature == EnumBuildinType.BUILDIN

        # gives the supercompiler information if the value was ever changed
        # if it was never changed it can be handled as a real constant
        self.constness = EnumDrivingVariableConstness.INVALID

        # for oop objects this contains the DrivingValues of the variables
        # if it is valid this is a dict
        self.objectValues = None

        # for buildin value this contains the value
        self.buildinValue = None

    ## gets this object/value as a disjuct object which seperates type information and the value
    #
    # this is later needed because copying the whole object is no solution, because most information is redudant (all up to the value)
    def getAsDisjuctTypeValue(self):
        # for simplicity we just return a copy
        return self._copy()

    def _copy(self):
        result = DrivingValue(self.typeNature)
        result.buildinType = self.buildinType
        result.constness = self.constness

        if result.objectValues == None:
            pass
        else:
            result.objectValues = {}

            for iterationKey in self.objectValues.keys():
                result.objectValues[iterationKey] = self.objectValues[iterationKey].getAsDisjuctTypeValue()

        result.buildinValue = self.buildinValue

        return result


class DrivingVariable(object):
    def __init__(self):
        self.name = None

        self.value = None # type is "DrivingValue"

# small layer above the lookup and storage of variables while driving
class DrivingVariableContainer(object):
    def __init__(self):
        # TODO< should be a hashtable for faster lookup >
        self.variables = [] # instances of "DrivingVariable"

    # returns the DrivingVariable instance if found
    # throws VariableLookupException if no variable was found
    def lookupVariableByName(self, name: str) -> DrivingVariable:
        for iterationVariable in self.variables:
            if iterationVariable.name == name:
                return iterationVariable

        assert False

    def existVariableByName(self, name: str) -> bool:
        for iterationVariable in self.variables:
            if iterationVariable.name == name:
                return True

        return False

    def addVariable(self, drivingVariable: DrivingVariable):
        self.variables.append(drivingVariable)

    # TODO
    def copy(self):
        assert False



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


class Supercompiler(object):
    def __init__(self):
        self._drivingGraph = Graph()

        self._ast = None

        # for driving
        self._drivingDescriptors = []

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
                        drivingVariable.value.buildinType = EnumBuildinType.INT
                        drivingVariable.value.constness = EnumDrivingVariableConstness.CONSTANT

                        iterationDrivingDescriptor.variableContainer.addVariable(drivingVariable)

                    drivingVariable.value.buildinValue = rightSideConstantValue


                    # write out the done variable assignment
                    self._drivingGraph.addElement(GraphElement(DrivingGraphAssignmentElement()))
                    newOutputgraphIndex = len(self._drivingGraph.elements)-1
                    self._drivingGraph.elements[iterationDrivingDescriptor.outputGraphIndex].childIndices.append(newOutputgraphIndex)

                    self._drivingGraph.elements[newOutputgraphIndex].content.leftVariableName = leftSideVariableName
                    self._drivingGraph.elements[newOutputgraphIndex].content.rightExpression = ConstantExpression(rightSideConstantValue)
                else:
                    # TODO< throw exception
                    assert False

                iterationDrivingDescriptor.astElementIndex += 1

            else:
                assert False

            drivingDescriptorIndex += 1


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
