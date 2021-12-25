# -*- coding: utf-8 -*-
##############################################################################
# Author：QQ173782910
##############################################################################
import redis
import json
import pytz
# 注意：
#    持仓方向为单向,不会设置杠杆
#    下边的dingding_token,wx_openid为空的话是不会发送钉钉消息和公众号消息

version_flag = '20211225'

with open(r'must_edit_config.json', encoding='utf-8') as edit_file:
    edit_config_dict = json.load(edit_file)
edit_config = edit_config_dict

with open(r'config.json', encoding='utf-8') as config_file:
    config_dict = json.load(config_file)
config_raw = config_dict

meta_version = config_dict['trade']['meta_version']
meta_path = rf'metas/{meta_version}'
print(f'meta_version: {meta_version}')

with open(rf'{meta_path}/symbol_metas.json', encoding='utf-8') as symbol_metas_file:
    symbol_metas_dict = json.load(symbol_metas_file)
    config_dict['trade']['strategy']['symbol_metas'] = symbol_metas_dict

timezone = pytz.timezone(config_dict['system']['timezone'])
print_error = config_dict['system']['print_error']

key = edit_config['api_key']  # 币安API的key
secret = edit_config['api_secret']  # 币安API的secret

dingding_token = edit_config['ding_talk_token']  # 钉钉webhook的access_token
wechat_qyapi_key = edit_config['wechat_qyapi_key']  # 企业微信webhook的key
wx_openid = edit_config['wechat_open_id']  # 关注简道斋后发送openid得到的那一串字符就是这个
position_side = edit_config['PositionSide']  # 允许机器人下单的方向,0多空,1仅多,2仅空

trade_size_factor = config_dict['trade']['trade_size_factor']
tactics_flag = config_dict['trade']['tactics_flag']  # 机器人消息参数，1为钉钉确认策略计算是否正常，2为钉钉确认ws接收数据是否正常，
# 机器人消息参数  3为打印确认ws接收数据是否正常,4为打印确认策略计算是否正常。

leverage = edit_config['leverage']  # 下单杠杆
only_msg = config_dict['trade']['only_msg']  # 可修改是否仅发微信提醒
win_flag = config_dict['trade']['win_flag']  # 可修改是否开启追踪止盈

redis_config = config_dict['system']['redis']
redis_pool = redis.ConnectionPool(host=redis_config['host'], port=redis_config['port'],
                                  db=redis_config['db_index'], password=redis_config['password'])
redisc = redis.StrictRedis(connection_pool=redis_pool)


def get_symbol_metas(group_name: str = 'customized'):
    if group_name is None:
        group_name = 'customized'
    if group_name != "customized":
        raise Exception(f'group_name not is customized')
    _strategy_config = config_dict['trade']['strategy']
    _symbol_metas = _strategy_config['symbol_metas']
    _symbols = _strategy_config['select_symbol_groups'][group_name]

    return {symbol: meta for symbol, meta in _symbol_metas.items() if symbol in _symbols}
