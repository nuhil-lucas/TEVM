# python -m nuitka --onefile --enable-plugin=tk-inter --output-dir=dist tools/scripts/tevm-install.py

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
    rename as os_rename
)
from os.path import (
    dirname as osp_dirname,
    exists as osp_exists
)
from sys import exit as sys_exit
from shutil import rmtree as shutil_rmtree
from tarfile import open as tarfile_open
from json import  load as json_load
from subprocess import run as sp_run
from time import (
    time as t_time,
    sleep as t_sleep
)

class get_python:
    time_start: int = t_time()

    @staticmethod
    def get_release(owner: str, repo: str, proxy: str | dict = None):
        url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"

        if isinstance(proxy, str):
            proxy_handler = ulr_ProxyHandler({'http': proxy, 'https': proxy})
        elif isinstance(proxy, dict):
            proxy_handler = ulr_ProxyHandler(proxy)
        else:
            proxy_handler = None

        opener = ulr_build_opener() if proxy_handler is None else ulr_build_opener(proxy_handler)
        req = ulr_Request(url, headers={'User-Agent': 'Python-urllib'})

        try:
            with opener.open(req, timeout=10) as response:
                data = json_load(response)
        except (ule_HTTPError, ule_URLError) as E:
            return False, str(E.reason)
        except Exception as E:
            return False, str(E)
        else:
            return True,  data

    @staticmethod
    def get_url(data: dict):
        assets: list[dict[str, str]] = data["assets"] if "assets" in data else None
        if assets is None:
            return False, "Failed"

        for asset in assets:
            if asset["name"].startswith("cpython-3.12.12+") and asset["name"].endswith("-x86_64-pc-windows-msvc-install_only_stripped.tar.gz"):
                return True, (asset["name"], asset["browser_download_url"])
        else:
            return False, "Failed"

    @staticmethod
    def file_download(url: str, path: str, proxy: str | dict = None):

        if isinstance(proxy, str):
            proxy_handler = ulr_ProxyHandler({'http': proxy, 'https': proxy})
        elif isinstance(proxy, dict):
            proxy_handler = ulr_ProxyHandler(proxy)
        else:
            proxy_handler = None

        opener = ulr_build_opener() if proxy_handler is None else ulr_build_opener(proxy_handler)

        FileSize: float = 0
        Progress: int = 0
        ChunkSize: int = 8192
        try:
            os_makedirs(osp_dirname(path), exist_ok=True)
            with opener.open(url, timeout=30) as response:
                FileSize = round(int(response.headers.get('Content-Length'))/1024/1024, 2)
                Progress = 0
                with open(path, "wb") as File:
                    while True:
                        Chunk = response.read(ChunkSize)
                        if not Chunk: break
                        Progress += ChunkSize
                        print(f"\rDownloading: python-build-standalone[{round(Progress/1024/1024, 2)}MB/{FileSize}MB]", end="", flush=True)
                        File.write(Chunk)
                print()
        except ule_URLError as E:
            return False, str(E.reason)
        except Exception as E:
            return False, str(E)
        else:
            return True, path

    @staticmethod
    def file_extract(file: str, root: str):
        temp_root: str = "temp"

        try:
            if osp_exists(root + "/python_standalone"): shutil_rmtree(root + "/python_standalone")
            if osp_exists(temp_root + "/python_standalone"): shutil_rmtree(temp_root + "/python_standalone")
            if osp_exists(temp_root + "/python"): shutil_rmtree(temp_root + "/python")

            with tarfile_open(file, "r:gz") as tar:
                tar.extractall(path=temp_root, filter="data")

            for count in range(20):
                print(f"\rTry Rename And Move Folder: {count+1} Times", end="", flush=True)
                try:
                    os_makedirs(root, exist_ok=True)
                    os_rename(temp_root + "/python", root + "/python_standalone")
                except Exception as E:
                    t_sleep(1)
                else:
                    print()
                    break
            else:
                print()
                raise Exception("The renaming failed. The file may be occupied abnormally. Try manually renaming \"temp/python\" to \"temp/python_standalone\" and move it to the \"projects\" folder")

            if osp_exists(file): os_remove(file)
            if osp_exists(temp_root + "/python_standalone"): shutil_rmtree(temp_root + "/python_standalone")
            if osp_exists(temp_root + "/python"): shutil_rmtree(temp_root + "/python")

        except Exception as E:
            return False, str(E)
        else:
            return True, root

    @staticmethod
    def run(pause: bool = True):
        file_url_old: tuple[str] = ("cpython-3.12.12+20251031-x86_64-pc-windows-msvc-install_only_stripped.tar.gz", "https://github.com/astral-sh/python-build-standalone/releases/download/20251031/cpython-3.12.12%2B20251031-x86_64-pc-windows-msvc-install_only_stripped.tar.gz")

        # 获取最新一版 Release
        _state_get_release_, data = get_python.get_release(
            owner="astral-sh",
            repo="python-build-standalone",
            proxy={
                "http": "127.0.0.1:7890",
                "https": "127.0.0.1:7890"
            }
        )
        if not _state_get_release_:
            print("\033[91mError[get_release]:\n    " + data + "\033[0m")
        else:
            print("\033[94mInfo[get_release]:\n    release get success.\033[0m")

        # 获取 Release 中的指定 Asset
        _state_get_url_, file_url = get_python.get_url(data) if _state_get_release_ else (False, "get latest release asset download url failed")
        if not _state_get_url_:
            print("\033[91mError[get_url]:\n    " + file_url + "\033[0m")
            file_url = file_url_old
            print("\033[93mWarn[get_url]:\n    try to download the old python build version.\033[0m")
        else:
            print("\033[94mInfo[get_url]:\n    asset url get success.\033[0m")

        # 下载指定的 Asset
        _state_file_download_, file_path = get_python.file_download(
            file_url[1],
            f"temp/{file_url[0]}"
        )
        if not _state_file_download_:
            print("\033[91mError[file_download]:\n    " + file_path + "\033[0m")
            return False, input() if pause else None
        else:
            print("\033[94mInfo[file_download]:\n    asset download success.\033[0m")

        # 解压下载的 tar.gz 文件
        _state_file_extract_, root = get_python.file_extract(
            file_path,
            "projects"
        )
        if not _state_file_extract_:
            print("\033[91mError[file_extract]:\n    " + root + "\033[0m")
            return False, input() if pause else None
        else:
            print("\033[94mInfo[file_extract]:\n    tar.gz extract success.\033[0m")

        print("\033[94m" + f"Info[GetPython]:\n    Time Use: {t_time() - get_python.time_start}.\033[0m")
        return True, input() if pause else None

