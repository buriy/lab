import importlib.util
import inspect
from pathlib import Path
from typing import Union


def get_classes(module, base_type: type):
    classes = []
    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj):
            if (
                isinstance(obj, type)
                and issubclass(obj, base_type)
                and obj is not base_type
            ):
                classes.append((f"{module.__name__}.{name}", obj))
    return classes


def import_module(py_file: Path):
    module_name = py_file.stem
    spec = importlib.util.spec_from_file_location(module_name, py_file)
    if spec is not None:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        return module
    return None


def find_class_by_name(full_name: str):
    module_path, class_name = full_name.rsplit(".", 1)
    module = import_module(Path(f'{module_path}.py'))
    return module.getattr(class_name)


def find_classes_in_files(root_dir: Union[str, Path], base_type: type) -> list:
    result = []

    root_path = Path(root_dir)

    # обходим все питоновские файлы в подкаталогах экспериментов
    for py_file in root_path.rglob("*.py"):
        if module := import_module(py_file):
            classes = get_classes(module, base_type)
            result.extend(classes)

    return result
