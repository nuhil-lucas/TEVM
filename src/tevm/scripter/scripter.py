# Standard
from subprocess import run as sp_run
# Internal
from tevm.basic import file_remove, path_exists
from tevm.instance import Instance
# External
from pylucas.basic import Result

class Scripter():
    BatTemplate: list[str] = "\n".join([
        '@echo off',
        'set "ROOT=%~dp0.."',
        'set "CALLFROM=%CD%"',
        'set "PYTHONPATH=%ROOT%/src"',
        'cd /d "%ROOT%"',
        '"%ROOT%/projects/pystd/python.exe" -m tevm.main "%CALLFROM%." {prj_name} %*'
    ])

    @staticmethod
    def bat(prj_name: str, write: bool = True):
        """
        prj_name: 在 Shell 中调用时使用的关键字, 不区分大小写.
        """
        path_script: str = Instance.Root_BatScripts + "/" + prj_name + ".bat"
        data = Scripter.BatTemplate.format(prj_name=prj_name)

        if not write: return Result(True, data)

        try:
            with open(file=path_script, mode="w", encoding="utf-8") as File:
                File.write(data)
        except Exception as E:
            return Result(False, str(E))
        else:
            return Result(True, data)

    @staticmethod
    def ps1(prj_name: str, params: list[str], write: bool = True) -> tuple[bool, str]:
        """
        project: 项目配置数据.
        params: 被调用的可执行文件接受的参数.
        """
        try:
            file_remove(Instance.Path_TempExecutor)
        except Exception as E:
            return Result(False, str(E))

        executables: dict[str] = Instance.Data_Projects[prj_name]["executables"]
        envars: dict[str] = Instance.Data_Projects[prj_name]["envars"]

        cmd_envars: str = "\n".join([
            f"$env:{key} = \"{Instance.Root_TEVM + value[4:] if value.startswith('rel|') else value}\"" for key, value in envars.items()
        ]) + "\n"

        # 当 PowerShell 解析命令的时候, 会自动根据 " " 来分隔参数, 在此基础上, 如果存在 '"', 则会将被 双引号包裹的整段字符串视为一个参数.
        # 所以目前的解决办法只能想到用 双引号 去把所有参数全部包裹取来
        cmd_execute: str = "& " + " ".join([
            (Instance.Root_TEVM + _executable_[4:] if _executable_.startswith('rel|') else _executable_) + _params_
            for _executable_, _params_ in executables.items()
        ]) + (" " if params else "" + " ".join(params))

        if not write: return Result(True, data)

        try:
            with open(file=Instance.Path_TempExecutor, mode="w", encoding="utf-8-sig") as File:
                File.write(data:="chcp 65001 | Out-Null" + cmd_envars + cmd_execute)
        except Exception as E:
            return Result(False, str(E))
        else:
            return Result(True, data)

    @staticmethod
    def run(cwd: str):
        if not path_exists(Instance.Path_TempExecutor):
            return Result(False, f"File Not Exists \"{Instance.Path_TempExecutor}\".")

        try:
            sp_run(
                args=["powershell", "-ExecutionPolicy", "Bypass", "-File", Instance.Path_TempExecutor],
                cwd=cwd,
                stdout=None,
                stderr=None
            )
        except Exception as E:
            return Result(False, str(E))
        else:
            return Result(True, None)

if __name__ == "__main__":
    from tevm.instance import Instance

    Scripter.bat("test")

    result: Result = Scripter.ps1(prj_name="pysa", params="print('try run pysa.')", write=True)

    if result: Scripter.run(cwd=Instance.Root_TEVM)