import abc
import enum

from .Collector import Collector


class PropertyNameEnum(enum.Enum):
    TIME = "time"
    INPUT = "input"
    OUTPUT = "output"
    RT_MODEL = "rt_model"


class MemberFunctionEnum(enum.Enum):
    INITIALIZE = "initialize"
    STEP = "step"
    TERMINATE = "terminate"


class Driver(abc.ABC):
    module_name = "model"
    pip_package_name = "model"
    wrapper_class_name = "Model"

    @classmethod
    @abc.abstractmethod
    async def compose(cls, architect: Collector, output_dir: str, license_text: str) -> str:
        pass
