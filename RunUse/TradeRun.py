# -*- coding: utf-8 -*-
##############################################################################
# Author：QQ173782910
##############################################################################

import traceback
from decimal import Decimal

from utils.brokers import Broker
from getaway.send_msg import bugcode, getToday, dingding, wechat_qy
from constant.constant import (EVENT_POS_LONG, EVENT_POS_SHORT)
from utils.event import EventEngine, Event
from strategies.LineWith import LineWith
from config import (key, secret, redisc, trade_size_factor, leverage, timezone, get_symbol_metas)
from apscheduler.schedulers.background import BackgroundScheduler


class TradeRun:

    def __init__(self, config: dict, group_name: str = None):
        symbol_metas = get_symbol_metas(group_name)
        self._config = config
        self.min_volume_dict = {}
        self.symbols_list = []
        self.symbols_dict = {}
        self.trading_size_dict = {}
        self.redisc = redisc
        self.conf_initialize(symbol_metas)
        self.bugcode = bugcode
        self.wechat_qy = wechat_qy
        self.getToday = getToday
        self.dingding = dingding
        self.min_volume = 0.001
        self.key = key
        self.secret = secret

        self.engine = EventEngine()
        self.scheduler = BackgroundScheduler(timezone=timezone)
        self.broker = Broker(timezone, self.engine,
                             key=self.key, secret=self.secret, symbols_list=self.symbols_list)
        self.initialization_data()
        self.broker.add_strategy(LineWith, self.symbols_dict, self.min_volume_dict, self.trading_size_dict)

    def conf_initialize(self, symbol_metas):
        # 初始化dict
        # [symbol, trading_size, win_arg, add_arg, loss_arg, trace_win]
        for symbol, meta in symbol_metas.items():
            self.symbols_list.append(symbol)
            symbols_list = [meta['win_arg'], meta['loss_arg'], meta['trace_win'],
                            meta['long_sold'], meta['short_bought']]
            self.symbols_dict[symbol] = symbols_list
            config_trading_size = meta['trading_size']
            precision = self.calculate_precision(config_trading_size)
            trading_size = Decimal(str(config_trading_size)) * Decimal(trade_size_factor)
            if precision > 0:
                quantize_format = '0.' + int(precision) * '0'
                trading_size = trading_size.quantize(Decimal(quantize_format))
            trading_size = float(trading_size)
            self.trading_size_dict[symbol] = trading_size

    def initialization_data(self):
        try:
            exchange_infos = self.broker.binance_http.exchangeInfo()
            if isinstance(exchange_infos, dict):
                exchange_symbol_infos = exchange_infos['symbols']
                for exchange_symbol_info in exchange_symbol_infos:
                    _symbol = exchange_symbol_info['symbol']
                    if _symbol in self.trading_size_dict:
                        for j in exchange_symbol_info['filters']:
                            if j['filterType'] == 'LOT_SIZE':
                                min_qty = float(j['minQty'])
                                trading_size = self.trading_size_dict[_symbol]
                                if min_qty > trading_size:
                                    self.trading_size_dict[_symbol] = min_qty
                                    msg = f"config里的symbol:{_symbol},trading_size:{trading_size},太小,minQty{min_qty}"
                                    self.dingding(msg, _symbol)
                                    self.wechat_qy(msg, _symbol)
                                self.min_volume_dict[_symbol] = min_qty
            for _symbol in self.trading_size_dict.keys():
                self.broker.binance_http.set_leverage(_symbol, leverage)
        except:
            self.bugcode(traceback, "yyline_TradeRun_initialization_data")

    def _register_position_fetcher(self):
        self.scheduler.add_job(self.get_position, trigger='cron', id='trade_get_position', second='*/10')

    def start(self):
        self._register_position_fetcher()
        self.scheduler.start()

    def get_position(self):
        try:
            try:
                info = self.broker.binance_http.get_position_info()
            except Exception as e:
                print(e)
                info = self.broker.binance_http.get_position_info()
            if isinstance(info, list):
                for item in info:
                    symbolm = item["symbol"]
                    positionSide = item["positionSide"]
                    if symbolm in self.symbols_dict and positionSide == 'LONG':
                        event = Event(EVENT_POS_LONG, {"symbol": symbolm, "pos": item})
                        self.broker.event_engine.put(event)
                    elif symbolm in self.symbols_dict and positionSide == 'SHORT':
                        event = Event(EVENT_POS_SHORT, {"symbol": symbolm, "pos": item})
                        self.broker.event_engine.put(event)
            elif info['code'] != -1021:
                self.dingding(f"注意是不是超并发了或时间不对，{info}", "position")
                self.wechat_qy(f"注意是不是超并发了或时间不对，{info}", "position")
                self.bugcode(f"get_position:{info}")
        except:
            self.bugcode(traceback, "yyline_TradeRun_get_position")

    @staticmethod
    def calculate_precision(number):
        number_str = str(number)
        if number_str.__contains__('.'):
            precision = len(number_str) - number_str.index('.') - 1
        else:
            precision = 0
        return precision
