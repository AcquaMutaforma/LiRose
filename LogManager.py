import logging
import datetime


def setName(nome: str) -> logging.Logger:
    return logging.getLogger(nome)


date = datetime.datetime.now().strftime('%d_%m_%y')
logFileName = "Logs/" + date + "_LogFile.log"
logging.basicConfig(filename=logFileName, encoding='utf-8',
                    format='[%(levelname)s] - %(asctime)s - %(name)s - %(message)s',
                    datefmt='%I:%M:%S %p', level=logging.DEBUG)

