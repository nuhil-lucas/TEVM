from typing import Literal, Callable
from os.path import exists as Path_Exists, isabs as Path_IsABS, normpath as Path_NormPath
from ..instance import (
    Projects as PROJECTS,
    Path_ConfigProjects,
    Path_CallFrom,
    Root_BatScripts,
    # Path_Python,
    # Root_TEVM,
    # Root_Recipes
)
from ..lib.func import file_remove, check_prjname, input
from ..lib.core import Projecter, Scripter, Reciper
from ..lib import Json
from pylucas.basic import Result
from pylucas.better_print import CPrint

def Execute(): pass
def __help__(): pass
def __run__(): pass
def __recipe__(): pass
def __recipe_run__(): pass
def __recipe_list__(): pass
def __project__(): pass
def __project_gui__(): pass
def __project_list__(): pass
def __project_new__(): pass
def __project_rem__(): pass
def __project_modify__(): pass
def __show__(): pass

CMDS: dict[str, dict[str]] = {
    "description": "TEVM, Your Env Manage Helper.",
    "sub": {
        "help": {
            "description": "command help of tevm.",
            "sub": {},
            "call": __help__
        },
        "run": {
            "description": "run the project.",
            "sub": {
                "--name": {
                    "description": "Name Of Project.",
                    "sub": {},
                    "call": None
                }
            },
            "call": __run__
        },
        "recipe": {
            "description": "run the project.",
            "sub": {
                "run": {
                    "description": "Run Target Recipe.",
                    "sub": {
                        "--name": {
                            "description": "Name Of Project.",
                            "sub": {},
                            "call": None
                        },
                    },
                    "call": __recipe_run__
                },
                "list": {
                    "description": "List All Recipe.",
                    "sub": {
                        "-name": {
                            "description": "List All Recipe Name.",
                            "sub": {},
                            "call": None
                        },
                        "-info": {
                            "description": "List All Recipe Info.",
                            "sub": {},
                            "call": None
                        }
                    },
                    "call": __recipe_list__
                }
            },
            "call": __run__
        },
        "project": {
            "description": "Project Projects With TEVM, Additionally, \"prj\" Is Also A Supported Command.",
            "sub": {
                "gui": {
                    "description": "A Web GUI For User To Project.",
                    "sub": {
                        "-debug": {
                            "description": "Open The Debug Console.",
                            "sub": {},
                            "call": None
                        }
                    },
                    "call": __project_gui__
                },
                "list": {
                    "description": "List All Project, Default With \"-name\" Mode.",
                    "sub": {
                        "-name": {
                            "description": "List All Project Name.",
                            "sub": {},
                            "call": None
                        }
                    },
                    "call": __project_list__
                },
                "new": {
                    "description": "Add New Project.",
                    "sub": {
                        "--name": {
                            "description": "Name Of Project.",
                            "sub": {},
                            "call": None
                        }
                    },
                    "call": __project_new__
                },
                "rem": {
                    "description": "Remove Project.",
                    "sub": {
                        "--name": {
                            "description": "Name Of Project.",
                            "sub": {},
                            "call": None
                        }
                    },
                    "call": __project_rem__
                },
                "modify": {
                    "description": "Modfiy Project.",
                    "sub": {
                        "--name": {
                            "description": "Name Of Project.",
                            "sub": {},
                            "call": None
                        }
                    },
                    "call": __project_modify__
                },
            },
            "call": __project__
        }
    },
    "call": Execute
}

def Execute(params: str | list[str]):
    if params.__len__() == 0:
        params.append("help")
    match params[0].lower():
        case "help":
            if params.__len__() == 1:
                __help__(help_level="info")
            else:
                __help__(
                    msg=f"Unknow Command: tevm {" ".join(params)}",
                    help_level="error"
                )
        case "run":
            __run__(params[1:])
        case "recipe":
            __recipe__(params[1:])
        case "project":
            __project__(params[1:])
        case "prj":
            __project__(params[1:])
        case _:
            __help__(
                msg=f"Unknow Command: tevm {" ".join(params)}",
                help_level="error"
            )

def __help__(
        msg: str | Literal["Unknow Command"] = None,
        help_params: list[str] = [],
        help_level: Literal["error", "warn", "info"] = "info"
    ):
    _cprint: Callable = None
    match help_level:
        case "error":
            _cprint = CPrint.error
        case "warn":
            _cprint = CPrint.warn
        case "info":
            _cprint = CPrint.info
        case _:
            CPrint.error(f"A Non-Existent Help Level: {help_level}")
            return

    if not help_level == "info":
        _cprint(help_level.upper(), end="\n")

    if msg:
        _cprint("    " + msg, end="\n\n")
    
    zCMDS = CMDS
    for key in help_params:
        zCMDS = zCMDS["sub"][key]

    CPrint.info(f'Command:\n    [tevm]{" " if help_params else ""}{" ".join(help_params)}: {zCMDS["description"]}')

    def PrintSub(zCMDS: dict, index: int = 2):
        for key in zCMDS["sub"]:
            CPrint.info(f'{"    " * index}[{key}]: {zCMDS["sub"][key]["description"]}')
            if zCMDS["sub"][key]["sub"]:
                PrintSub(zCMDS["sub"][key], index+1)
    PrintSub(zCMDS)

