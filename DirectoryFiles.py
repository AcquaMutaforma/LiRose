"""
Questa classe rappresenta i files presenti all'interno di una certa cartella.
Lo scopo principale è fornire supporto a: config manager per scrittura e lettura, file manager per valutazioni,
scrittura e lettura infine è utilizzato per la valutazione dei files al caricamento della directory.
"""
import FileManager


class DirFiles:
    def __init__(self, dirpath: str):
        self.fileDict = FileManager.loadFiles(dirpath)

    def toDict(self) -> dict:
        pass
