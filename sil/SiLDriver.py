import asyncio
import logging
import os
import tempfile

from jinja2 import Environment, FileSystemLoader

from ..Collector import Collector
from ..Driver import Driver


class SiLDriver(Driver):
    _templ_dir = os.path.abspath(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'templates')
    )
    _env = Environment(loader=FileSystemLoader(_templ_dir), autoescape=True, keep_trailing_newline=True)

    @classmethod
    async def compose(cls, collector: Collector, output_dir: str, license_text: str) -> tuple[str, str, str]:
        if not os.path.isdir(output_dir):
            raise ValueError(f"Directory '{output_dir}' not found.")

        pkg_dir = os.path.join(output_dir, collector.python_package_name)
        os.mkdir(pkg_dir)

        build_dir = tempfile.TemporaryDirectory()
        stash_dir = tempfile.TemporaryDirectory()
        try:
            init_str = cls._env.get_template("__init__.py.j2").render(
                model_name=collector.model_name
            )
            init_path = os.path.join(pkg_dir, "__init__.py")
            with open(init_path, 'w') as file_obj:
                file_obj.write(init_str)

            base_model_str = cls._env.get_template("BaseModel.py.j2").render()
            base_model_path = os.path.join(pkg_dir, "BaseModel.py")
            with open(base_model_path, 'w') as file_obj:
                file_obj.write(base_model_str)

            model_str = cls._env.get_template("Model.py.j2").render(
                model_name=collector.model_name,
                input_map=collector.input_members,
                output_map=collector.output_members
            )
            model_path = os.path.join(pkg_dir, "Model.py")
            with open(model_path, 'w') as file_obj:
                file_obj.write(model_str)

            pyproject_str = cls._env.get_template("pyproject.toml.j2").render(
                model_version=collector.model_version,
                package_name=collector.python_package_name,
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

            swig_str = cls._env.get_template("swig.i.j2").render(
                model_name=collector.model_name
            )
            swig_path = os.path.join(stash_dir.name, "swig.i")
            with open(swig_path, 'w') as file_obj:
                file_obj.write(swig_str)

            cmake_str = cls._env.get_template("CMakeLists.txt.j2").render(
                model_name=collector.model_name,
                source_dir=collector.c_code_tmp_path,
                swig_interface_path=swig_path,
                output_dir=pkg_dir,
                build_dir=build_dir.name,
            )
            cmake_path = os.path.join(stash_dir.name, "CMakeLists.txt")
            with open(cmake_path, 'w') as file_obj:
                file_obj.write(cmake_str)

            cmake_proc = await asyncio.create_subprocess_exec(
                'cmake',
                f'-B{build_dir.name}',
                f'-S{stash_dir.name}',
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.PIPE
            )
            _, stderr = await cmake_proc.communicate()
            if cmake_proc.returncode:
                logging.error(stderr)
                raise RuntimeError(stderr)

            make_proc = await asyncio.create_subprocess_exec(
                'make',
                f'-C{build_dir.name}',
                '--silent',
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.PIPE
            )
            _, stderr = await make_proc.communicate()
            if make_proc.returncode:
                logging.error(stderr)
                raise RuntimeError(stderr)
        finally:
            build_dir.cleanup()
            stash_dir.cleanup()

        return collector.python_package_name, cls.module_name, cls.wrapper_class_name
