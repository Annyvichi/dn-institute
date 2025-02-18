import os
import subprocess

default_subprocess_config = {
    # FIXME: Is this required?
    # "cwd": os.environ["GITHUB_WORKSPACE"],
    "stdout": subprocess.PIPE,
    "universal_newlines": True,
    "check": True,
}


def execute(cmd: list[str], config: dict = default_subprocess_config):
    cmd_str = " ".join(cmd)
    print(f"Executing: {cmd_str}")
    process = subprocess.run(cmd, **config)
    print(process.stdout)
    print(f"Process exited with code {process.returncode}")
    return process


def logging_decorator(group_name):
    def decorator_wrapper(original_func):
        def wrapper_func(*func_args, **func_kwargs):
            if os.environ.get("GITHUB_ACTIONS") == "true":
                print(f"::group::{group_name}")
                result = original_func(*func_args, **func_kwargs)
                print("::endgroup::")
            else:
                print(f"=={group_name}==\n")
                result = original_func(*func_args, **func_kwargs)
                print("\n==End==\n\n")

            return result

        return wrapper_func

    return decorator_wrapper
