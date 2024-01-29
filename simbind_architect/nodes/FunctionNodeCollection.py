from pycparser import c_ast as ast

from .Node import Node
from .FunctionNode import FunctionNode
from .Collection import Collection


class FunctionNodeCollection(Node, Collection):
    def __init__(self, top_node):
        self.functions = []
        for nested in top_node:
            if FunctionNode.is_type(nested):
                self.functions.append(FunctionNode(nested))
            elif FunctionNode.is_type(nested.type):
                self.functions.append(FunctionNode(nested.type))

    @staticmethod
    def is_type(decl_node):
        return type(decl_node) == ast.FileAST

    # def validate(self):
    #     names = [var.name for var in self.functions]
    #     duplicates = list(set(set([x for x in names if names.count(x) > 1])))
    #     if len(duplicates) > 0:
    #         raise ValueError(f"Found duplicates in enums: '{duplicates}'")

    def get_public_names(self, driver):
        result = {}
        for function in self.functions:
            if function.is_main_function(driver):
                result[driver.mock_function_name(function.name)] = function.params
        return result
