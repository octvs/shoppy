import subprocess
import shutil
from pathlib import Path

shoppy_exec = Path.home().joinpath(".local/bin/shoppy")
print(shoppy_exec)
if not shoppy_exec.exists():
    print(Path(__file__).parent.joinpath("shoppy"))
    print("Copying executable to .local/bin")
    shutil.copy(shoppy_exec, Path(__file__).parent.joinpath("shoppy"))
else:
    print("Executable exists")