def __run__(params: list[str]):
    if params.__len__() == 0:
        __help__(
            help_params=["run"],
            help_level="info"
        )
        return
    elif params.__len__() > 1:
        __help__(
            msg=f"Unknow Command: tevm run {" ".join(params)}",
            help_params=["run"],
            help_level="error"
        )
        return

    Project_Name: str = params[0].lower()
    if not Project_Name in PROJECTS:
        CPrint.error(f"Project {Project_Name} Not Exists.")
        return

    Scripter.ps1(
        project_name=Project_Name,
        params=params[1:]
    )
    Scripter.run(cwd=Path_CallFrom)

def __recipe__(params: list[str]):
    if params.__len__() == 0:
        __help__(
            help_params=["recipe"],
            help_level="info"
        )
        return

    match params[0]:
        case "run":
            __recipe_run__(params[1:])
        case "list":
            __recipe_list__(params[1:])
        case _:
            __help__(
                msg=f"Unknow Command: tevm recipe {" ".join(params)}",
                help_params=["recipe"],
                help_level="error"
            )

def __recipe_run__(params: list[str]):
    if params.__len__() == 0:
        __help__(
            help_params=["recipe", "run"],
            help_level="info"
        )
        return
    elif params.__len__() > 1:
        __help__(
            msg=f"Unknow Command: tevm recipe run {" ".join(params)}",
            help_params=["recipe", "run"],
            help_level="error"
        )
        return
    
    recipe_name: str = params[0]
    reciper: Reciper = Reciper()

    if not recipe_name in reciper:
        CPrint.error(f"\nRecipe {recipe_name} Not Exists.")
        return
    
    result: Result = reciper.run(recipe_name)

    if not result:
        CPrint.failure(f"\nFailed To Run Recipe \"{recipe_name}\": [{result()}]")
    else:
        CPrint.success(f"\nSucceed To Run Recipe \"{recipe_name}\".")

def __recipe_list__(params: list[str]):
    if params.__len__() > 1 or (params and not params[0] in CMDS["sub"]["recipe"]["sub"]["list"]["sub"]):
        __help__(
            msg=f"Unknow Command: tevm recipe list {" ".join(params)}",
            help_params=["recipe", "list"],
            help_level="error"
        )
        return

    reciper: Reciper = Reciper()
    CPrint.info("\nTEVM Recipes List:")
    CPrint.info(reciper.list(*params, beg="    "))

def __project__(params: list[str]):
    if params.__len__() == 0:
        __help__(
            help_params=["project"],
            help_level="info"
        )
        return
    match params[0].lower():
        case "gui":
            __project_gui__(params[1:])
        case "list":
            __project_list__(params[1:])
        case "new":
            __project_new__(params[1:])
        case "rem":
            __project_rem__(params[1:])
        case "modify":
            __project_modify__(params[1:])
        case _:
            __help__(
                msg=f"Unknow Command: tevm project {" ".join(params)}",
                help_params=["project"],
                help_level="error"
            )

def __project_gui__(params: list[str]):
    CPrint.warn(f"This Features Has Not Been Realized Yet.")

    from ..gui import runGUI
    if params.__len__() == 0:
        runGUI()
    elif params.__len__() == 1 and params[0].lower() == "-debug":
        runGUI(debug=True)
    else:
        __help__(
            msg=f"Unknow Command: tevm project gui {" ".join(params)}",
            help_params=["project", "gui"],
            help_level="error"
        )

def __project_list__(params: list[str]):
    if params.__len__() > 1 or (params and not params[0] in CMDS["sub"]["project"]["sub"]["list"]["sub"]):
        __help__(
            msg=f"Unknow Command: tevm project list {" ".join(params)}",
            help_params=["project", "list"],
            help_level="error"
        )
        return
    
    CPrint.info("TEVM Projects List:")
    CPrint.info(Projecter._list_(*params, beg="    "))

