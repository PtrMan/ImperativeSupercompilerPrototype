from Frontend.Java.VariableDeclarationFrontendAstElement import VariableDeclarationFrontendAstElement
from Frontend.Java.FrontendAstElement import FrontendAstElement
from Frontend.Java.EnumFrontendAstElementType import EnumFrontendAstElementType
from Frontend.Java.JavaTypeFrontendAstElement import JavaTypeFrontendAstElement

from Driving.BoundTypeInformation import BoundTypeInformation
from Driving.EnumTypeNature import EnumTypeNature

from DrivingGraphExpressions.Expression import Expression as DrivingGraphExpression
from DrivingGraphExpressions.BinaryExpression import BinaryExpression as DrivingGraphBinaryExpression
from DrivingGraphExpressions.VariableIdentifierExpression import VariableIdentifierExpression as DrivingGraphVariableIdentifierExpression

from AbstractSyntaxTree.VariableDeclarationAbstractSyntaxTreeNode import VariableDeclarationAbstractSyntaxTreeNode

## rewrites a tree from a Frontend Tree to an AST Tree
#
# is necessary because only with this the Supercompiler can work on a General AST while the Frontend Parts can work on language specific representations
class TreeRewriter(object):
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
                    drivingGraphExpression = TreeRewriter._convertJavaAstExpressionToDrivingGraphExpression(iterationVariableDeclarator.variableInitializer.expression)

                    # then we create a Ast Variable-Declaration and add it to the result list
                    resultVariableDeclaration.rightside = drivingGraphExpression

            resultList.append(resultVariableDeclaration)

        return resultList

    @staticmethod
    def _convertJavaAstExpressionToDrivingGraphExpression(astElement: FrontendAstElement) -> DrivingGraphExpression:
        if astElement.type == EnumFrontendAstElementType.BINARYOPERATION:
            convertedLeftElement = TreeRewriter._convertJavaAstExpressionToDrivingGraphExpression(astElement.leftElement)
            convertedRightElement = TreeRewriter._convertJavaAstExpressionToDrivingGraphExpression(astElement.rightElement)

            operationIsWithoutAssignment = not astElement.isAssignment

            if not operationIsWithoutAssignment:
                # TODO< allow and translate somehow binary assignments >
                # TODO< raise Exception "Binary operations with assignment are not allowed" >
                assert False

            return DrivingGraphBinaryExpression(convertedLeftElement, convertedRightElement, astElement.operationType)

        elif astElement.type == EnumFrontendAstElementType.IDENTIFIER:
            # TODO< is the variable identifier correct ? >
            return DrivingGraphVariableIdentifierExpression(astElement.variableName)

        # TODO< numeric literal >
        else:
            # TODO< raise exception >
            assert False

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