import importlib


def run_script(name, body):
    file_name, func_name = name.split("/")

    module = importlib.import_module(f"scripts.{file_name}")
    func = getattr(module, func_name)
    return func(body)
