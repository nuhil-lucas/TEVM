from abc import ABC, abstractmethod
from types import ModuleType

from pylucas.basic import Result

class Recipe(ABC):
    name: str = "example"
    author: str = "Author"
    version: str = "0.1.0"
    request_project: list[str] = []
    request_pypkg: dict = {}

    project_info: dict = {
        "executables": {
            "rel|/example.exe": "",
            "C://example.exe": ""
        },
        "envars": {
            "EXAMPLE_HOME": "example"
        },
        "appendcmd": []
    }

    def __init__(self):
        from .... import instance as INSTANCE
        self.INSTANCE: ModuleType = INSTANCE
        if not (check_result:=Recipe.check()):
            raise check_result.Exception
    
    @classmethod
    def check(cls) -> Result:
        from ....instance import Projects as PROJECTS
        from ...func import check_prjname

        if not check_prjname(cls.name):
            return Result(False, f"Project Name Illegal \"{cls.name}\".")
        elif cls.name in PROJECTS:
            return Result(False, f"Project \"{cls.name}\" Already Exists.")
        elif not all(key in cls.project_info for key in ["executables", "envars", "appendcmd"]):
            return Result(False, f"Project Info Missing Keys.")

        if (missing_prjs:=[project for project in cls.request_project if not project in PROJECTS]):
            return Result(False, f"Requested Projects Not Satisfied: " + ", ".join(missing_prjs))

        return Result(True, None)

    @abstractmethod
    def before_install(self):
        pass

    @abstractmethod
    def after_install(self):
        pass

    def install(self):
        self.before_install()
        self.bat_build()
        self.prj_update()
        self.after_install()

    def bat_build(self):
        from .. import Scripter
        Scripter.bat(self.name)

    def prj_update(self):
        from .. import Projecter
        Projecter._update_(self.name, self.project_info)