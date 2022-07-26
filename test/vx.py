#微信推送

import requests
from loguru import logger

serverKey = "SCT67036TtYWf92opesnpjGwOhJYWZiIB"

def post(vxtitle,vxtext):
    if(serverKey == ""):
        logger.info("没有KEY，不推送")
        return False
    url = "https://sctapi.ftqq.com/" + serverKey+".send"
    print(url+"|"+vxtitle+"|"+vxtext)
    data = {
    "text":vxtitle,
    "desp":vxtext
    }
    try:
        r = requests.post(url, data)
        logger.info("微信推送成功")
        return True
    except:
        logger.error("微信推送失败")
        return False