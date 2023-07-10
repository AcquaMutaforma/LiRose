import logging
import datetime


def setName(nome: str) -> logging:
    return logging.getLogger(nome)


date = datetime.datetime.now().strftime('%d_%m_%y')
logger = setName(__name__)
logFileName = "Logs/" + date + "_LogFile.log"
logging.basicConfig(filename=logFileName, encoding='utf-8',
                    format='[%(levelname)s] - %(asctime)s - %(name)s - %(message)s',
                    datefmt='%I:%M:%S %p', level=logging.DEBUG)



