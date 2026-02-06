# Standard
from sys import path as sys_path
# Internal
from tevm.instance import Instance
# External
from pylucas.better_print import CPrint
from pylucas.basic.func import dependency_check
sys_path.insert(-1, Instance.Root_ExternalPkg_Opt)
if not (result:=dependency_check("pywebview", "Result")):
    CPrint.error(result)
    raise result.exception(type=ImportError)
from webview import create_window, start

class API():
    def __init__(self):
        pass

    def send(self):
        pass

    def receive(self):
        pass

def runGUI(debug: bool = False) -> None:
    create_window(
        title="TEVM",
        url=f'file://{Instance.Path_WebGUI}',
        js_api=API(),
        width=1300,
        height=665,
        resizable=False
    )

    start(
        gui="edgechromium",
        debug=debug,
        icon=r"D:\User\Lucas\Desktop\256X256.ico"
    )


