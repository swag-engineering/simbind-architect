import abc

from pycparser import c_ast as ast


class Node(metaclass=abc.ABCMeta):
    @staticmethod
    @abc.abstractmethod
    def is_type(node):
        return

    @staticmethod
    def _skip_ptr_decls(node, lvl=0):
        if isinstance(node, ast.PtrDecl):
            return Node._skip_ptr_decls(node.type, lvl+1)
        return node, lvl

