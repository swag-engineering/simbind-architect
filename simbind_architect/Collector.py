from __future__ import annotations
import asyncio
import os

from pycparser import parse_file, c_ast as ast

from .nodes import StructNodeCollection, FunctionNodeCollection, VariableNodeCollection, TypeNodeMap
from .architect_utils import extract_model_data, collect_includes


class Collector:
    def __init__(self, c_code_path: str, python_package_name: str, time_step: float):
        self.c_code_tmp_path = c_code_path
        self.python_package_name = python_package_name
        self.time_step = time_step

        self.rtmodel_h_path = os.path.join(self.c_code_tmp_path, 'rtmodel.h')
        if not os.path.exists(self.rtmodel_h_path):
            raise ValueError("Can not find 'rtmodel.h'")

        main_c_path = os.path.join(self.c_code_tmp_path, 'rt_main.c')
        if os.path.exists(main_c_path):
            os.remove(main_c_path)

        self.model_name, self.model_version = extract_model_data(self.rtmodel_h_path)

        includes = collect_includes(self.c_code_tmp_path)
        top_node = parse_file(self.rtmodel_h_path, use_cpp=True, cpp_args=includes)
        if not isinstance(top_node, ast.FileAST):
            raise ValueError("Didn't find valid declaration after parsing header.")

        self.structs_collection = StructNodeCollection(top_node)
        self.functions_collection = FunctionNodeCollection(top_node)
        self.variables_collection = VariableNodeCollection(top_node)
        self.types_map = TypeNodeMap(top_node)

    @property
    def input_members(self) -> dict:
        return self.get_members(f"ExtU_{self.model_name}_T")

    @property
    def output_members(self) -> dict:
        return self.get_members(f"ExtY_{self.model_name}_T")

    def get_members(self, struct_name: str) -> dict:
        return {
            member.name: self.types_map[member.type]
            for member in self.structs_collection[struct_name].members
        } if struct_name in self.structs_collection else {}

    @classmethod
    async def create(cls, c_code_path: str, python_package_name: str, time_step: float) -> Collector:
        return await asyncio.to_thread(cls, c_code_path, python_package_name, time_step)
