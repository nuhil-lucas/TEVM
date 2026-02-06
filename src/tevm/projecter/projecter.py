# Standard
from typing import Literal
# Internal
from tevm.basic.json import Json
from tevm.instance import Instance
# External
from pylucas.basic import Result

class Projecter():
    @staticmethod
    def _isin_(prj_name: str) -> bool:
        return prj_name in Instance.Data_Projects

    @staticmethod
    def _list_(mode: Literal["-name"] = "-name", beg: str = "") -> str:
        result: list[str] = []
        match mode:
            case "-name":
                result = [beg + prj_name for prj_name in Instance.Data_Projects]
            case "_":
                result = [beg + prj_name for prj_name in Instance.Data_Projects]

        return "\n".join(result)

    @staticmethod
    def _get_(prj_name: str) -> dict[str] | None:
        if not prj_name in Instance.Data_Projects:
            return None
        return Instance.Data_Projects[prj_name]

    @staticmethod
    def _update_(prj_name: str, project_info: dict[str]) -> Result:
        Instance.Data_Projects[prj_name] = project_info
        return Json.write(file=Instance.Path_ProjectsJson, data=Instance.Data_Projects)

    @staticmethod
    def _rem_(prj_name: str) -> Result:
        if not prj_name in Instance.Data_Projects:
            return Result(True, Instance.Data_Projects)
        Instance.Data_Projects.pop(prj_name)
        return Json.write(file=Instance.Path_ProjectsJson, data=Instance.Data_Projects)