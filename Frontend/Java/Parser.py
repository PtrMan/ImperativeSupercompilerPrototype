from Frontend.Java.LocalVariableDeclarationFrontendAstElement import LocalVariableDeclarationFrontendAstElement
from Libs.pyparsing import Literal, alphas, Word, delimitedList, Optional, ZeroOrMore, Forward, oneOf, nums, FollowedBy, OneOrMore, restOfLine
from Frontend.Java.IdentifierFrontendAstElement import IdentifierFrontendAstElement
from Frontend.Java.BinaryOperationFrontendAstElement import BinaryOperationFrontendAstElement
from Frontend.Java.JavaTypeFrontendAstElement import JavaTypeFrontendAstElement
from Frontend.Java.VariableDeclaratorFrontendAstElement import VariableDeclaratorFrontendAstElement
from Frontend.Java.VariableInitializerFrontendAstElement import VariableInitializerFrontendAstElement
from Frontend.Java.VariableDeclarationFrontendAstElement import VariableDeclarationFrontendAstElement
from Frontend.Java.ModifierFrontendAstElement import ModifierFrontendAstElement
from Frontend.Java.IntegerLiteralAstElement import IntegerLiteralAstElement
from Frontend.Java.TakeFirstAstElement import TakeFirstAstElement
from Frontend.Java.IfStatementAstElement import IfStatementAstElement
from Frontend.Java.BlockFrontendAstElement import BlockFrontendAstElement
from Frontend.Java.ReferenceTypeFrontendAstElement import ReferenceTypeFrontendAstElement
from Frontend.Java.TypeArgumentFrontendAstElement import TypeArgumentFrontendAstElement
from Frontend.Java.TypeArgumentsFrontendAstElement import TypeArgumentsFrontendAstElement
from Frontend.Java.TypeFrontendAstElement import TypeFrontendAstElement
from Frontend.Java.VariableDeclaratorsFrontendAstElement import VariableDeclaratorsFrontendAstElement
from Frontend.Java.VariableModifierFrontendAstElement import VariableModifierFrontendAstElement

from Frontend.Java.TreeRewrite.TreeRewriter import TreeRewriter

# for the (used) java parser specification see http://docs.oracle.com/javase/specs/jls/se7/html/jls-18.html

