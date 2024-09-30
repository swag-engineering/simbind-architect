from pycparser import c_ast as ast

from .Node import Node
from .VariableNode import VariableNode
from .Collection import Collection


class VariableNodeCollection(Node, Collection):
    def __init__(self, top_node):
        self.variables: list[VariableNode] = []
        for nested in top_node:
            try:
                if VariableNode.is_type(nested):
                    self.variables.append(VariableNode(nested))
                elif VariableNode.is_type(nested.type):
                    self.variables.append(VariableNode(nested.type))
            except AttributeError:
                continue

    @staticmethod
    def is_type(node):
        try:
            return isinstance(node, ast.FileAST)
        except AttributeError:
            return False
