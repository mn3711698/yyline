# -*- coding: utf-8 -*-
##############################################################################
# Author：QQ173782910
##############################################################################

from strategies import Base


class LineWith(Base):

    def on_pos_long_data(self, symbol, pos_dict):
        # 先判断是否有仓位，如果是多头的仓位， 然后检查下是多头还是空头，设置相应的止损的价格..
        current_pos = float(pos_dict['positionAmt'])
        pos = self.long_pos_dict.get(symbol, 0)
        if pos != current_pos:  # 检查仓位是否是一一样的.
            open_orders = self.broker.binance_http.get_open_orders(symbol)
            buy_flag = 0
            sell_flag = 0
            if isinstance(open_orders, list) and len(open_orders) > 0:
                for o in open_orders:
                    if o["side"] == 'BUY':  # 开多未成交
                        buy_flag = 1
                    elif o["side"] == 'SELL':  # 平仓未成交
                        sell_flag = 1

            if current_pos == 0 and buy_flag == 0:  # 无持仓且不存在开仓单
                msg = f"多方向仓位检查:{symbol},交易所帐户仓位为0，无持仓，系统仓位为:{pos},重置为0"
                self.dingding(msg, symbol)
                self.wechat_qy(msg, symbol)
                self.long_pos_dict[symbol] = 0
            elif current_pos != 0 and sell_flag == 0:  # 有持仓且不存在平仓单
                info = self.broker.binance_http.get_position_info()
                if isinstance(info, list):
                    for item in info:
                        symbolm = item["symbol"]
                        positionSide = item["positionSide"]
                        if symbolm == symbol and positionSide == 'LONG':
                            current_pos = float(item['positionAmt'])
                if current_pos == 0:
                    return
                msg = f"多方向仓位检查:{symbol},交易所仓位为:{current_pos},系统仓位为:{pos},重置为:{current_pos}"
                self.dingding(msg, symbol)
                self.wechat_qy(msg, symbol)
                self.long_pos_dict[symbol] = current_pos

        if current_pos != 0:
            unRealizedProfit = float(pos_dict['unRealizedProfit'])
            entryPrice = float(pos_dict['entryPrice'])

            if self.long_enter_price_dict.get(symbol, 0) == 0 or self.long_enter_price_dict.get(symbol, 0) != entryPrice:
                self.long_enter_price_dict[symbol] = entryPrice
                self.long_win_price_dict[symbol] = entryPrice * 1.015
                self.long_trigger_price_dict[symbol] = entryPrice * (1 + self.long_win_args_dict.get(symbol, 0))
                self.long_loss_price_dict[symbol] = entryPrice * (1 - self.long_loss_args_dict.get(symbol, 0))
                # msg = f"多方向:{self.long_win_price_dict[symbol]},{self.long_trigger_price_dict[symbol]}"
                # msg += f",{self.long_loss_price_dict[symbol]}"
                # self.dingding(msg, symbol)
                self.long_high_price_dict[symbol] = entryPrice
                self.long_low_price_dict[symbol] = entryPrice

            self.long_unRealizedProfit_dict[symbol] = unRealizedProfit
            maxunRealizedProfit = self.long_maxunRealizedProfit_dict.get(symbol, 0)
            lowProfit = self.long_lowProfit_dict.get(symbol, 0)
            if self.long_unRealizedProfit_dict.get(symbol, 0) > 0:
                self.long_maxunRealizedProfit_dict[symbol] = max(maxunRealizedProfit, unRealizedProfit)
            elif self.long_unRealizedProfit_dict.get(symbol, 0) < 0:
                self.long_lowProfit_dict[symbol] = min(lowProfit, unRealizedProfit)

    def on_pos_short_data(self, symbol, pos_dict):
        # 先判断是否有仓位，如果是多头的仓位， 然后检查下是多头还是空头，设置相应的止损的价格..
        current_pos = float(pos_dict['positionAmt'])
        pos = self.short_pos_dict.get(symbol, 0)
        if pos != current_pos:  # 检查仓位是否是一一样的.
            open_orders = self.broker.binance_http.get_open_orders(symbol)
            buy_flag = 0
            sell_flag = 0
            if isinstance(open_orders, list) and len(open_orders) > 0:
                for o in open_orders:
                    if o["side"] == 'SELL':  # 开空未成交
                        buy_flag = 1
                    elif o["side"] == 'BUY':  # 平仓未成交
                        sell_flag = 1

            if current_pos == 0 and buy_flag == 0:  # 无持仓且不存在开仓单
                msg = f"空方向仓位检查:{symbol},交易所帐户仓位为0，无持仓，系统仓位为:{pos},重置为0"
                self.dingding(msg, symbol)
                self.wechat_qy(msg, symbol)
                self.short_pos_dict[symbol] = 0
            elif current_pos != 0 and sell_flag == 0:  # 有持仓且不存在平仓单
                info = self.broker.binance_http.get_position_info()
                if isinstance(info, list):
                    for item in info:
                        symbolm = item["symbol"]
                        positionSide = item["positionSide"]
                        if symbolm == symbol and positionSide == 'SHORT':
                            current_pos = float(item['positionAmt'])
                if current_pos == 0:
                    return
                msg = f"空方向仓位检查:{symbol},交易所仓位为:{current_pos},系统仓位为:{pos},重置为:{current_pos}"
                self.dingding(msg, symbol)
                self.wechat_qy(msg, symbol)
                self.short_pos_dict[symbol] = current_pos

        if current_pos != 0:
            unRealizedProfit = float(pos_dict['unRealizedProfit'])
            entryPrice = float(pos_dict['entryPrice'])

            if self.short_enter_price_dict.get(symbol, 0) == 0 or self.short_enter_price_dict.get(symbol, 0) != entryPrice:
                self.short_enter_price_dict[symbol] = entryPrice
                self.short_win_price_dict[symbol] = entryPrice * 0.985
                self.short_trigger_price_dict[symbol] = entryPrice * (1 - self.short_win_args_dict.get(symbol, 0))
                self.short_loss_price_dict[symbol] = entryPrice * (1 + self.short_loss_args_dict.get(symbol, 0))
                # msg = f"空方向:{self.short_win_price_dict[symbol]},{self.short_trigger_price_dict[symbol]}"
                # msg += f",{self.short_loss_price_dict[symbol]}"
                # self.dingding(msg, symbol)
                self.short_high_price_dict[symbol] = entryPrice
                self.short_low_price_dict[symbol] = entryPrice

            self.short_unRealizedProfit_dict[symbol] = unRealizedProfit
            maxunRealizedProfit = self.short_maxunRealizedProfit_dict.get(symbol, 0)
            lowProfit = self.short_lowProfit_dict.get(symbol, 0)
            if self.short_unRealizedProfit_dict.get(symbol, 0) > 0:
                self.short_maxunRealizedProfit_dict[symbol] = max(maxunRealizedProfit, unRealizedProfit)
            elif self.short_unRealizedProfit_dict.get(symbol, 0) < 0:
                self.short_lowProfit_dict[symbol] = min(lowProfit, unRealizedProfit)

    def on_ticker_long_data(self, ticker):
        symbol = ticker['symbol']
        if symbol in self.symbol_dict:
            self.last_price_dict[symbol] = float(ticker['last_price'])  # 最新的价格.
            if self.long_pos_dict.get(symbol, 0) != 0:
                if self.long_high_price_dict.get(symbol, 0.0) > 0.0:
                    self.long_high_price_dict[symbol] = max(self.long_high_price_dict.get(symbol, 0.0),
                                                            self.last_price_dict.get(symbol, 0.0))
                if self.long_low_price_dict.get(symbol, 0.0) > 0.0:
                    self.long_low_price_dict[symbol] = min(self.long_low_price_dict.get(symbol, 0.0),
                                                           self.last_price_dict.get(symbol, 0.0))
            now_enter_price = self.long_enter_price_dict.get(symbol, 0)
            if self.long_pos_dict.get(symbol, 0) > 0 and now_enter_price > 0 and self.only_msg == 0:  # 多单持仓
                if self.last_price_dict.get(symbol, 0) > self.long_win_price_dict.get(symbol, 0) > 0:
                    # 止盈处理
                    self.long_win_dict[symbol] = 0
                    self.long_enter_price_dict[symbol] = 0
                    trading_size = self.long_pos_dict.get(symbol)
                    self.long_pos_dict[symbol] = 0
                    res_sell = self.long_sell(symbol, 100, trading_size, mark=True)
                    low_profit = self.long_lowProfit_dict.get(symbol, 0)
                    low_price = self.long_low_price_dict.get(symbol, 0)
                    high_price = self.long_high_price_dict.get(symbol, 0)
                    rt = (self.last_price_dict.get(symbol, 0) - now_enter_price) * trading_size
                    Profit = self.round_to(rt, 0.0001)
                    self.dingding(f"止盈平多,交易所返回:{res_sell}", symbol)
                    self.wechat_qy(f"止盈平多,交易所返回:{res_sell}", symbol)
                    HYJ_jd_first = "止盈平多:交易对:%s,最大浮亏损:%s,最大浮利润:%s,当前浮利润:%s,仓位:%s" % (
                        symbol, low_profit, self.long_maxunRealizedProfit_dict.get(symbol, 0),
                        self.long_unRealizedProfit_dict.get(symbol, 0), trading_size)
                    HYJ_jd_tradeType = "止盈"
                    HYJ_jd_curAmount = f"{now_enter_price}"
                    HYJ_jd_remark = "预计利润:%s,最新价:%s,最高价:%s,最低价:%s" % (
                        Profit, self.last_price_dict.get(symbol, 0), high_price, low_price)
                    if "code" in res_sell:
                        HYJ_jd_remark += f'{res_sell}'
                    else:
                        random_no = self.redisc.get('%s_random_no' % symbol)
                        if random_no:
                            randomno = random_no.decode("utf8")
                        else:
                            randomno = ''
                        self.log_msg_send(symbol, low_profit, low_price, Profit, high_price, now_enter_price, randomno)
                    self.long_pos_time_dict[symbol] = ''
                    self.long_high_price_dict[symbol] = 0
                    self.long_low_price_dict[symbol] = 0
                    self.long_maxunRealizedProfit_dict[symbol] = 0
                    self.long_unRealizedProfit_dict[symbol] = 0
                    self.long_lowProfit_dict[symbol] = 0
                    self.wx_send_msg(HYJ_jd_first, HYJ_jd_tradeType, HYJ_jd_curAmount, HYJ_jd_remark)

                elif self.long_loss_price_dict.get(symbol, 0) > self.last_price_dict.get(symbol, 0) > 0:
                    # 止损
                    self.long_win_dict[symbol] = 0
                    self.long_enter_price_dict[symbol] = 0
                    trading_size = self.long_pos_dict.get(symbol)
                    self.long_pos_dict[symbol] = 0
                    res_sell = self.long_sell(symbol, 100, abs(trading_size), mark=True)
                    low_profit = self.long_lowProfit_dict.get(symbol, 0)
                    low_price = self.long_low_price_dict.get(symbol, 0)
                    high_price = self.long_high_price_dict.get(symbol, 0)
                    rt = (self.last_price_dict.get(symbol, 0) - now_enter_price) * trading_size
                    Profit = self.round_to(rt, 0.0001)
                    self.dingding(f"止损平多,交易所返回:{res_sell}", symbol)
                    self.wechat_qy(f"止损平多,交易所返回:{res_sell}", symbol)
                    HYJ_jd_first = "止损平多:交易对:%s,最大浮亏:%s,最大浮利:%s,当前浮亏:%s,仓位:%s" % (
                        symbol, low_profit, self.long_maxunRealizedProfit_dict.get(symbol, 0),
                        self.long_unRealizedProfit_dict.get(symbol, 0), trading_size)
                    HYJ_jd_tradeType = "止损"
                    HYJ_jd_curAmount = f"{now_enter_price}"
                    HYJ_jd_remark = "预计亏损:%s,最新价:%s,最高价:%s,最低价:%s" % (
                        Profit, self.last_price_dict.get(symbol, 0), high_price, low_price)
                    if "code" in res_sell:
                        HYJ_jd_remark += f'{res_sell}'
                    else:
                        random_no = self.redisc.get('%s_random_no' % symbol)
                        if random_no:
                            randomno = random_no.decode("utf8")
                        else:
                            randomno = ''
                        self.log_msg_send(symbol, low_profit, low_price, Profit, high_price, now_enter_price, randomno)
                    self.long_pos_time_dict[symbol] = ''
                    self.long_high_price_dict[symbol] = 0
                    self.long_low_price_dict[symbol] = 0
                    self.long_maxunRealizedProfit_dict[symbol] = 0
                    self.long_unRealizedProfit_dict[symbol] = 0
                    self.long_lowProfit_dict[symbol] = 0
                    self.wx_send_msg(HYJ_jd_first, HYJ_jd_tradeType, HYJ_jd_curAmount, HYJ_jd_remark)

                elif self.long_win_dict.get(symbol, 0) == 1 and self.long_high_price_dict.get(symbol, 0.0) > 0.0:
                    # 追踪多单止盈处理
                    self.trigger_long(symbol, now_enter_price)
                elif self.last_price_dict.get(symbol, 0) > self.long_trigger_price_dict.get(symbol, 0) > 0 \
                        and self.win_flag == 1:
                    # 触发多单追踪止盈
                    self.long_win_dict.update({symbol: 1})
                    if self.long_high_price_dict.get(symbol, 0.0) > 0.0:
                        self.trigger_long(symbol, now_enter_price)

            if self.tactics_flag == 2:
                self.dingding(f'{symbol},ws接收数据成功', symbol)
                self.wechat_qy(f'{symbol},ws接收数据成功', symbol)
            elif self.tactics_flag == 3:
                print(f'{symbol}', 'ws Receive data is ok')

    def on_ticker_short_data(self, ticker):
        symbol = ticker['symbol']
        if symbol in self.symbol_dict:
            self.last_price_dict[symbol] = float(ticker['last_price'])  # 最新的价格.
            if self.short_pos_dict.get(symbol, 0) != 0:
                if self.short_high_price_dict.get(symbol, 0.0) > 0.0:
                    self.short_high_price_dict[symbol] = max(self.short_high_price_dict.get(symbol, 0.0),
                                                             self.last_price_dict.get(symbol, 0.0))
                if self.short_low_price_dict.get(symbol, 0.0) > 0.0:
                    self.short_low_price_dict[symbol] = min(self.short_low_price_dict.get(symbol, 0.0),
                                                            self.last_price_dict.get(symbol, 0.0))
            now_enter_price = self.short_enter_price_dict.get(symbol, 0)
            if self.short_pos_dict.get(symbol, 0) < 0 < now_enter_price and self.only_msg == 0:  # 多单持仓
                if 0 < self.last_price_dict.get(symbol, 0) < self.short_win_price_dict.get(symbol, 0):
                    # 止盈处理
                    self.short_win_dict[symbol] = 0
                    self.short_enter_price_dict[symbol] = 0
                    trading_size = self.short_pos_dict.get(symbol)
                    self.short_pos_dict[symbol] = 0
                    res_sell = self.short_sell(symbol, 100, abs(trading_size), mark=True)
                    low_profit = self.short_lowProfit_dict.get(symbol, 0)
                    low_price = self.short_low_price_dict.get(symbol, 0)
                    high_price = self.short_high_price_dict.get(symbol, 0)
                    rt = (now_enter_price - self.last_price_dict.get(symbol, 0)) * abs(trading_size)
                    Profit = self.round_to(rt, 0.0001)
                    self.dingding(f"止盈平空,交易所返回:{res_sell}", symbol)
                    self.wechat_qy(f"止盈平空,交易所返回:{res_sell}", symbol)
                    HYJ_jd_first = "止盈平空:交易对:%s,最大浮亏损:%s,最大浮利润:%s,当前浮利润:%s,仓位:%s" % (
                        symbol, low_profit, self.short_maxunRealizedProfit_dict.get(symbol, 0),
                        self.short_unRealizedProfit_dict.get(symbol, 0), trading_size)
                    HYJ_jd_tradeType = "止盈"
                    HYJ_jd_curAmount = f"{now_enter_price}"
                    HYJ_jd_remark = "预计利润:%s,最新价:%s,最高价:%s,最低价:%s" % (
                        Profit, self.last_price_dict.get(symbol, 0), high_price, low_price)
                    if "code" in res_sell:
                        HYJ_jd_remark += f'{res_sell}'
                    else:
                        random_no = self.redisc.get('%s_random_no' % symbol)
                        if random_no:
                            randomno = random_no.decode("utf8")
                        else:
                            randomno = ''
                        self.log_msg_send(symbol, low_profit, low_price, Profit, high_price, now_enter_price, randomno)
                    self.short_pos_time_dict[symbol] = ''
                    self.short_high_price_dict[symbol] = 0
                    self.short_low_price_dict[symbol] = 0
                    self.short_maxunRealizedProfit_dict[symbol] = 0
                    self.short_unRealizedProfit_dict[symbol] = 0
                    self.short_lowProfit_dict[symbol] = 0
                    self.wx_send_msg(HYJ_jd_first, HYJ_jd_tradeType, HYJ_jd_curAmount, HYJ_jd_remark)

                elif 0 < self.short_loss_price_dict.get(symbol, 0) < self.last_price_dict.get(symbol, 0):
                    # 止损
                    self.short_win_dict[symbol] = 0
                    self.short_enter_price_dict[symbol] = 0
                    trading_size = self.short_pos_dict.get(symbol)
                    self.short_pos_dict[symbol] = 0
                    res_sell = self.short_sell(symbol, 100, abs(trading_size), mark=True)
                    low_profit = self.short_lowProfit_dict.get(symbol, 0)
                    low_price = self.short_low_price_dict.get(symbol, 0)
                    high_price = self.short_high_price_dict.get(symbol, 0)
                    rt = (now_enter_price - self.last_price_dict.get(symbol, 0)) * abs(trading_size)
                    Profit = self.round_to(rt, 0.0001)
                    self.dingding(f"止损平空,交易所返回:{res_sell}", symbol)
                    self.wechat_qy(f"止损平空,交易所返回:{res_sell}", symbol)
                    HYJ_jd_first = "止损平空:交易对:%s,最大浮亏:%s,最大浮利:%s,当前浮亏:%s,仓位:%s" % (
                        symbol, low_profit, self.short_maxunRealizedProfit_dict.get(symbol, 0),
                        self.short_unRealizedProfit_dict.get(symbol, 0), trading_size)
                    HYJ_jd_tradeType = "止损"
                    HYJ_jd_curAmount = f"{now_enter_price}"
                    HYJ_jd_remark = "预计亏损:%s,最新价:%s,最高价:%s,最低价:%s" % (
                        Profit, self.last_price_dict.get(symbol, 0), high_price, low_price)
                    if "code" in res_sell:
                        HYJ_jd_remark += f'{res_sell}'
                    else:
                        random_no = self.redisc.get('%s_random_no' % symbol)
                        if random_no:
                            randomno = random_no.decode("utf8")
                        else:
                            randomno = ''
                        self.log_msg_send(symbol, low_profit, low_price, Profit, high_price, now_enter_price, randomno)
                    self.short_pos_time_dict[symbol] = ''
                    self.short_high_price_dict[symbol] = 0
                    self.short_low_price_dict[symbol] = 0
                    self.short_maxunRealizedProfit_dict[symbol] = 0
                    self.short_unRealizedProfit_dict[symbol] = 0
                    self.short_lowProfit_dict[symbol] = 0
                    self.wx_send_msg(HYJ_jd_first, HYJ_jd_tradeType, HYJ_jd_curAmount, HYJ_jd_remark)

                elif self.short_win_dict.get(symbol, 0) == 1 and self.short_low_price_dict.get(symbol, 0.0) > 0.0:
                    # 追踪空单止盈处理
                    self.trigger_short(symbol, now_enter_price)
                elif 0 < self.last_price_dict.get(symbol, 0) < self.short_trigger_price_dict.get(symbol, 0) \
                        and self.win_flag == 1:
                    # 触发空单追踪止盈
                    self.short_win_dict.update({symbol: 1})
                    if self.short_high_price_dict.get(symbol, 0.0) > 0.0:
                        self.trigger_short(symbol, now_enter_price)

            if self.tactics_flag == 2:
                self.dingding(f'{symbol},ws接收数据成功', symbol)
                self.wechat_qy(f'{symbol},ws接收数据成功', symbol)
            elif self.tactics_flag == 3:
                print(f'{symbol}', 'ws Receive data is ok')
