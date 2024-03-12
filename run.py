import sys
from src import cpl, ide, misc, distr

vscode = ide.VSCode()
python = cpl.Python("3.12.2")
gcc = cpl.GCC("11.2.0", add_path=True)

everything = [
    ide.DevCpp(),
    vscode,
    ide.VSCodeExt(vscode, gcc),
    ide.Sublime(),
    ide.CodeBlocks(),

    cpl.GCC("13.2.0"),
    gcc,
    cpl.GCC("8.1.0"),
    python,

    misc.Gurobi(python),
    misc.GGB(),
    misc.Graph(),
]

match sys.argv[1]:
    case "prepare":
        for component in everything:
            component.prepare()
        distr.create_distr()
        
    case "install":
        for component in everything:
            component.install()
