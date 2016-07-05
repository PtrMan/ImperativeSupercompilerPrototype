import os

from Frontend.Java.Parser import Parser
from Frontend.Java.TreeRewrite.TreeRewriter import TreeRewriter

parser = Parser()

path = os.path.dirname(os.path.realpath(__file__))

currentFile = open(path + "\\..\\Tests\\declaration 1.java")

currentContent = currentFile.read()
currentFile.close()

rewrittenAst = parser.parse(currentContent)

a = 5