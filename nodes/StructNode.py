from pycparser import c_ast as ast

from .Node import Node
from .StructNodeMember import StructNodeMember


class StructNode(Node):
    def __init__(self, decl_node, nested=False):
        self.name = decl_node.declname if type(decl_node) == ast.TypeDecl else decl_node.type.name
        self.members = []
        self.nested = nested

        for decl in decl_node.type.decls:
            if StructNodeMember.is_type(decl.type):
                self.members.append(StructNodeMember(decl.type))

    @staticmethod
    def is_type(decl_node):
        if type(decl_node.type) == ast.Struct and decl_node.type.decls:
            return True
        return False
