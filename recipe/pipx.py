from tevm.lib.core import Recipe as BaseRecipe

class Recipe(BaseRecipe):
    name: str = "pipx"
    author: str = "Nuhil-Lucas"
    version: str = "0.1.0"
    request_project: list[str] = ["pysa"]

    project_info: dict = {
        "executables": {
            "rel|/projects/python_standalone/python.exe": "",
            "rel|/projects/pipx/pipx.pyz": ""
        },
        "envars": {
            "PIPX_HOME": "./projects/pipx/home",
            "PIPX_GLOBAL_HOME": "",
            "PIPX_BIN_DIR": "./projects/pipx/scripts",
            "PIPX_GLOBAL_BIN_DIR": "",
            "PIPX_MAN_DIR": "./projects/pipx/man",
            "PIPX_GLOBAL_MAN_DIR": "",
            "PIPX_SHARED_LIBS": "",
            "PIPX_DEFAULT_PYTHON": "./projects/python_standalone/python.exe",
            "PIPX_FETCH_MISSING_PYTHON": "",
            "PIPX_USE_EMOJI": "",
            "PIPX_HOME_ALLOW_SPACE": ""
        },
        "appendcmd": []
    }

    def before_install(self):
        return super().before_install()

    def after_install(self):
        return super().after_install()

from tevm.lib.core.reciper.devlib import check_request, net_operate, file_operate, release_github, project_operate, ColorPrint as cp

def run() -> bool:
    file_url_backup: list = ["pipx.pyz", "https://github.com/pypa/pipx/releases/download/1.8.0/pipx.pyz"]

    _state_check_request_, request = check_request(request_tevm, request_pypackage)
    if not _state_check_request_:
        cp.error("Request Package Or Projects Not Installed Yet.")
        print("    " + str(request))
        return False

    _state_get_release_, data = release_github.get_release("pypa", "pipx")
    cp.info("Info: [get_release].")
    if _state_get_release_:
        cp.info("    release get success.")
    else:
        cp.error("    " + data)
        cp.info("    try to use " + str(file_url_backup))

    _state_get_url_, file_url = release_github.get_url(data, [r"^pipx\.pyz$"]) if _state_get_release_ else False, file_url_backup
    if _state_get_release_:
        cp.info("Info: [get_url].")
    if _state_get_url_:
        cp.info("    url get success.")
    elif _state_get_release_ and not _state_get_url_:
        cp.error("    " + file_url)
        cp.info("    try to use " + str(file_url_backup))
        file_url = file_url_backup

    _state_get_file_, file = release_github.get_file(file_url[1], "./temp/pipx", file_url[0])
    cp.info("Info: [get_file].")
    if _state_get_file_:
        cp.info("    file get success.")
    else:
        cp.error("    " + file)
        return False

    _state_moveto_, file = file_operate.moveto(file, "./projects/pipx/pipx.pyz", True)
    cp.info("Info: [moveto].")
    if _state_moveto_:
        cp.info("    file move success.")
    else:
        cp.error("    " + file)
        return False
    
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