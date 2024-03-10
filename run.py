from src import ide, cpl
base = [ide.DevCpp()]

# for cls in base:
#     cls.install()

vscode = ide.VSCode()
vscode.install()

add_ons = [ide.VSCodeExt("python", vscode)]

for cls in add_ons:
    cls.install()
