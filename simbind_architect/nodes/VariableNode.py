from pycparser import c_ast as ast

from .Node import Node


class VariableNode(Node):
    def __init__(self, node):
        node, _ = self._skip_ptr_decls(node.type)
        self.name = node.declname
        self.type = " ".join(node.type.names)

    @staticmethod
    def is_type(node):
        return isinstance(node, ast.Decl) and (isinstance(node.type, ast.TypeDecl) or isinstance(node.type, ast.PtrDecl))