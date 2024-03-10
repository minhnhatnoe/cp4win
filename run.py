from src import cpl, ide, misc

vscode = ide.VSCode()
python = cpl.Python("3.12.2")

everything = [
    vscode,
    ide.VSCodeExt(vscode),
    ide.DevCpp(),
    ide.Sublime(),
    ide.CodeBlocks(),

    cpl.GCC("13.2.0"),
    cpl.GCC("11.2.0", add_path=True),
    cpl.GCC("8.1.0"),
    python,

    misc.GGB(),
    misc.Gurobi(python),
]

for component in everything:
    # component.prepare()
    component.install()
