from AbstractSyntaxTree.NonscopedSequenceAbstractSyntaxTreeNode import NonscopedSequenceAbstractSyntaxTreeNode
from Exceptions.InternalErrorException import InternalErrorException
from Exceptions.TodoException import TodoException

from Frontend.Java.BlockFrontendAstElement import BlockFrontendAstElement
from Frontend.Java.LocalVariableDeclarationFrontendAstElement import LocalVariableDeclarationFrontendAstElement
from Frontend.Java.TypeFrontendAstElement import TypeFrontendAstElement
from Frontend.Java.VariableDeclarationFrontendAstElement import VariableDeclarationFrontendAstElement
from Frontend.Java.FrontendAstElement import FrontendAstElement
from Frontend.Java.EnumFrontendAstElementType import EnumFrontendAstElementType
from Frontend.Java.JavaTypeFrontendAstElement import JavaTypeFrontendAstElement
from Frontend.Java.BinaryOperationFrontendAstElement import BinaryOperationFrontendAstElement
from Frontend.Java.TakeFirstAstElement import TakeFirstAstElement
from Frontend.Java.IfStatementAstElement import IfStatementAstElement

from Driving.BoundTypeInformation import BoundTypeInformation
from Driving.EnumTypeNature import EnumTypeNature

from AbstractSyntaxTree.AbstractSyntaxTreeNode import AbstractSyntaxTreeNode
from AbstractSyntaxTree.IdentifierAbstractSyntaxTreeNode import IdentifierAbstractSyntaxTreeNode
from AbstractSyntaxTree.BinaryOperationAbstractSyntaxTreeNode import BinaryOperationAbstractSyntaxTreeNode
from AbstractSyntaxTree.IntegerLiteralSyntaxTreeNode import IntegerLiteralSyntaxTreeNode
from AbstractSyntaxTree.EnumBinaryOperationType import EnumBinaryOperationType
from AbstractSyntaxTree.SequenceAbstractSyntaxTreeNode import SequenceAbstractSyntaxTreeNode

from AbstractSyntaxTree.VariableDeclarationAbstractSyntaxTreeNode import VariableDeclarationAbstractSyntaxTreeNode
from AbstractSyntaxTree.TwoWayIfAbstractSyntaxTreeNode import TwoWayIfAbstractSyntaxTreeNode

## rewrites a tree from a Frontend Tree to an AST Tree
#
# is necessary because only with this the Supercompiler can work on a General AST while the Frontend Parts can work on language specific representations
from Frontend.Java.VariableInitializerFrontendAstElement import VariableInitializerFrontendAstElement


