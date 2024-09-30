from pycparser import c_ast as ast

from .Node import Node
from .FunctionNode import FunctionNode
from .Collection import Collection


class FunctionNodeCollection(Node, Collection):
    def __init__(self, top_node):
        self.functions: list[FunctionNode] = []
        for nested in top_node:
            try:
                if FunctionNode.is_type(nested):
                    self.functions.append(FunctionNode(nested))
                elif FunctionNode.is_type(nested.type):
                    self.functions.append(FunctionNode(nested.type))
            except AttributeError:
                continue

    @staticmethod
    def is_type(decl_node):
        try:
            return isinstance(decl_node, ast.FileAST)
        except AttributeError:
            return False
