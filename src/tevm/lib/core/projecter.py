from typing import Literal

from pylucas.basic import Result
from ..json import Json
from ...instance import Projects as PROJECTS, Path_ConfigProjects

class Projecter():
    @staticmethod
    def _isin_(project_name: str) -> bool:
        return project_name in PROJECTS

    @staticmethod
    def _list_(mode: Literal["-name"] = "-name", beg: str = "") -> str:
        result: list[str] = []
        match mode:
            case "-name":
                result = [beg + project_name for project_name in PROJECTS]

        return "\n".join(result)

    @staticmethod
    def _get_(project_name: str) -> dict[str] | None:
        if not project_name in PROJECTS:
            return None
        return PROJECTS[project_name]

    @staticmethod
    def _update_(project_name: str, project_info: dict[str]) -> Result:
        PROJECTS[project_name] = project_info
        return Json.write(Path_ConfigProjects, PROJECTS)

    @staticmethod
    def _rem_(project_name: str) -> Result:
        if not project_name in PROJECTS:
            return Result(True, PROJECTS)
        PROJECTS.pop(project_name)
        return Json.write(file=Path_ConfigProjects, data=PROJECTS)