from pycparser import c_ast as ast
import logging

from .Node import Node
from .VariableNode import VariableNode
from .Collection import Collection


class VariableNodeCollection(Node, Collection):
    def __init__(self, top_node):
        self.variables = []
        for nested in top_node:
            if VariableNode.is_type(nested):
                self.variables.append(VariableNode(nested))
            elif VariableNode.is_type(nested.type):
                self.variables.append(VariableNode(nested.type))

    @staticmethod
    def is_type(node):
        return type(node) == ast.FileAST

    # def filter(self, so_var_names):
    #     base_names = set([var.name for var in self.variables])
    #     filter_names = set(so_var_names)
    #     self.variables = [var for var in self.variables if var.name in so_var_names]
    #     if len(self.variables) == 0:
    #         logging.warning("Variable collection contains 0 variables after filtering")
    #     return base_names - filter_names, filter_names - base_names

    # def validate(self):
    #     names = [var.name for var in self.variables]
    #     duplicates = list(set(set([x for x in names if names.count(x) > 1])))
    #     if len(duplicates) > 0:
    #         raise ValueError(f"Found duplicates in enums: '{duplicates}'")

    # def get_main_types(self, driver):
    #     main_types = []
    #     for variable in self.variables:
    #         if variable.is_main_variable(driver) and \
    #                 not variable.is_hidden_variable(driver):
    #             main_types.append(variable.type)
    #     return main_types

    # def get_public_names(self, driver):
    #     result = {}
    #     for variable in self.variables:
    #         if variable.is_main_variable(driver) and \
    #                 not variable.is_hidden_variable(driver):
    #             result[variable.public_name(driver)] = variable.type
    #     return result

    # def construct_str(self, driver, indent=0):
    #     forward_declarations = ""
    #     accessors = ""
    #     for variable in self.variables:
    #         if variable.is_main_variable(driver) and not variable.is_hidden_variable(driver):
    #             accessors += variable.construct_accessors(driver, indent)
    #             forward_declarations += variable.constract_class_members(
    #                 driver, indent)
    #         # secondary block contains:
    #         # rtInf: float
    #         # rtMinusInf: float
    #         # rtNaN: float
    #         # rtInfF: float
    #         # rtMinusInfF: float
    #         # rtNaNF: float
    #     return accessors if forward_declarations == "" else forward_declarations + "\n" + accessors

    # def construct_class_members(self, driver, indent=0):
    #     pass
        # class_members = ""
        # for variable in self.variables:
        #     if variable.is_main_variable(driver) and not variable.is_hidden_variable(driver):
        #         class_members += variable.construct_class_members(driver, indent)
        # return class_members

    # def construct_init(self, driver, indent=0):
    #     forward_declarations = ""
    #     for variable in self.variables:
    #         if variable.is_main_variable(driver) and not variable.is_hidden_variable(driver):
    #             forward_declarations += variable.construct_init_members(driver, indent)
    #     return forward_declarations

    # def construct_accessors(self, driver, indent=0):
    #     accessors = ""
    #     for variable in self.variables:
    #         if variable.is_main_variable(driver) and not variable.is_hidden_variable(driver):
    #             accessors += variable.construct_accessors(driver, indent)
    #     return accessors

    # def construct_type_alias(self, driver, indent=0):
    #     result = ""
    #     for variable in self.variables:
    #         if variable.is_main_variable(driver) and \
    #                 not variable.is_hidden_variable(driver):
    #             stack = self.types.get_types_stack(variable.type)
    #             for idx in range(len(stack) - 1):
    #                 result += "{0} = {1}\n".format(
    #                     driver.types_access + stack[idx],
    #                     driver.types_access + stack[idx + 1])
    #     return "\n" + result if result != "" else ""
