from urllib.request import (
    build_opener as ulr_build_opener,
    Request as ulr_Request,
    ProxyHandler as ulr_ProxyHandler
)
from urllib.error import (
    HTTPError as ule_HTTPError,
    URLError as ule_URLError
)
from os import (
    makedirs as os_makedirs,
    remove as os_remove,
    rename as os_rename,
    listdir as os_listdir
)
from os.path import (
    dirname as osp_dirname,
    exists as osp_exists,
    normpath as osp_normpath,
    basename as osp_basename,
    splitext as osp_splitext,
    dirname as osp_dirname,
    isfile as osp_isfile,
    isdir as osp_isdir,
    join as osp_join
)
from time import (
    sleep as t_sleep,
    time as t_time
)
from sys import exit as sys_exit
from shutil import rmtree as shutil_rmtree
from json import  load as json_load
from subprocess import run as sp_run
from re import search as re_search
from typing import Literal
from pylucas.net import GitHub, GitHubReleases, download_file

def check_request(tevm_projects: list[str] = [], pypackage: list[str] = []):
    from sys import path as sys_path
    from ....instance import Projects, Root_Packages

    missing_projects: list[str] = []
    for project in tevm_projects:
        if not project.lower() in Projects: missing_projects.append(project)

    if Root_Packages not in sys_path: sys_path.insert(0, Root_Packages)
    module_list = set()
    for file_item in os_listdir(Root_Packages):
        path = osp_join(Root_Packages, file_item)
        if file_item.endswith(".py") and file_item != "__init__.py" and not file_item.startswith("_"): module_list.add(file_item[:-3])
        elif osp_isdir(path):
            init_file = osp_join(path, "__init__.py")
            if osp_isfile(init_file):
                module_list.add(file_item)

    missing_pypackage: list[str] = []
    for pypkg in pypackage:
        if not pypkg in module_list: missing_pypackage.append(pypkg)
    
    return not any([missing_projects, missing_pypackage]), {"missing_projects": missing_projects, "missing_pypackage": missing_pypackage}

class net_operate:
    proxy: dict = None
    @staticmethod
    def get_file(url: str, root: str, file_name: str) -> tuple[bool, str]:
        root: str = osp_normpath(root).replace("\\", "/")
        path: str = root + "/" + file_name
        FileSize: float = 0
        Progress: int = 0
        ChunkSize: int = 8192

        opener = ulr_build_opener() if release_github.proxy is None else ulr_build_opener(ulr_ProxyHandler(release_github.proxy))
        try:
            os_makedirs(osp_normpath(root), exist_ok=True)
            with opener.open(url, timeout=30) as response:
                FileSize = round(int(response.headers.get('Content-Length'))/1024/1024, 2)
                Progress = 0
                with open(path, "wb") as File:
                    while True:
                        Chunk = response.read(ChunkSize)
                        if not Chunk: break
                        Progress += ChunkSize
                        print(f"\rDownloading: {file_name}[{round(Progress/1024/1024, 2)} / {FileSize} MB]", end="", flush=True)
                        File.write(Chunk)
                print()
        except ule_URLError as E:
            return False, str(E.reason)
        except Exception as E:
            return False, str(E)
        else:
            return True, path

