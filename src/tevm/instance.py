from sys import (
    path as __sys_path__,
    argv as __argv__,
    exit as __sys_exit__
)
from os import getcwd as os_getcwd
from subprocess import run as sp_run

# Usable Mark Params
__param_useable__: bool = __argv__.__len__() > 2

# Basic Data
Projects: dict = {}
SourceBat: str = __argv__[2] if __param_useable__ else ""
Params: list = __argv__[3:] if __param_useable__ else []
Root_TEVM: str = os_getcwd().replace("\\", "/") # TEVM 的根路径.

# Basic File
Root_BatScripts: str = Root_TEVM + "/scripts" # 作为启动器的 bat 脚本文件的根目录.
Root_TempFiles: str = Root_TEVM + "/temp" # 临时文件文件夹.
Root_Recipes: str = Root_TEVM + "/recipe" # 配方文件夹
Root_Config: str = Root_TEVM + "/config" # 配置文件夹

Path_CallFrom: str = __argv__[1].replace("\\", "/")[:-1] if __argv__.__len__() > 1 else "" # bat脚本文件被调用位置.
Path_PyScript: str = __argv__[0].replace("\\", "/") # 作为执行目标的 Python 脚本文件路径.
Path_ConfigProjects: str = Root_Config + "/projects.json" # 配置文件.
Path_TempPS1: str = Root_TempFiles + "/temp.ps1"

Path_Python: str = Root_TEVM + "/python_standalone/python.exe" # TEVM 内置的 Python 解释器.
Path_PIP: str = Root_TEVM + "/python_standalone/Scripts/pip.exe" # TEVM 内置的 pip 工具.

Root_Packages: str = Root_TEVM + "/src/tevm/site-packages" # 执行部分操作所需的 Python 第三方库.
Root_LucasLib: str = Root_TEVM + "/src/lucas-lib" # TEVM 内置的 Lucas-Lib 库路径.
Path_LucasLibs: list[str] = [
    Root_TEVM + "/src/lucas-lib/pylucas-4.0.0-py3-none-any.whl"
] # TEVM 内置的 pylucas 库路径.

Path_HTML: str = Root_TEVM + "/src/tevm/gui/index.html" # WEB GUI 的 index 文件.

# add site-packages to sys.path
__sys_path__.insert(0, Root_LucasLib)
try:
    import pylucas
except ImportError:
    try:
        print("Lucas-Lib 相关库加载失败, 尝试自动安装...")
        for Path_LucasLib in Path_LucasLibs:
            sp_run(args=["pip", "install", "--target", Root_LucasLib, Path_LucasLib], shell=True)
    except Exception as E:
        print(E)
        print("Lucas-Lib 相关库自动安装失败, 请手动安装后重试.")
        __sys_exit__(0)
    else:
        print("Lucas-Lib 相关库安装成功, 请重新执行程序.")
else:
    from os import makedirs as os_makedirs
    from os.path import exists as path_exists
    from .lib import Json
    from .lib.func import sys_exit

    # rebuild ConfigProjects
    if not path_exists(Path_ConfigProjects):
        try:
            if not path_exists(Root_Config):
                os_makedirs(name=Root_Config, exist_ok=True)
            with open(Path_ConfigProjects, "w", encoding="utf-8") as File:
                File.write("{}")
        except Exception as E:
            print(E)
            sys_exit(0)

    # rebuild TempDir
    if not path_exists(Root_TempFiles):
        try:
            if not path_exists(Root_TempFiles):
                os_makedirs(name=Root_TempFiles, exist_ok=True)
        except Exception as E:
            print(E)
            sys_exit(0)

    # load Projects
    if (result:=Json.read(Path_ConfigProjects)): Projects = result()
    else: raise Exception(Projects)
