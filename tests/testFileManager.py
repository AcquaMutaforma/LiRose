import FileManager
import os
import unittest
import json


percorsoCompleto = str(__file__).replace('testFileManager.py', '')


"""def correggi_path(aaa: str) -> str:
    if os.name == 'nt':
        return aaa.replace('/', '\\')
    else:
        return aaa"""


class MyTestCase(unittest.TestCase):
    def test_nuovoFileObj(self):
        filename = 'tmp/test1.txt'
        fp = open(filename, 'w')
        fp.write('ciaone test 123 prova prova sa sa')
        fp.close()
        fileobj = FileManager.creaNuovoFileObj(filename=filename, dirpath=percorsoCompleto)
        self.assertIsNotNone(fileobj)
        self.assertTrue(FileManager.verificaCorrettezzaFileInConfig(y=fileobj, dirpath=percorsoCompleto))
        self.assertEqual(filename, fileobj.getFilename())
        #os.remove(filename)

    def test_loadfiles(self):
        filename = 'tmp/test2.txt'
        fp = open(filename, 'w')
        fp.write('ciaone test 123 prova prova sa sa')
        fp.close()
        fileobj = FileManager.creaNuovoFileObj(filename=filename, dirpath=percorsoCompleto)
        configFile = 'tmp/file.conf'
        conffile = open(configFile, 'w')
        conffile.write(json.dumps(fileobj.toDict()))
        conffile.close()
        lista = FileManager.loadFiles(percorsoCompleto)
        '''print(f"lista ==" +str(lista))
        self.assertEqual(0, lista[1])
        self.assertEqual(0, lista[2])
        self.assertEqual(0, lista[3])
        #os.remove(filename)'''

if __name__ == '__main__':
    unittest.main()
