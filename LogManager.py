import logging
import datetime

date = datetime.datetime.now().strftime('%d_%m_%y')
logger = logging.getLogger(__name__)
logFileName = "Logs/" + date + "_LogFile.log"
logging.basicConfig(filename=logFileName, encoding='utf-8',
                    format='[%(levelname)s] - %(asctime)s - %(name)s - %(message)s',
                    datefmt='%I:%M:%S %p',
                    level=10)
