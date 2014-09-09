# small prototype for a supercompiler

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

class EnumVariableType(object):
    INTEGER = 0

class Value(object):
    def __init__(self, type):
        self.type = type

        self.valueInt = 0

class DrivingGraphElementContent(object):
    def __init__(self, type):
        self.type = type


class EnumAbstractSyntaxTreeNodeType(object):
    LOOP = 0
    ONEWAYCONDITION = 1
    CONTINUE = 2
    NOP = 3  # for testing
    ROOT = 4 # pseudo, only the top element can be a root element
    ASSIGMENT = 5
    CONSTANT = 6
    IDENTIFIER = 7

class AbstractSyntaxTreeNode(object):
    def __init__(self, type):
        self.type = type

        self.childrens = []


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

class ConstantAbstractSyntaxTreeNode(AbstractSyntaxTreeNode):
    def __init__(self):
        super(ConstantAbstractSyntaxTreeNode, self).__init__(EnumAbstractSyntaxTreeNodeType.CONSTANT)

        self.value = None # type is "Value"

class IdentifierAbstractSyntaxTreeNode(AbstractSyntaxTreeNode):
    def __init__(self, name):
        super(IdentifierAbstractSyntaxTreeNode, self).__init__(EnumAbstractSyntaxTreeNodeType.IDENTIFIER)

        self.name = name

class DrivingVariable(object):
    def __init__(self):
        self.name = None

        self.value = None # type is "Value"


class DrivingDescriptor(object):
    def __init__(self):
        self.astElement = None  # the current abstract syntax element which is "executed" next
        self.astElementIndex = None

        self.variables = []  # instances of "DrivingVariable"
        self.outputGraphIndex = None  # index of the root Graph element where the next nodes are appended

        # tupes of the form (astElement, astElementIndex)
        # note that the index _can_ be outside the valid range, if so the execution/driving needs to break out of the next layer and so on
        self.traceback = []

    def copy(self):
        createdDescriptor = DrivingDescriptor()
        createdDescriptor.astElement = self.astElement
        createdDescriptor.astElementIndex = self.astElementIndex
        createdDescriptor.variables = self.variables
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

        self._drivingGraph.addElement(GraphElement(DrivingGraphElementContent(EnumDrivingGraphElementContentType.NOP)))

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

            elif iterationDrivingDescriptor.astElement.childrens[
                iterationDrivingDescriptor.astElementIndex].type == EnumAbstractSyntaxTreeNodeType.ONEWAYCONDITION:
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
                currentAstElement = iterationDrivingDescriptor.astElement

                iterationDrivingDescriptor.astElement = currentAstElement
                iterationDrivingDescriptor.astElementIndex = 0

            else:
                assert False

            drivingDescriptorIndex += 1


supercompiler = Supercompiler()
supercompiler._ast = LoopAbstractSyntaxTreeNode()
supercompiler._ast.childrens.append(ContinueAbstractSyntaxTreeNode())

supercompiler._drivingDescriptors.append(DrivingDescriptor())
supercompiler._drivingDescriptors[0].astElement = supercompiler._ast
supercompiler._drivingDescriptors[0].astElementIndex = 0

supercompiler.drive()

# TODO< assigment, variable creation/retrival for Driving descriptor >

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
