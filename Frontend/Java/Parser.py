from Libs.pyparsing import Literal, alphas, Word, delimitedList, Optional, ZeroOrMore, Forward, oneOf, nums, FollowedBy, OneOrMore
from Frontend.Java.VariableIdentifierFrontendAstElement import VariableIdentifierFrontendAstElement
from Frontend.Java.BinaryOperationFrontendAstElement import BinaryOperationFrontendAstElement
from Frontend.Java.JavaTypeFrontendAstElement import JavaTypeFrontendAstElement
from Frontend.Java.VariableDeclaratorFrontendAstElement import VariableDeclaratorFrontendAstElement
from Frontend.Java.VariableInitializerFrontendAstElement import VariableInitializerFrontendAstElement

class Parser(object):
    def __init__(self):
        self._init()

    def _init(self):
        # forwards
        expression = Forward()
        variableInitializer = Forward()

        identifier = Word(alphas)

        # TODO< after spec >
        integerLiteral = Word(nums)

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



        variableInitializerNonforward = (Literal("{") + delimitedList(expression, delim=",") + Optional(Literal(",")) + Literal("}")) | expression
        variableInitializerNonforward.setParseAction(VariableInitializerFrontendAstElement)

        variableInitializer = variableInitializerNonforward

        variableDeclarator = identifier + Optional(Literal("[") + Literal("]")) + Optional(Literal("=") + variableInitializer)
        variableDeclarator.setParseAction(VariableDeclaratorFrontendAstElement)

        variableDeclaration = Optional(modifier) + javaType + variableDeclarator + Literal(";")
        variableDeclaration.setParseAction(VariableDeclarationFrontendAstElement)

        # is this actually correct because int[] a[] is possible?
        parameter = Optional(modifier) + javaType + identifier + Optional(Literal("[") + Literal("]"))

        parameterList = delimitedList(parameter, delim=",")

        methodParameters = Optional(parameterList)


        castingExpression = Literal("(") + javaType + Literal(")") + expression

        # indicates access to a variable
        variableIdentifier = identifier
        variableIdentifier.setParseAction(VariableIdentifierFrontendAstElement)

        # TODO< can also be a chained oop thingy, array accesses and so on >
        expressionLeft = variableIdentifier

        binaryNumericExpressionPriorityHigh = expressionLeft + oneOf("* *= / /=") + expression
        binaryNumericExpressionPriorityHigh.setParseAction(BinaryOperationFrontendAstElement)

        binaryNumericExpressionPriorityLow = expressionLeft + oneOf("+ += - -= % %=") + expression
        binaryNumericExpressionPriorityLow.setParseAction(BinaryOperationFrontendAstElement)

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



        statement = \
            variableDeclaration | \
            expression + Literal(";")

        terminatedStatements = ZeroOrMore(statement)

        methodDefinition = javaType + identifier + Literal("(") + methodParameters + Literal(")") + Literal("{") + terminatedStatements + Literal("}")


        b = variableInitializer.parseString("{aa,bb}")[0]

        a = variableDeclaration.parseString("int a;")[0]



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



        print("real tests")

        # type test
        print(methodDefinition.parseString("mytype test() {a+b;}"))
        print(methodDefinition.parseString("mytype[] test() {a+b;}"))

        # numerics
        print(methodDefinition.parseString("mytype test() {a+a;}"))

        # parameters
        print(methodDefinition.parseString("mytype test(int a, int b) {a+b;}"))

        # variable initialisation
        print(methodDefinition.parseString("mytype test(int a, int b) {int z = a;}"))