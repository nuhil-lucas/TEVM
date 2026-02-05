from tevm.instance import Projects, Path_CallFrom, Params, SourceBat

if SourceBat.lower()  == "tevm":
    from tevm.cli import Execute
    Execute(Params)
elif SourceBat in Projects:
    from tevm.lib.core import Scripter
    Scripter.ps1(
        project_name=SourceBat,
        params=Params
    )
    Scripter.run(cwd=Path_CallFrom)
else:
    print(f"command {SourceBat} unfind in projects.")

from tevm.lib.func import sys_exit
sys_exit(0)
