from pycparser import c_ast as ast

from .Node import Node


class VariableNode(Node):
    def __init__(self, node):
        node, _ = self._skip_ptr_decls(node.type)
        # node = node.type
        self.name = node.declname
        self.type = " ".join(node.type.names)

    @staticmethod
    def is_type(node):
        # if type(nested) == ast.Decl and (type(nested.type) == ast.TypeDecl or type(nested.type) == ast.PtrDecl):
        #     self.variables.append(VariableNode(nested.type))
        return type(node) == ast.Decl and (type(node.type) == ast.TypeDecl or type(node.type) == ast.PtrDecl)

    # def is_main_variable(self, driver):
    #     return driver.is_main_variable(self.name)

    # def is_hidden_variable(self, driver):
    #     return driver.is_hidden_variable(self.name)

    # def public_name(self, driver):
    #     return driver.mock_variable_name(self.name)

    # def private_name(self, driver):
    #     if not driver.variables_access:
    #         return "self.__" + self.public_name(driver)
    #     return driver.variables_access + self.name

    # TODO relocate self to driver.variables_access(?)
    # def private_member_name(self, driver):
    #     if not driver.variables_access:
    #         return "self." + self.private_name(driver)
    #     return self.private_name(driver)

    # def public_type(self, driver):
    #     return driver.mock_variable_name(self.name) if \
    #         self.types.is_root_basic_type(self.type) else self.type

    # def construct_accessors(self, driver, indent=0):
    #     result = ""
    #     # TODO need the controller to diff class members, obj members and if accessors are needed
    #     # if not driver.variables_access:
    #     #     return result
    #     if driver.is_variable_readable(self.public_name(driver)):
    #         result += self._formatter_getter.format(
    #             self.public_name(driver),
    #             driver.types_access + self.public_type(driver),
    #             self.private_member_name(driver),
    #             driver.indent_str * indent,
    #             driver.indent_str * (indent + 1))
    #     if driver.is_variable_writable(self.public_name(driver)):
    #         result += self._formatter_setter.format(
    #             self.public_name(driver),
    #             driver.types_access + self.public_type(driver),
    #             self.private_member_name(driver),
    #             driver.indent_str * indent,
    #             driver.indent_str * (indent + 1))
    #     return result

    # def construct_class_members(self, driver, indent=0):
    #     return ""

    # def construct_init_members(self, driver, indent=0):
    #     if driver.variables_access:
    #         return ""
    #     return self._formatter_init.format(
    #         self.private_name(driver),
    #         driver.types_access + self.public_type(driver),
    #         driver.indent_str * indent
    #     )
