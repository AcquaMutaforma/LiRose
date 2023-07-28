import logging
import datetime
import FileManager


def setName(nome: str) -> logging.Logger:
    return logging.getLogger(nome)


date = datetime.datetime.now().strftime('%d_%m_%y')
logFileName = FileManager.cartella_logs + date + "_LogFile.log"
logging.basicConfig(filename=logFileName, encoding='utf-8',
                    format='[%(levelname)s] - %(asctime)s - %(name)s - %(message)s',
                    datefmt='%I:%M:%S %p', level=logging.DEBUG)

