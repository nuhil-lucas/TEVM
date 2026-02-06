# Standard
from sys import (
    path as __sys_path__,
    argv as __argv__,
    exit as __sys_exit__
)
from subprocess import (
    run as sp_run
)
from os import (
    getcwd as os_getcwd,
    makedirs as os_makedirs
)
from os.path import (
    exists as path_exists
)
from typing import (
    Literal
)
# Internal
# External

# Usable Mark Params
__param_useable__: bool = __argv__.__len__() > 2

ENVARS = Literal[
    "Root_TEVM",
    "Path_Python",
    "Path_PIP",
    "Path_WebGUI",
    "Root_Config",
    "Root_BatScripts",
    "Root_Temps",
    "Root_Recipes",
    "Path_ProjectsJson",
    "Path_TempExecutor",
    "Root_ExternalPkg_Req",
    "Parh_ExternalPkg_Req",
    "Root_ExternalPkg_Opt",
    "Parh_ExternalPkg_Opt",
    "Path_CalledFrom",
    "Path_SourceBat",
    "Path_SourcePy",
    "Data_Params",
    "Data_Projects"
]

class Instance():
    # TEVM 的根路径
    Root_TEVM: str = os_getcwd().replace("\\", "/")

    # 可执行文件
    Path_Python: str = Root_TEVM + "/python_standalone/python.exe" # TEVM 内置的 Python 解释器.
    Path_PIP: str = Root_TEVM + "/python_standalone/Scripts/pip.exe" # TEVM 内置的 pip 工具.
    Path_WebGUI: str = Root_TEVM + "/src/tevm/gui/index.html" # WEB GUI 的 index 文件.

    # 基础文件夹
    Root_Config: str = Root_TEVM + "/config" # 配置文件夹
    Root_BatScripts: str = Root_TEVM + "/scripts" # 作为启动器的 bat 脚本文件的根目录
    Root_Temp: str = Root_TEVM + "/temp" # 临时文件文件夹
    Root_Recipes: str = Root_TEVM + "/recipe" # 配方文件夹

    # 基础文件
    Path_ProjectsJson: str = Root_Config + "/projects.json" # 配置文件.
    Path_TempExecutor: str = Root_Temp + "/temp.ps1"

    # 必要的外部依赖
    Root_ExternalPkg_Req: str = Root_TEVM + "/src/lucas-lib" # 包根路径
    Parh_ExternalPkg_Req: list[str] = [  # 分发包路径
        Root_TEVM + "/src/lucas-lib/pylucas-4.0.0-py3-none-any.whl" # Pylucas
    ]
    # 可选的外部依赖
    Root_ExternalPkg_Opt: str = Root_TEVM + "/src/site-packages" # 包根路径
    Parh_ExternalPkg_Opt: list[str] = [] # 分发包路径

    # 启动脚本
    Root_CalledFrom: str = __argv__[1].replace("\\", "/")[:-1] if __argv__.__len__() > 1 else "" # Bat 脚本文件被调用的位置
    Path_SourceBat: str = __argv__[2] if __param_useable__ else "" # 被调用的 Bat 脚本文件路径
    Path_SourcePy: str = __argv__[0].replace("\\", "/") # 被执行的 Python 脚本文件路径.

    # Data
    Data_Params: list = __argv__[3:] if __param_useable__ else []
    Data_Projects: dict = {}

    def __new__(cls):
        return {
            key: value for key, value in cls.__dict__.items()
            if not key.startswith('__') and not callable(value)
        }

    @classmethod
    def get(cls, var: ENVARS):
        if not hasattr(cls, var): raise KeyError(f"No Variable Named \"{var}\".")
        return getattr(cls, var)

def depend_import() -> bool:
    __sys_path__.insert(0, Instance.Root_ExternalPkg_Req)
    try:
        import pylucas
    except ImportError as E:
        try:
            print("必要外部库加载失败, 尝试自动安装.")
            for pkg in Instance.Parh_ExternalPkg_Req:
                sp_run(args=["pip", "install", "--target", Instance.Root_ExternalPkg_Req, pkg], shell=True)
            import pylucas
        except Exception as E:
            print(f"必要外部库自动安装失败 \"{str(E)}\", 请手动安装后重试.")
            return False
        else:
            print("必要外部库安装成功, 请重新执行程序.")
            return True
    except Exception as E:
        print("必要外部库无法加载, 发生未预期的错误, 请尝试手动排查错误.")
        return False
    else:
        return True

def init():
    if not depend_import(): __sys_exit__(0)

    from pylucas.basic import Result
    from tevm.basic import Json

    # Rebuild ProjectsJson If Not Exists
    if not path_exists(Instance.Path_ProjectsJson):
        try:
            os_makedirs(name=Instance.Root_Config, exist_ok=True)
            with open(Instance.Path_ProjectsJson, "w", encoding="utf-8") as File: File.write("{}")
        except Exception as E:
            print(f"Rebuild Projects Json Failed. \"{str(E)}\"")
            __sys_exit__(0)

    # Rebuild Temp Folder
    if not path_exists(Instance.Root_Temp):
        try:
            os_makedirs(name=Instance.Root_Temp, exist_ok=True)
        except Exception as E:
            print(f"Rebuild Temp Folder Failed. \"{str(E)}\"")
            __sys_exit__(0)

    # load Projects
    result: Result = Json.read(Instance.Path_ProjectsJson)
    if result:
        Instance.Data_Projects = result()
    else:
        print(f"Load Project Json Failed. \"{str(result)}\"")

init()

if __name__ == "__main__":
    from pprint import pprint
    pprint(Instance())
    Instance["123"]