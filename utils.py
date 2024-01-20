import asyncio
import multiprocessing
import os
import random
import shutil
import sys
from concurrent.futures import ProcessPoolExecutor
from importlib import import_module

from .Collector import Collector


async def test_model_integrity(
        search_path: str,
        pkg_name: str,
        module_name: str,
        class_name: str,
        collector: Collector,
        test_callback: bool = False,
):
    loop = asyncio.get_event_loop()
    pool = ProcessPoolExecutor(max_workers=1)
    manager = multiprocessing.Manager()
    queue = manager.Queue(-1)

    await loop.run_in_executor(
        pool,
        execute,
        queue,
        search_path,
        pkg_name,
        module_name,
        class_name,
        collector.input_members.keys(),
        collector.output_members.keys(),
        test_callback
    )
    if not queue.empty():
        raise RuntimeError(queue.get())
    delete_cache(search_path)


def delete_cache(root_dir):
    for root, dirs, files in os.walk(root_dir):
        if "__pycache__" in dirs:
            shutil.rmtree(os.path.join(root, "__pycache__"))


def execute(
        queue: multiprocessing.Queue,
        search_path: str,
        pkg_name: str,
        module_name: str,
        class_name: str,
        input_vars: list[str],
        output_vars: list[str],
        test_callback: bool
):
    current_time = 0
    prev_time = 0
    callback_called = False
    current_input = {}
    current_output = {}

    def callback(time: float, in_data: dict, out_data: dict):
        nonlocal callback_called
        callback_called = True
        if set(in_data.keys()) != set(input_vars):
            raise RuntimeError("Input vars do not match!")
        if set(out_data.keys()) != set(output_vars):
            raise RuntimeError("Output vars do not match!")
        if time != current_time:
            raise RuntimeError("Time does not match")
        if in_data != current_input:
            raise RuntimeError("Current input does not match")
        if out_data != current_output:
            raise RuntimeError("Current output does not match")

    def collect_data():
        nonlocal current_time
        current_time = getattr(instance, "time")
        input_data = getattr(instance, "input")
        output_data = getattr(instance, "output")
        for val in input_vars:
            current_input[val] = getattr(input_data, val)
        for val in output_vars:
            current_output[val] = getattr(output_data, val)

    def set_input():
        input_data = getattr(instance, "input")
        for val in input_vars:
            setattr(input_data, val, random.uniform(0.0, 1000.0))

    try:
        sys.path.append(search_path)

        model_module = import_module(module_name, package=pkg_name)
        model_class = getattr(model_module, class_name)

        instance = model_class(callback) if test_callback else model_class()
        for _ in range(100):
            set_input()
            collect_data()
            instance.step()
            if test_callback:
                if not callback_called:
                    raise RuntimeError("Callback is not called")
                callback_called = False
            if prev_time == getattr(instance, "time"):
                raise RuntimeError("Time does not increment")
            prev_time = getattr(instance, "time")
        collect_data()
        instance.terminate()
    except Exception as ex:
        queue.put(str(ex))
