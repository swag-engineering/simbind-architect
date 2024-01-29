from pycparser import c_ast as ast

from .Node import Node
from .StructNode import StructNode
from .Collection import Collection


class StructNodeCollection(Node, Collection):
    def __init__(self, top_node):
        self.structs: dict[str, StructNode] = {}
        for nested in top_node:
            if StructNode.is_type(nested):
                self.add(StructNode(nested))
            elif StructNode.is_type(nested.type):
                self.add(StructNode(nested.type))

    @staticmethod
    def is_type(decl_node):
        return isinstance(decl_node, ast.FileAST)

    def add(self, struct: StructNode):
        if struct.name in self.structs.keys():
            raise ValueError(f"Found duplicate struct name: '{struct.name}'")
        self.structs[struct.name] = struct

    def __getitem__(self, item):
        return self.structs[item]

    def __contains__(self, item):
        return item in self.structs.keys()
