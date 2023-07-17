"""Classe che contiene le differenze tra gli oggetti presenti in locale e la configurazione che viene comparata"""
import DirFilesManager


class Diff:
    def __init__(self, dirpath: str, confEsternaPath: str):
        """aggiunti, rimossi, diversi -- fonte A(local) e B(local/remote) le metto? i percorsi delle conf (path e 'tmp'Path)? """


# todo
def confrontaConfigEsterna(dirpath: str, confEsterna) -> Diff:
    pass
    # NOTA: nella valutazione, se l'hash è uguale, skippo
    '''def test() -> [list, list]:
    a = ['a','1']
    b = ['b', '2']
    return a, b
    t, _ = test()
    print(f"t = {t}")'''
