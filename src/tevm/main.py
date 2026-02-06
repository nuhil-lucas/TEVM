# Standard
# Internal
from tevm.instance import Instance
from tevm.basic.func import sys_exit
from tevm.cli import Execute
from tevm.scripter import Scripter
# External
from pylucas.better_print import CPrint

if Instance.Path_SourceBat.lower()  == "tevm":
    Execute(Instance.Data_Params)
elif Instance.Path_SourceBat in Instance.Data_Projects:
    Scripter.ps1(
        prj_name=Instance.Path_SourceBat,
        params=Instance.Data_Params
    )
    Scripter.run(cwd=Instance.Root_CalledFrom)
else:
    CPrint.error(f"Command {Instance.Path_SourceBat} Unfind In Projects.")

sys_exit(0)
