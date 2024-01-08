from pycparser import c_ast as ast

from .Node import Node


class StructNodeMember(Node):
    def __init__(self, type_decl_node):
        self.name = type_decl_node.declname
        self.type = " ".join(type_decl_node.type.names)

    @staticmethod
    def is_type(decl_node):
        return type(decl_node.type) == ast.IdentifierType
