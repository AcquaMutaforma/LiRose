import DirFilesManager
import os
import unittest
import json
import ConfigManager


percorsoCompleto = str(__file__).replace('testFileManager.py', '')


class MyTestCase(unittest.TestCase):
    def test_nuovoElementoFile(self):
        filename = 'tmp/test1.txt'
        fp = open(filename, 'w')
        fp.write('ciaone test 123 prova prova sa sa')
        fp.close()
        fileobj = FileManager.__creaElementoFile(filename=filename, dirpath=percorsoCompleto)
        print(f"Elemento File creato = {fileobj.toDict()}")
        self.assertIsNotNone(fileobj)
        self.assertEqual(filename, fileobj.getFilename())
        os.remove(filename)
        print(f"File {filename} eliminato")

    def test_nuovoElementoDir(self):
        nomeDir = '/aaa'
        percorsoDir = percorsoCompleto + nomeDir
        try:
            os.rmdir(percorsoDir)
        except FileNotFoundError:
            pass
        os.mkdir(percorsoDir)
        aaa = FileManager.__creaElementoDir(dirname=nomeDir)
        self.assertIsNotNone(aaa)
        self.assertEqual([], aaa.toDict().get('contenuto'))
        os.rmdir(percorsoDir)

    def test_configurazione(self):
        filename = 'tmp/test2.txt'
        fp = open(filename, 'w')
        fp.write('ciaone test 123 prova prova sa sa')
        fp.close()
        configFile = ConfigManager.confFile
        configurazione = FileManager.getConfigurazione(percorsoCompleto + '/tmp/')
        conffile = open(configFile, 'w')
        conffile.write(json.dumps(configurazione))
        conffile.close()
        os.remove(filename)


if __name__ == '__main__':
    unittest.main()
