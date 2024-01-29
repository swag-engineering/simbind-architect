from pycparser import c_ast as ast

from .Node import Node
from .FunctionNodeParameter import FunctionNodeParameter


class FunctionNode(Node):
    def __init__(self, node):
        node = node.type
        self.name = node.type.declname
        self.return_type = " ".join(node.type.type.names)
        self.params = []
        for decl in node.args.params:
            if FunctionNodeParameter.is_type(decl):
                param = FunctionNodeParameter(decl)
                self.params.append(param)

    @staticmethod
    def is_type(decl_node):
        return (isinstance(decl_node, ast.Decl) or isinstance(decl_node, ast.PtrDecl)) and \
            isinstance(decl_node.type, ast.FuncDecl)

    def param_names(self):
        return [param.name for param in self.params]
