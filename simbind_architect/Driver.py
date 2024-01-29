import abc

from .Collector import Collector


class Driver(abc.ABC):
    wrapper_class_name = "Model"

    @classmethod
    @abc.abstractmethod
    async def compose(cls, architect: Collector, output_dir: str, license_text: str) -> tuple[str, str]:
        pass
