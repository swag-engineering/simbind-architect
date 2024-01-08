import os

from jinja2 import Environment, FileSystemLoader

from ..Collector import Collector
from ..Driver import Driver


class MockDriver(Driver):
    _templ_dir = os.path.abspath(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'templates')
    )
    _env = Environment(loader=FileSystemLoader(_templ_dir), autoescape=True, keep_trailing_newline=True)

    @classmethod
    async def compose(cls, collector: Collector, output_dir: str, license_text: str) -> tuple[str, str, str]:
        if not os.path.isdir(output_dir):
            raise ValueError(f"Directory '{output_dir}' not found.")

        module_dir = os.path.join(output_dir, cls.module_name)
        os.mkdir(module_dir)

        init_str = cls._env.get_template("__init__.py.j2").render()
        init_path = os.path.join(module_dir, "__init__.py")
        with open(init_path, 'w') as file_obj:
            file_obj.write(init_str)

        base_model_str = cls._env.get_template("BaseModel.py.j2").render()
        base_model_path = os.path.join(module_dir, "BaseModel.py")
        with open(base_model_path, 'w') as file_obj:
            file_obj.write(base_model_str)

        model_str = cls._env.get_template("Model.py.j2").render(
            model_name=collector.model_name,
            input_map=collector.input_members,
            output_map=collector.output_members,
            time_step=collector.time_step
        )
        model_path = os.path.join(module_dir, "Model.py")
        with open(model_path, 'w') as file_obj:
            file_obj.write(model_str)

        types_str = cls._env.get_template("types.py.j2").render(
            model_name=collector.model_name,
            input_map=collector.input_members,
            output_map=collector.output_members
        )
        types_path = os.path.join(module_dir, "types.py")
        with open(types_path, 'w') as file_obj:
            file_obj.write(types_str)

        pyproject_str = cls._env.get_template("pyproject.toml.j2").render(
            model_version=collector.model_version,
            package_name=cls.pip_package_name,
            model_name=collector.model_name
        )
        pyproject_path = os.path.join(output_dir, "pyproject.toml")
        with open(pyproject_path, 'w') as file_obj:
            file_obj.write(pyproject_str)

        license_path = os.path.join(output_dir, "LICENSE")
        with open(license_path, 'w') as file_obj:
            file_obj.write(license_text)

        readme_str = cls._env.get_template("README.md.j2").render()
        readme_path = os.path.join(output_dir, "README.md")
        with open(readme_path, 'w') as file_obj:
            file_obj.write(readme_str)

        return cls.pip_package_name, cls.module_name, cls.wrapper_class_name
