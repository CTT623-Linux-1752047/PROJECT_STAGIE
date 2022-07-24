import logging
from common.Const import Const

class Log:
    def writeLog(message):
        logging.basicConfig(filename=f"./Log/{Const.DATE_CD_DMYHMS}_log.txt", encoding='utf-8')
        # logging.error(f" {Const.DATE_DMYHMS} - :  {message}")
        return (f"{Const.DATE_DMYHMS} - :  {message}")
        


    def writeNotification(codeMessage, lstParam=[]):
        logging.basicConfig(filename=f"./Log/{Const.DATE_CD_DMYHMS}_log.txt", encoding='utf-8')
        message = codeMessage
        if lstParam :
            cnt = 0
            for param in lstParam :
                message = message.replace(Const.CURLY_BRACKETS_OPEN + str(cnt) + Const.CURLY_BRACKETS_CLOSE, param)
                cnt =+1
        logging.warning(f" {Const.DATE_DMYHMS} - {message}")
        return (f" {Const.DATE_DMYHMS} - {message}")