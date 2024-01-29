import sys

from pycparser import c_ast as ast

from .Node import Node


class TypeNodeMap(Node):
    _c2python_types_map = {
        'void': 'None',
        'char': 'int',
        'signed char': 'int',
        'unsigned char': 'int',
        'short': 'int',
        'short int': 'int',
        'signed short': 'int',
        'signed short int': 'int',
        'unsigned short': 'int',
        'unsigned short int': 'int',
        'int': 'int',
        'signed': 'int',
        'signed int': 'int',
        'unsigned': 'int',
        'unsigned int': 'int',
        'long': 'int',
        'long int': 'int',
        'signed long': 'int',
        'signed long int': 'int',
        'unsigned long': 'int',
        'unsigned long int': 'int',
        'long long': 'int',
        'long long int': 'int',
        'signed long long': 'int',
        'signed long long int': 'int',
        'unsigned long long': 'int',
        'unsigned long long int': 'int',
        'float': 'float',
        'double': 'float',
        'long double': 'float'
    }

    def __init__(self, top_node):
        self.map = {}
        for nested in top_node:
            if not isinstance(nested, ast.Typedef):
                continue
            nested.type, _ = Node._skip_ptr_decls(nested.type)
            if not isinstance(nested.type, ast.TypeDecl):
                continue
            if isinstance(nested.type.type, ast.IdentifierType):
                self._update_types(nested.type.declname, " ".join(nested.type.type.names))
            elif isinstance(nested.type.type, ast.Struct):
                self._update_types(nested.type.declname, nested.type.type.name)

    @staticmethod
    def is_type(node):
        return isinstance(node, ast.FileAST)

    def __getitem__(self, item):
        if item in self.map:
            return self.__getitem__(self.map[item])
        if item in self._c2python_types_map:
            return self._c2python_types_map[item]
        return item

    def _update_types(self, left, right):
        if left in self.map.keys():
            sys.exit("Found duplicated(second definition?) type '" + left + "'")
        self.map[left] = right
