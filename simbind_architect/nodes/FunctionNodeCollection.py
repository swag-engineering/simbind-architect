from pycparser import c_ast as ast

from .Node import Node
from .FunctionNode import FunctionNode
from .Collection import Collection


class FunctionNodeCollection(Node, Collection):
    def __init__(self, top_node):
        self.functions: list[FunctionNode] = []
        for nested in top_node:
            if FunctionNode.is_type(nested):
                self.functions.append(FunctionNode(nested))
            elif FunctionNode.is_type(nested.type):
                self.functions.append(FunctionNode(nested.type))

    @staticmethod
    def is_type(decl_node):
        return isinstance(decl_node, ast.FileAST)
