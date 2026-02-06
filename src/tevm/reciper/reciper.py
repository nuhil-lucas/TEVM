from os import listdir as os_listdir
from os.path import isfile as os_isfile
from importlib.util import spec_from_file_location, module_from_spec
from importlib.machinery import ModuleSpec
from types import ModuleType
from typing import Literal

from tevm.instance import Instance
from pylucas.basic import Result
from pylucas.better_print import CPrint
from .recipe import Recipe

class Reciper():
    def __contains__(self, recipe_name: str) -> bool:
        return recipe_name in self.recipes

    def __init__(self):
        self.recipes: dict[str, Recipe] = {}

        self.load()

    def load(self):
        for recipe in os_listdir(Instance.Root_Recipes):
            if not recipe.endswith(".py"): continue
            
            module_name: str = recipe[:-3]
            module_path: str = Instance.Root_Recipes + "/" + recipe

            if not os_isfile(module_path): continue

            try:
                spec: ModuleSpec | None = spec_from_file_location(module_name, module_path)
                if spec is None or spec.loader is None:
                    raise ModuleNotFoundError(f"\"{module_name}\" Is Not A Effective Module.")
                module: ModuleType = module_from_spec(spec)
                spec.loader.exec_module(module)

                module: Recipe = module.Recipe
            except Exception as E:
                CPrint.failure(f"Load Recipe Failure \"{module_name}\": {str(E)}")
            else:
                CPrint.success(f"Loaded Recipe \"{module_name}\".")
                self.recipes[module_name] = module

    def list(self, mode: Literal["-name", "-info"] = "-name", beg: str = "") -> str:
        result: list[str] = []
        match mode:
            case "-name":
                result = [beg + recipe_name for recipe_name in self.recipes]
            case "-info":
                for recipe_name, recipe_module in self.recipes.items():
                    result += [
                        beg + recipe_name,
                        beg + f"    author: {recipe_module.author}",
                        beg + f"    version: {recipe_module.version}",
                        beg + f"    requested projects: {', '.join(recipe_module.request_project)}"
                    ]

        return "\n".join(result)

    def run(self, recipe_name: str):
        if not recipe_name in self.recipes:
            return Result(False, f"Recipe \"{recipe_name}\" Not Found.")
        
        MODULE: Recipe = self.recipes[recipe_name]
        try:
            MODULE().install()
        except Exception as E:
            return Result(False, str(E))
        else:
            return Result(True, None)

def run_recipe(path_recipe: str, params: list[str] | str = ""):
    from subprocess import run as sp_run
    sp_run(
        args=["powershell", "-Command", Instance.Path_Python, path_recipe].append("" if params == "" else "\"" + "\" \"".join(params) + "\""),
        cwd=Instance.Root_CalledFrom,
        stdout=None,
        stderr=None
    )

if __name__ == "__main__":
    from pprint import pprint
    # reciper: Reciper = Reciper()
    # reciper.list()
    # reciper.run("example")
    print(result:=Recipe.check())
    if not result: raise result.Exception
