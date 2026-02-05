# Standard
from os import makedirs as MakeDirs
from os.path import exists as FileExists
from os.path import join as PathJoin
from os import remove as RemoveFile
# Internal
# External

def CreateTestsPY(TargetDir: str, Name: str = "Test", Type: str = ".py", Range: int | range = 10):
    if not FileExists(TargetDir):
        MakeDirs(TargetDir, exist_ok=True)
        print(f"指定的目录不存在, 已自动创建: {TargetDir}")

    if isinstance(Range, int): Range = range(1, Range+1)
    if not isinstance(Range, range): raise TypeError("参数Range必须是int或range类型")

    CreateCount: int = 0
    for FileIndex in Range:
        FilePath: str = PathJoin(TargetDir, f'{Name}_{FileIndex}{Type}')
        if FileExists(FilePath): continue
        with open(FilePath, 'w', encoding='utf-8') as File:
            File.close()
        CreateCount += 1
        print(f"已创建: {FilePath}")

    print(f"总共创建 {CreateCount} 个测试脚本.")

if __name__ == "__main__":
    CreateTestsPY(TargetDir='./tests/JavaScript', Name="JS_Test", Type=".js", Range=10)
    CreateTestsPY(TargetDir='./tests/Python', Name="Py_Test", Type=".py", Range=10)
    CreateTestsPY(TargetDir='./tests/SQL', Name="SQL_Test", Type=".sql", Range=10)
