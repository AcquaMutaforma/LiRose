import FileManager
import os

print('[] - Test File Manager ----')
print('percorso attuale:' + __file__)
percorsoCompleto = str(__file__).replace('testFileManager.py','')
print('percorso di test:' + percorsoCompleto)
filename = 'test1.txt'
try:
    fp = open(filename, 'w')
    fp.write('ciaone test 123 prova prova sa sa')
    fp.close()
    fileobj = FileManager.creaNuovoFileObj(filename=filename, dirpath=percorsoCompleto)
    print(fileobj.toDict())
except Exception as e:
    print(e)