def __project_new__(params: list[str]):
    if params.__len__() != 1:
        __help__(
            msg="Param Missing: Project Name Not Filled In." if params.__len__() == 0 else f"Unknow Command: tevm project new {" ".join(params)}",
            help_params=["project", "new"],
            help_level="error"
        )
        return

    project_name = params[0].lower() if params.__len__() == 1 else ""
    project_info: dict = {
        "executables": {},
        "envars": {},
        "appendcmd": []
    }

    # 项目名称检查
    if not check_prjname(project_name):
        CPrint.error("Project Name Only Allowed Contain ASCII Lowercase Letters \"[a-z]\" And Underscores \"_\".")
        return
    if project_name in PROJECTS:
        CPrint.error(f"Project {project_name} Already Exists.") 
        return

    # 可执行文件与执行参数
    info_exec: dict[str] = {}
    keep_loop: bool = True
    CPrint.info("Input <N> To Finish.\nInput Should Format As \"Executable File: Parameters\"")
    while keep_loop:
        # 输入接收
        _input_: str | list[str] | None = input("\nExecutable & Param: ")

        # 结束输入检查
        if _input_.lower() == "n":
            if not input("End Now? (y/n): ").lower() == "y":
                continue
            if info_exec:
                keep_loop = False
                continue
            else:
                CPrint.warn("Please Specify The Executable File.")
                continue
        else:
            colon_index: int = _input_.find(":")

        exec: str = (_input_ if colon_index == -1 else _input_[: colon_index]).strip()
        param: str = "" if colon_index == -1 else _input_[colon_index+1: ].strip()

        # 引号识别
        if exec.__len__() > 2 and exec[0] == exec[-1] in ("\"", "'"):
            exec = exec[1:-1]

        # 文件存在性校验
        if Path_Exists(exec):
            # 判断相对路径并转换格式
            if Path_IsABS(exec):
                exec = exec.replace("\\", "/")
            else:
                exec = "rel|/" + Path_NormPath(exec).replace("\\", "/")
        else:
            CPrint.error(f"Executable File Not Exists. [{exec}]")
            continue

        info_exec[exec] = param
    else:
        CPrint.info("\nExecutables:")
        for exec, param in info_exec.items():
            CPrint.info(f"    {exec}: {param}")

    # 环境变量
    info_envar: dict = {}
    keep_loop: bool = True
    CPrint.info("\nInput <N> To Finish.\nInput Should Format As \"Key Of EnvVar: Value Of EnvVar\"")
    while keep_loop:
        _input_: str | list[str] | None = input("\nKey & Value: ")

        if _input_.lower() == "n":
            if not input("End Now? (y/n)").lower() == "y":
                continue
            keep_loop = False
            continue
        elif _input_ == "":
            CPrint.error("Please Specify The Key & Value.")
        else:
            colon_index: int = _input_.find(":")

        key: str = (_input_ if colon_index == -1 else _input_[: colon_index]).strip()
        value: str = "" if colon_index == -1 else _input_[colon_index+1: ].strip()

        info_envar[key] = value
    else:
        CPrint.info("\nEnvars:")
        for key, value in info_envar.items():
            CPrint.info(f"    \"{key}\": \"{value}\"")

    # 附加指令
    info_append_cmd: list[str] = []
    keep_loop: bool = True
    CPrint("\nInput <N> To Finish.")
    while keep_loop:
        _input_: str | list[str] | None = input("Command: ")

        if _input_.lower() == "n":
            if not input("Sure The Finish? (y/n)").lower() == "y":
                continue
            keep_loop = False
            continue
        elif _input_ == "":
            continue
        else:
            info_append_cmd.append(_input_)
    else:
        CPrint.info("\nAppendCMD:")
        for cmd in info_append_cmd:
            CPrint.info(f"    {cmd}")

    project_info["executables"] = info_exec
    project_info["envars"] = info_envar
    project_info["appendcmd"] = info_append_cmd

    # 写入配置文件
    result: Result = Projecter._update_(project_name, project_info)
    if not result: CPrint.failure(f"Failed To Create A New Project: [{result()}]")

    # 生成bat脚本
    Scripter.bat(project_name)

def __project_rem__(params: list[str]):
    Project_Name: str = ""
    match params.__len__():
        case 0:
            __help__(
                help_params=["project", "rem"],
                help_level="info"
            )
            return
        case 1:
            Project_Name = params[0]
        case _:
            __help__(
                msg=f"Unknow Command: tevm project rem {" ".join(params)}",
                help_params=["project", "rem"],
                help_level="error"
            )
            return

    if not Project_Name in PROJECTS:
        CPrint.error(f"Project {Project_Name} Not Exists.")
    else:
        file_remove(Root_BatScripts + "/" + Project_Name + ".bat")
        PROJECTS.pop(Project_Name)
        result: Result = Json.write(Path_ConfigProjects, PROJECTS)
        if not result: CPrint(result)

def __project_modify__(params: list[str]):
    CPrint.warn(f"This Features Has Not Been Realized Yet.")

    if params.__len__() == 0:
        __help__(
            help_params=["project", "modify"],
            help_level="info"
        )
        return

    Project_Name: str = params[0].lower()

    if not Project_Name in PROJECTS:
        CPrint.error(f"Project {Project_Name} Not Exists.")
        return

if __name__ == "__main__":
    # __help__(msg="123123", help_params=["project"])
    # __project_new__(["test", "1"])
    pass