class get_pip:
    @staticmethod
    def get_script(url: str, proxy: str | dict = None):
        if isinstance(proxy, str):
            proxy_handler = ulr_ProxyHandler({'http': proxy, 'https': proxy})
        elif isinstance(proxy, dict):
            proxy_handler = ulr_ProxyHandler(proxy)
        else:
            proxy_handler = None

        opener = ulr_build_opener() if proxy_handler is None else ulr_build_opener(proxy_handler)

        data: str = ""
        try:
            with opener.open(url, timeout=10) as response:
                data = response.read().decode('utf-8')
        except (ule_HTTPError, ule_URLError) as E:
            return False, E.reason
        except Exception as E:
            return False, str(E)
        else:
            return True, data

    @staticmethod
    def run_script(data: str, python: str):
        path_script: str = "temp/get-pip.py"

        try:
            if osp_exists(path_script): os_remove(path_script)

            with open(path_script, "w", encoding="utf-8") as File:
                File.write(data)
            
            sp_run(
                [python, path_script],
                check=True
            )

            if osp_exists(path_script): os_remove(path_script)
        except Exception as E:
            return False, str(E)
        else:
            return True, None

    @staticmethod
    def run(pause: bool = True):
        path_python: str = "projects/python_standalone/python.exe"
        url_get_pip: str = "https://bootstrap.pypa.io/get-pip.py"
        if not osp_exists(path_python):
            print("\033[91mError[check_python]:\n    python not installed yet, pls install python with <get-python> first.\033[0m")
            return False, input() if pause else None

        _state_get_script_, data = get_pip.get_script(url_get_pip)
        if not _state_get_script_:
            print("\033[91mError[get_script]:\n    " + data + "\033[0m")
            return False, input() if pause else None
        else:
            print("\033[94mInfo[run_script]:\n    get get-pip.py script success.\033[0m")
        
        _state_run_script_, _ = get_pip.run_script(data, path_python)
        if not _state_run_script_:
            print("\033[91mError[run_script]:\n    " + _ + "\033[0m")
            return False, input() if pause else None
        else:
            print("\033[94mInfo[run_script]:\n    run get pip success.\033[0m")

        return True, input() if pause else None

class install_dependency:
    @staticmethod
    def pip_install(path_pip: str, path_requirements: str, root_pkg: str):
        try:
            sp_run(
                [path_pip, "install", "-r", path_requirements, "-t", root_pkg],
                check=True
            )
        except Exception as E:
            return False, str(E)
        else:
            return True, None

    @staticmethod
    def run(pause: bool = True):
        path_pip = "projects/python_standalone/Scripts/pip.exe"
        path_requirements: str = "config/requirements.txt"
        root_pkg: str = "src/tevm/site-packages"
        if not osp_exists(path_pip):
            print("\033[91mError[check_python]:\n    pip not installed yet, pls install pip with <get-pip> first.\033[0m")
            return False, input() if pause else None
        
        _state_pip_install_, _ = install_dependency.pip_install(path_pip, path_requirements, root_pkg)
        if not _state_pip_install_:
            print("\033[91mError[pip_install]:\n    " + _ + "\033[0m")
            return False, input() if pause else None
        else:
            print("\033[94mInfo[pip_install]:\n    install dependency success.\033[0m")
        
        return True, input() if pause else None

if __name__ == "__main__":
    _state_get_python_, _ = get_python.run(pause=False)
    if not _state_get_python_:
        input("Press Enter To Continue...")
        sys_exit(1)

    _state_get_pip_, _ = get_pip.run(pause=False)
    if not _state_get_pip_:
        input("Press Enter To Continue...")
        sys_exit(1)

    _state_install_dependency_, _ = install_dependency.run(pause=False)
    if not _state_install_dependency_:
        input("Press Enter To Continue...")
        sys_exit(1)
    else:
        input("Press Enter To Continue...")
