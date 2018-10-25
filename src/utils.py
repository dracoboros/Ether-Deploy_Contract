from dracodes import FileGear as fg
import os


def contractSource(contractName, path=None):
    if path is None:
        path = f"contracts/{contractName}.sol"

    try:
        from dracodes import FileGear as fg
        try:
            return fg.fileContent(path)
        except FileNotFoundError:
            raise FileNotFoundError("File does not exist")
    except ModuleNotFoundError:
        with open(path) as solidityFile:
            return solidityFile.read()