class TreeRewriter(object):
    @staticmethod
    def rewriteSingleElement(astElement: FrontendAstElement) -> AbstractSyntaxTreeNode:
        if astElement.type == EnumFrontendAstElementType.IDENTIFIER:
            return TreeRewriter._convertJavaAstExpressionToGeneralAst(astElement)
        elif astElement.type == EnumFrontendAstElementType.TAKEFIRST:
            return TreeRewriter._rewriteTakeFirst(astElement)
        elif astElement.type == EnumFrontendAstElementType.BINARYOPERATION:
            return TreeRewriter._rewriteBinaryOperation(astElement)
        elif astElement.type == EnumFrontendAstElementType.IF:
            return TreeRewriter._rewriteIf(astElement)
        elif astElement.type == EnumFrontendAstElementType.VARIABALEDECLARATIONS:
            return TreeRewriter.rewriteVariableDeclaration(astElement)
        elif astElement.type == EnumFrontendAstElementType.BLOCK:
            return TreeRewriter._rewriteBlock(astElement)
        elif astElement.type == EnumFrontendAstElementType.LOCALVARIABLEDECLARATION:
            return TreeRewriter._rewriteLocalVariableDeclaration(astElement)
        else:
            raise InternalErrorException("Unhandled astElement.type")

    @staticmethod
    def _rewriteIf(ifStatement: IfStatementAstElement) -> TwoWayIfAbstractSyntaxTreeNode:
        resultAstNode = TwoWayIfAbstractSyntaxTreeNode()
        resultAstNode.expression = TreeRewriter.rewriteSingleElement(ifStatement.conditionExpression)
        resultAstNode.trueBody = TreeRewriter.rewriteSingleElement(ifStatement.trueBody)

        if ifStatement.elseBody != None:
            resultAstNode.elseBody = TreeRewriter.rewriteSingleElement(ifStatement.elseBody)

    @staticmethod
    def _rewriteTakeFirst(takeFirst: TakeFirstAstElement) -> AbstractSyntaxTreeNode:
        return TreeRewriter.rewriteSingleElement(takeFirst.element)

    @staticmethod
    def _rewriteBinaryOperation(binaryOperationJavaAst: BinaryOperationFrontendAstElement) -> BinaryOperationAbstractSyntaxTreeNode:
        return TreeRewriter._convertJavaAstExpressionToGeneralAst(binaryOperationJavaAst)

    @staticmethod
    def _rewriteBlock(blockStatement: BlockFrontendAstElement) -> SequenceAbstractSyntaxTreeNode:
        resultAstNode = SequenceAbstractSyntaxTreeNode()

        for iterationFrontendAstElement in blockStatement.elements:
            resultAstNode.childrens.append(TreeRewriter.rewriteSingleElement(iterationFrontendAstElement))

        return resultAstNode

    # rewrites an VariableDeclarationFrontendAstElement to one or many assignment statements
    # the array initialisators are rewritten too
    @staticmethod
    def rewriteVariableDeclaration(variableDeclarationJavaAst: VariableDeclarationFrontendAstElement) -> [VariableDeclarationAbstractSyntaxTreeNode]:
        resultList = []

        # extract and translate type to BoundTypeInformation
        boundTypeInformation = TreeRewriter._translateJavaTypeToBoundTypeinformation(variableDeclarationJavaAst.javaType)

        # go through each variable declaration and try to create a VariableDeclarationAbstractSyntaxTreeNode for it

        variableDeclarators = variableDeclarationJavaAst.variableDeclarators
        for iterationVariableDeclarator in variableDeclarators:
            # TODO< declarator with brackets >
            assert not iterationVariableDeclarator.hasBrackets, "Declarator with Brackets not jet supported"


            resultVariableDeclaration = VariableDeclarationAbstractSyntaxTreeNode(boundTypeInformation, iterationVariableDeclarator.declarationVariablenameIdentifier.identifierAsString)

            if iterationVariableDeclarator.variableInitializer != None:
                # check if the initializer is a simple expression
                if iterationVariableDeclarator.variableInitializer.withInitialisationArray:
                    assert False, "TODO"
                else:
                    # first we translate the Java Ast for the Expression to a DrivingGraphExpression
                    drivingGraphExpression = TreeRewriter._convertJavaAstExpressionToGeneralAst(iterationVariableDeclarator.variableInitializer.expression)

                    # then we create a Ast Variable-Declaration and add it to the result list
                    resultVariableDeclaration.rightSide = drivingGraphExpression

            resultList.append(resultVariableDeclaration)

        return resultList

    @staticmethod
    def _rewriteLocalVariableDeclaration(localVariableDeclarationJavaAst: LocalVariableDeclarationFrontendAstElement):
        ## translates the type to a bound type, if possible
        # modifiers can be []
        def getBoundType():
            modifiers = localVariableDeclarationJavaAst.modifiers
            type = localVariableDeclarationJavaAst.type2

            if len(modifiers) > 0:
                # TODO
                raise TodoException("modifiers need to be implemented")

            if type.type2 == TypeFrontendAstElement.EnumType.BASICTYPE:
                resultBoundType = BoundTypeInformation(EnumTypeNature.BUILDIN)
                resultBoundType.buildinType = type.basicType

                return resultBoundType
            elif type.type2 == TypeFrontendAstElement.EnumType.REFERENCETYPE:
                # TODO
                raise TodoException("reference types are currently not supported")

        # convertVariableInitialisizer can be None, in this case it returns None
        def convertVariableInitialisizer(variableDeclarator : VariableInitializerFrontendAstElement):
            if variableDeclarator == None:
                return None
            # else here

            # TODO< declarator needs type, if it is a expression or a array thingy >
            if variableDeclarator.expression == None:
                # TODO
                raise TodoException("Non expressions as an initialisizer are not supported yet!")
            else:
                # declarator is an expression, convert it
                return TreeRewriter.rewriteSingleElement(variableDeclarator.expression)

        baseBoundType = getBoundType()

        variableDeclarators = localVariableDeclarationJavaAst.variableDeclaratorsObject

        if len(variableDeclarators.declarators) == 0:
            raise InternalErrorException("len(variableDeclarators.declarators) is zero, which is impossible")

        resultNonscopedSequence = NonscopedSequenceAbstractSyntaxTreeNode()

        for iterationVariableDeclarator in variableDeclarators.declarators:
            if iterationVariableDeclarator.hasBrackets:
                # TODO
                raise TodoException("bracket 'modifiers' are currently not supported")

            variablename = iterationVariableDeclarator.declarationVariablenameIdentifier.identifierAsString
            initialisizerConvertedToAst = convertVariableInitialisizer(iterationVariableDeclarator.variableInitializer)

            variableDeclarationAstNode = VariableDeclarationAbstractSyntaxTreeNode(baseBoundType, variablename)
            variableDeclarationAstNode.rightSide = initialisizerConvertedToAst
            resultNonscopedSequence.childrens.append(variableDeclarationAstNode)

        return resultNonscopedSequence


    @staticmethod
    def _convertJavaAstExpressionToGeneralAst(astElement: FrontendAstElement) -> AbstractSyntaxTreeNode:
        if astElement.type == EnumFrontendAstElementType.BINARYOPERATION:
            convertedLeftElement = TreeRewriter._convertJavaAstExpressionToGeneralAst(astElement.leftElement)
            convertedRightElement = TreeRewriter._convertJavaAstExpressionToGeneralAst(astElement.rightElement)

            if astElement.isAssignment:
                # allow only raw assignments without an operation
                if astElement.operationType == EnumBinaryOperationType.ASSIGNMENT:
                    resultNode = BinaryOperationAbstractSyntaxTreeNode(astElement.operationType)
                    resultNode.leftSide = convertedLeftElement
                    resultNode.rightSide = convertedRightElement

                    return resultNode

                # TODO< allow and translate somehow binary assignments >
                # TODO< raise Exception "Binary operations with assignment are not allowed" >
                assert False

            resultNode = BinaryOperationAbstractSyntaxTreeNode(astElement.operationType)
            resultNode.leftSide = convertedLeftElement
            resultNode.rightSide = convertedRightElement

            return resultNode

        elif astElement.type == EnumFrontendAstElementType.IDENTIFIER:
            return IdentifierAbstractSyntaxTreeNode(astElement.identifierAsString)

        elif astElement.type == EnumFrontendAstElementType.INTEGERLITERAL:
            return IntegerLiteralSyntaxTreeNode(astElement.integer)


        else:
            raise InternalErrorException("Unhandled astElement.type")

    # tries to translate a JavaTypeFrontendAstElement to a Bound Type which can be used for driving
    # for userdefined types this has to be called after the type analysis of the input program
    @staticmethod
    def _translateJavaTypeToBoundTypeinformation(javaType: JavaTypeFrontendAstElement) -> BoundTypeInformation:
        # TODO< translation/lookup for classes and internal java classes >

        if javaType.typeIdentiferElement.identifierAsString == "int" and not javaType.typeHasArray:
            boundType = BoundTypeInformation(EnumTypeNature.BUILDIN)
            boundType.buildinType = "int"

            return boundType
        else:
            # TODO
            assert False, "TODO"