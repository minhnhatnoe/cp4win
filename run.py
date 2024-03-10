from src import ide, cpl, misc

vscode = ide.VSCode()
ides = [ide.DevCpp(), ide.CodeBlocks(), ide.Sublime(), vscode]
exts = [ide.VSCodeExt(vscode)]
cpls = [cpl.GCC("13.2.0"), cpl.GCC("11.2.0"), cpl.GCC("8.1.0"), cpl.Python("3.12.2")]
miscs = [misc.GGB()]

a = cpl.Python("3.12.2")
a.install()

s = misc.Gurobi(a)
s.prepare()
s.install()
