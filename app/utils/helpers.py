import os


def get_env_variable(var_name: str, default_value: str = "") -> str:
    return os.getenv(var_name, default_value)
