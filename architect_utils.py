import os
import re

import pycparser_fake_libc


def extract_model_data(rtmodel_path: str) -> tuple[str, str]:
    with open(rtmodel_path) as file_obj:
        rtmodel_data = file_obj.read()
    return extract_model_name(rtmodel_data), extract_model_version(rtmodel_data)


def extract_model_version(rtmodel_data: str) -> str:
    match = re.search(r'Model version *: ([0-9.]+).*', rtmodel_data)
    if not match:
        raise ValueError("Can't detect model version")
    return match.group(1)


def extract_model_name(rtmodel_data: str) -> str:
    match = re.search(r'#include "(.*?).h".*', rtmodel_data)
    if not match:
        raise ValueError("Can't detect model name")
    return match.group(1)


def collect_includes(dir_path: str) -> list[str]:
    include_paths = [dir_path, pycparser_fake_libc.directory]
    includes = ["-I" + path for path in include_paths]
    return includes


def collect_files_with_ext(dir_path: str, ext: str) -> list[str]:
    result = []
    for file in os.listdir(dir_path):
        if file.endswith(ext):
            result.append(os.path.join(dir_path, file))
    return result
