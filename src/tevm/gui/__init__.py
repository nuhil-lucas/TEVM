from .api import api
from pylucas.better_print import CPrint

_api_ = api()

def runGUI(debug: bool = False) -> None:
    from sys import path as sys_path
    from tevm.instance import Path_HTML, Root_Packages

    try:
        sys_path.insert(0, Root_Packages)
        import webview
    except ImportError:
        CPrint.error("The Dependency <pywebview> Not Installed Yet.")
        return

    from webview import create_window, start

    create_window(
        title="TEVM",
        url=f'file://{Path_HTML}',
        js_api=_api_,
        width=1300,
        height=665,
        resizable=False
    )

    start(
        gui="edgechromium",
        debug=debug,
        icon=r"D:\User\Lucas\Desktop\256X256.ico"
    )