class Parser(object):
    def __init__(self):
        self._init()

    def _init(self):
        # comments

        comment = (Literal("/") + Literal("/") + restOfLine).suppress()


        # forwards

        identifier = Forward()

        basicType = Forward()
        referenceType = Forward()
        typeArguments = Forward()
        typeArgument = Forward()

        localVariableDeclarationStatement = Forward()

        expression = Forward()
        variableInitializer = Forward()

        #####################################

        _type = \
            (basicType + ZeroOrMore(Literal("[") + Literal("]"))) | \
            (referenceType + ZeroOrMore(Literal("[") + Literal("]")))
        _type.setParseAction(TypeFrontendAstElement)
        # decides based on the type of the first parameter if its a basicType or a referenceType

        basicTypeNonforward = \
            Literal("byte") | \
            Literal("short") | \
            Literal("char") | \
            Literal("int") | \
            Literal("long") | \
            Literal("float") | \
            Literal("double") | \
            Literal("boolean")
        basicType << basicTypeNonforward

        referenceTypeNonforward = identifier + Optional(typeArguments) + ZeroOrMore(Literal(".") + identifier + Optional(typeArguments))
        referenceTypeNonforward.setParseAction(ReferenceTypeFrontendAstElement)
        referenceType << referenceTypeNonforward

        typeArgumentsNonforward = Literal("<") + typeArgument + ZeroOrMore(Literal(",") + typeArgument) + Literal(">")
        typeArgumentsNonforward.setParseAction(TypeArgumentsFrontendAstElement)
        typeArguments << typeArgumentsNonforward

        typeArgumentNonforward = \
            referenceType | \
            (Literal("?") + Optional((Literal("extends") | Literal("super")) + referenceType) )
        typeArgumentNonforward.setParseAction(TypeArgumentFrontendAstElement)
        typeArgument << typeArgumentNonforward

        ######################################








        identifierNonforward = Word(alphas)
        identifier << identifierNonforward

        # TODO< after spec >
        integerLiteral = Word(nums)
        integerLiteral.setParseAction(IntegerLiteralAstElement)

        allDatatypes = identifier

        # stuff like
        # int
        # MyClass
        # MyClass<a, b>
        # MyClass<a, b>[]
        # TODO< generics stuff >
        javaType = allDatatypes + Optional(Literal("[") + Literal("]"))
        javaType.setParseAction(JavaTypeFrontendAstElement)

        datatypeDeclaration = allDatatypes

        modifier = \
            Literal("public") | \
            Literal("private") | \
            Literal("protected") | \
            Literal("static") | \
            Literal("final") | \
            Literal("native") | \
            Literal("synchronized") | \
            Literal("abstract") | \
            Literal("threadsafe") | \
            Literal("transient")
        modifier.setParseAction(ModifierFrontendAstElement)


        variableInitializerNonforward = (Literal("{") + delimitedList(expression, delim=",") + Optional(Literal(",")) + Literal("}")) | expression
        variableInitializerNonforward.setParseAction(VariableInitializerFrontendAstElement)

        variableInitializer = variableInitializerNonforward

        variableDeclarator = identifier + Optional(Literal("[") + Literal("]")) + Optional(Literal("=") + variableInitializer)
        variableDeclarator.setParseAction(VariableDeclaratorFrontendAstElement)

        variableDeclarators = variableDeclarator + ZeroOrMore(Literal(",") + variableDeclarator)
        variableDeclarators.setParseAction(VariableDeclaratorsFrontendAstElement)

        # TODO< multiple declarations >
        # TODO< maybe the action must be modified >
        variableDeclaration = ZeroOrMore(modifier) + javaType + variableDeclarator + Literal(";")
        variableDeclaration.setParseAction(VariableDeclarationFrontendAstElement)

        # is this actually correct because int[] a[] is possible?
        parameter = Optional(modifier) + javaType + identifier + Optional(Literal("[") + Literal("]"))

        parameterList = delimitedList(parameter, delim=",")

        methodParameters = Optional(parameterList)


        castingExpression = Literal("(") + javaType + Literal(")") + expression

        # indicates access to a variable
        variableIdentifier = identifier
        variableIdentifier.setParseAction(IdentifierFrontendAstElement)

        # TODO< can also be a chained oop thingy, array accesses and so on >
        expressionLeft = variableIdentifier

        binaryNumericExpressionPriorityHigh = expressionLeft + oneOf("* *= / /=") + expression
        binaryNumericExpressionPriorityHigh.setParseAction(BinaryOperationFrontendAstElement)

        binaryNumericExpressionPriorityLow = expressionLeft + oneOf("+ += - -= % %=") + expression
        binaryNumericExpressionPriorityLow.setParseAction(BinaryOperationFrontendAstElement)

        assignmentExpression = expressionLeft + Literal("=") + expression
        assignmentExpression.setParseAction(BinaryOperationFrontendAstElement)

        numericExpression = \
            binaryNumericExpressionPriorityHigh | \
            binaryNumericExpressionPriorityLow | \
            (Literal("-") | Literal("++") | Literal("--") ) + expression | \
            expressionLeft + ( Literal("++") | Literal("--") )

        # complete
        logicalExpression = \
            Literal("!") + expression | \
            expressionLeft + oneOf("ampersand ampersand= | |= ^ ^= ||= & &=") + expression | \
            expressionLeft + Literal("ampersand") + Literal("ampersand") + expression | \
            Literal("true") | \
            Literal("false")
        # 	expression + Literal("?") + expression + Literal(":") + expression | \

        # TODO< more >
        literalExpression = integerLiteral



        # splited from expression because it can't like it if it is in expression
        expressionNonforward = \
            assignmentExpression | \
            expressionLeft + Literal("[") + expression + Literal("]") | \
            literalExpression | \
            numericExpression | \
            logicalExpression | \
            Literal("null") | \
            Literal("super") | \
            Literal("this") | \
            variableIdentifier | \
            castingExpression | \
            Literal("(") + expression + Literal(")")



        expression << expressionNonforward

        statement = Forward()

        ########################

        variableModifier = \
            Literal("final")
            # TODO< Annotation >
        variableModifier.setParseAction(VariableModifierFrontendAstElement)

        ########################

        blockStatement = Forward()

        block = Literal("{") + ZeroOrMore(blockStatement) + Literal("}")
        block.setParseAction(BlockFrontendAstElement)

        # TODO< ClassOrInterfaceDeclaration >
        # TODO< [Identifier :] Statement  label >
        blockStatementNonforward = \
            localVariableDeclarationStatement | \
            statement
        blockStatement << blockStatementNonforward

        localVariableDeclarationStatementNonforward = ZeroOrMore(variableModifier) + _type + variableDeclarators + ";"
        localVariableDeclarationStatementNonforward.setParseAction(LocalVariableDeclarationFrontendAstElement)
        localVariableDeclarationStatement << localVariableDeclarationStatementNonforward

        ##########################

        ifStatement = Literal("if") + Literal("(") + expression + Literal(")") + statement + Optional(Literal("else") + statement)
        ifStatement.setParseAction(IfStatementAstElement)

        # TODO< assert Expression [: Expression] ;                       >
        # TODO< switch ParExpression { SwitchBlockStatementGroups }      >
        # TODO< while ParExpression Statement                            >
        # TODO< do Statement while ParExpression ;                       >
        # TODO< for ( ForControl ) Statement                             >
        # TODO< break [Identifier] ;                                     >
        # TODO< continue [Identifier] ;                                  >
        # TODO< return [Expression] ;                                    >
        # TODO< throw Expression ;                                       >
        # TODO< synchronized ParExpression Block                         >
        # TODO< try Block (Catches | [Catches] Finally)                  >
        # TODO< try ResourceSpecification Block [Catches] [Finally]      >
        statementNonforward = \
            block | \
            Literal(";") | \
            (expression + Literal(";")) | \
            ifStatement

        statement << statementNonforward

        terminatedStatements = ZeroOrMore(statement)

        methodDefinition = javaType + identifier + Literal("(") + methodParameters + Literal(")") + Literal("{") + terminatedStatements + Literal("}")

        self.parser = statement
        self.parser.ignore(comment)

        return

        b = variableInitializer.parseString("{aa,bb}")[0]

        a = variableDeclaration.parseString("int a=b;")[0]

        a = statement.parseString("int a = 0;")[0]
        a = terminatedStatements.parseString("a = 0;")

        a = statement.parseString("if(a) int a = 0;")

        listi = TreeRewriter.rewriteSingleElement(a[0])

        # just for testing
        return listi

        # expression and stuff
        parseTree = expression.parseString("aa+bb*cc")[0]

        x = 0 # for debugging

        print(expression.parseString("(aa+bb)"))
        print(expression.parseString("aa++"))
        print(expression.parseString("++aa"))
        print(expression.parseString("a+b*c"))
        print(expression.parseString("(c)a")) # casting
        print(expression.parseString("5")) # literal expression
        print(expression.parseString("a[6]"))

        print("variable declaration")

        # variable declaration
        #print(variableDeclaration.parseString("int x;"))
        print(variableDeclaration.parseString("int x=aaaa;"))



        print("real Tests")

        # type test
        print(methodDefinition.parseString("mytype test() {a+b;}"))
        print(methodDefinition.parseString("mytype[] test() {a+b;}"))

        # numerics
        print(methodDefinition.parseString("mytype test() {a+a;}"))

        # parameters
        print(methodDefinition.parseString("mytype test(int a, int b) {a+b;}"))

        # variable initialisation
        print(methodDefinition.parseString("mytype test(int a, int b) {int z = a;}"))

    ## tries to parse the text, throws a parsing exception if something gone wrong
    #
    # returns the Abstract Syntax Tree
    def parse(self, text: str):
        a = self.parser.parseString(text)

        rewritten = TreeRewriter.rewriteSingleElement(a[0])

        return rewritten