from src.ide import vscode
import logging


logging.getLogger().setLevel(logging.INFO)
vscode.VSCode().install()
