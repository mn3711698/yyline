# -*- coding: utf-8 -*-

##############################################################################
# Author：QQ173782910
##############################################################################

try:
    import talib
except Exception as e:
    raise ValueError("talib未正确安装")
import logging
import config
import sys
from RunUse.TradeRun import TradeRun


formats = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=formats, filename='gmlog_print.txt')
logger = logging.getLogger('print')
logging.getLogger("apscheduler").setLevel(logging.WARNING)  # 设置apscheduler.


if __name__ == '__main__':  # 25
    group_name = None
    if len(sys.argv) >= 2:
        group_name = sys.argv[1]
    trader = TradeRun(config.config_raw, group_name)
    trader.start()
