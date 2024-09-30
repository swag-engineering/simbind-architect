from pycparser import c_ast as ast

from .Node import Node


class FunctionNodeParameter(Node):
    def __init__(self, param):
        param.type, _ = self._skip_ptr_decls(param.type)
        self.name = param.name
        self.type = " ".join(param.type.type.names)

    @staticmethod
    def is_type(param):
        try:
            return (isinstance(param, ast.Typename) or isinstance(param, ast.Decl)) and param.name is not None
        except AttributeError:
            return False