class file_operate:
    @staticmethod
    def extract(
        path_file: str,
        root_target: str,
        ignore_topdir: bool = False,
        rename_attempts: int = 20
    ) -> tuple[bool, str]:
        file_name: str = osp_splitext(osp_basename(path_file))[0]
        root_temp: str = "temp" + "/" + file_name

        try:
            # Clear Temporary Files
            if osp_exists(root_temp): shutil_rmtree(root_temp)
            if osp_exists(root_target): shutil_rmtree(root_target)

            # Extract
            if path_file.lower().endswith("gz"):
                from tarfile import open as tarfile_open

                with tarfile_open(path_file, "r:gz") as tar:
                    tar.extractall(path=root_temp, filter="data")
            elif path_file.lower().endswith("zip"):
                from zipfile import ZipFile

                with ZipFile(path_file, 'r') as zip_ref:
                    zip_ref.extractall(path=root_temp)
            else:
                raise Exception("The File Type Does Not Support Extract.")

            # Rename & Move
            for count in range(rename_attempts):
                try:
                    os_makedirs(osp_dirname(root_target), exist_ok=True)
                    if ignore_topdir == True and (dir_extractd := os_listdir(root_temp)).__len__() == 1:
                        os_rename(root_temp + "/" + dir_extractd[0], root_target)
                    else:
                        os_rename(root_temp, root_target)
                except Exception as E:
                    print(f"\rTry Rename And Move Folder: {count+1} / {rename_attempts} Times", end="", flush=True)
                    t_sleep(1)
                else:
                    print()
                    break
            else:
                print()
                raise Exception("The renaming failed. The file may be occupied abnormally. Try manually renaming \"temp/python\" to \"temp/python_standalone\" and move it to the \"projects\" folder")

            # Clear Temporary Files
            if osp_exists(path_file): os_remove(path_file)
            if osp_exists(root_temp): shutil_rmtree(root_temp)
        except Exception as E:
            return False, str(E)
        else:
            return True, root_target

    def moveto(source: str, target: str, replace: bool) -> tuple[bool, str]:
        if not osp_exists(source):
            return False, "Source Not Exists."

        try:
            if osp_exists(target) and replace: os_remove(target)
            if osp_isfile(source):
                os_makedirs(osp_dirname(target), exist_ok=True)
            else:
                os_makedirs(target, exist_ok=True)
            os_rename(source, target)
        except Exception as E:
            return False, str(E)
        else:
            return True, target

class command_execute:
    _commands_bat_: list[str] = []
    _commands_ps1_: list[str] = []
    
    @staticmethod
    def cmd(command: str | list[str]):
        if isinstance(command, str):
            command_execute._commands_bat_.append(command)
        else:
            command_execute._commands_bat_ += command

    @staticmethod
    def powershell(command: str):
        command_execute._commands_ps1_.append(command)

    @staticmethod
    def run(mode: Literal["bat", "ps1"] | None = None, command: str | list[str] = "", cwd: str = None):
        try:
            bat: str = ""
            ps1: str = ""

            scripts: dict[str] = {}
            if command_execute._commands_bat_ and (mode == "bat" or mode == None):
                bat = "\n".join(command_execute._commands_bat_)
                with open((path_bat:="./temp/command_execute.bat"), "w", encoding="utf-8") as File:
                    File.write(bat)
                scripts.append(path_bat)
                command_execute._commands_bat_ = []

            if command_execute._commands_ps1_ and (mode == "ps1" or mode == None):
                ps1 = "\n".join(command_execute._commands_ps1_)
                with open((path_ps1:="./temp/command_execute.ps1"), "w", encoding="utf-8") as File:
                    File.write(ps1)
                scripts.append(path_ps1)
                command_execute._commands_ps1_ = []

            for mode, script in scripts.items():
                match mode:
                    case "bat":
                        sp_run(args=["powershell", "-ExecutionPolicy", "Bypass", "-File", script], cwd=cwd)
                    case "ps1":
                        sp_run(args=["cmd", "/c", script], cwd=cwd)
                    case _:
                        raise Exception("Unsupported Script Types.")
        except Exception as E:
            return False, str(E)
        else:
            return True, [data for data in [bat, ps1] if data != ""]

class project_operate:
    @staticmethod
    def create(project_info: dict):
        from ..instance import Path_ConfigProjects, Projects
        from .core import Json
        from ..cli.api import __project_new__
        
        project_repeat: list[str] = []
        for project_name in project_info:
            if project_name in Projects: project_repeat.append(project_name)
        
        if project_repeat: return False, f"Project Repeat: {" ;".join(project_repeat)}."
        
        for name, project in project_info.items():
            __project_new__(
                name
            )

        return Json.json_write((Path_ConfigProjects, Projects))

