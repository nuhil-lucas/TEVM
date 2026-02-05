name = "poetry"
version = "0.1.0"
author = "Nuhil-Lucas"
request_tevm = ["pipx"]
request_pypackage = []
project = {
    "poetry": {
        "executables": {
            "rel|/projects/pipx": "",
            "rel|/projects/python_standalone/python.exe": ""
        },
        "envars": {
            "POETRY_CONFIG_DIR": "./projects/pipx/home/venvs/poetry/pypoetry/config",
            "POETRY_DATA_DIR": "./projects/pipx/home/venvs/poetry/pypoetry",
            "POETRY_CACHE_DIR": "./projects/pipx/home/venvs/poetry/pypoetry/cache",
            "POETRY_VIRTUALENVS_IN_PROJECT": "true",
            "POETRY_VIRTUALENVS_USE_POETRY_PYTHON": "true"
        }
    }
}

from tevm.recipe import file_operate, release_github, command_execute, project_operate, ColorPrint as cp

def run() -> bool:
    command_execute.run(
        mode="ps1",
        command=[
            "pipx install poetry"
        ],
        cwd=""
    )

    _state_create_, info = project_operate.create(project)
    cp.info("Info: [create].")
    if _state_create_:
        cp.info("    project create success.")
    else:
        cp.error("    " + info)
        return False

    return True

if __name__ == "__main__":
    run()