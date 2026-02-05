from tevm.lib.core import Recipe as BaseRecipe

class Recipe(BaseRecipe):
    name: str = "example"
    author: str = "Nuhil Lucas"
    version: str = "0.1.0"
    request_project: list[str] = []

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

    def before_install(self):
        return super().before_install()

    def after_install(self):
        return super().after_install()