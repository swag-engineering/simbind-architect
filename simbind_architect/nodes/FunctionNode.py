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
        # if type(nested) == ast.Decl and type(nested.type) == ast.FuncDecl:
        #     self.functions.append(FunctionNode(nested.type))
        # # these functions defined but do not exist in so
        # if type(nested) == ast.Typedef and type(nested.type) == ast.PtrDecl and \
        #         type(nested.type.type) == ast.FuncDecl:
        #     self.functions.append(FunctionNode(nested.type.type))
        return (type(decl_node) == ast.Decl or type(decl_node) == ast.PtrDecl) and type(decl_node.type) == ast.FuncDecl

    # def _collect_args(decls):
    #     pass

    # def is_main_function(self, driver):
    #     return driver.is_main_function(self.name)

    def param_names(self):
        return [param.name for param in self.params]

    # def construct_params(self, with_types=False, instance_method=False):
    #     params_lst = ["self"] if instance_method else []
    #     if with_types:
    #         params_lst += [param.construct_str(driver) for param in self.params]
    #     else:
    #         params_lst += [param.name for param in self.params]
    #     return ", ".join(params_lst)

    # def construct_str(self, driver, indent=0):
    #     name = driver.mock_function_name(self.name)
    #     return_type = self.types.find_root_type(self.return_type) if \
    #         self.types.is_root_basic_type(self.return_type) else None
    #     result_block = self._formatter_decl.format(name,
    #                                                self.construct_params(True, True),
    #                                                return_type,
    #                                                driver.indent_str * indent)
    #     indent += 1
    #     # if driver.functions_access:
    #     #     result_block += self._formatter_body.format(
    #     #         driver.functions_access + self.name,
    #     #         self.construct_params(),
    #     #         driver.indent_str * indent)
    #     # else:
    #     # change function body here
    #
    #     # result_block += self._formatter_empty_body.format(driver.indent_str * indent)
    #     result_block += driver.get_function_body(self.name, indent)
    #     return result_block
