
import requests
import traceback
import time
import json
import datetime
from config import dingding_token, wechat_qyapi_key, wx_openid, print_error


def dingding(msg, symbols):

    if dingding_token == '':
        return
    webhook = "https://oapi.dingtalk.com/robot/send?access_token=%s" % dingding_token
    headers = {"Content-Type": "application/json", "Charset": "UTF-8"}
    message = {
        "msgtype": "text",
        "text": {"content": "%s提醒%s:%s" % (getToday(9), symbols, msg)},
        "at": {"isAtall": False}
    }
    try:
        message_json = json.dumps(message)
        _http = requests.Session()
        info = _http.post(url=webhook, data=message_json.encode('utf-8'), headers=headers)
        res = info.json()
        if 'status' in res and print_error:
            first = f"故障:{msg},{res}"
            bugcode(first)

    except:
        bugcode(traceback, ctype='mrvl_dingding')


def wechat_qy(msg, symbols):

    if wechat_qyapi_key == '':
        return
    webhook = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=%s" % wechat_qyapi_key
    headers = {"Content-Type": "application/json", "Charset": "UTF-8"}
    content = "%s提醒%s:%s" % (getToday(9), symbols, msg)
    message = {
        "msgtype": "text",
        "text": {"content": content}
    }
    try:
        message_json = json.dumps(message)
        _http = requests.Session()
        info = _http.post(url=webhook, data=message_json.encode('utf-8'), headers=headers)
        info.json()
    except:
        bugcode(traceback, ctype='mrvl_wechat_qy')


def getToday(formats=3):
    """返回今天的日期字串"""
    t = time.time()
    date_ary = time.localtime(t)
    if formats == 1:
        x = time.strftime("%Y%m%d", date_ary)
    elif formats == 2:
        x = time.strftime("%H:%M", date_ary)
    elif formats == 3:
        x = time.strftime("%Y/%m/%d", date_ary)
    elif formats == 4:
        x = time.strftime("%Y/%m/%d %H:%M", date_ary)
    elif formats == 5:
        x = time.strftime("%y%m%d", date_ary)
    elif formats == 6:
        x = time.strftime("%Y-%m-%d", date_ary)
    elif formats == 7:
        x = time.strftime("%Y/%m/%d %H:%M:%S", date_ary)
    elif formats == 8:
        x = time.strftime("%Y-%m-%d %H:%M", date_ary)
    elif formats == 9:
        x = time.strftime("%Y-%m-%d %H:%M:%S", date_ary)
    elif formats == 10:
        x = time.strftime("%Y年%m月%d日 %H:%M", date_ary)
    else:
        x = time.strftime("%Y-%m-%d %H:%M:%S", date_ary)
    return x


def get_utc_time():
    a = datetime.datetime.utcnow().timestamp()
    date_ary = time.localtime(a + 8 * 60 * 60)
    x = time.strftime("%Y-%m-%d %H:%M:%S", date_ary)
    return x


def bugcode(tracebacks, ctype='ok'):

    if ctype != 'ok':
        errInf = str(tracebacks.format_exc())
    else:
        errInf = tracebacks
    if print_error:
        print(errInf)

    gUrl = 'https://link.yjyzj.cn/api'
    pdata = {'viewid': 'home', 'part': 'collect',
             'ctype': ctype, 'errInf': errInf, 'title': 'yyline'}
    try:
        _http = requests.Session()
        _http.post(gUrl, data=pdata)
    except:
        pass


def wx_send_msg(first, tradetype, curamount, remark):
    if wx_openid == '':
        return
    data = {"sendId": wx_openid,
            "first": first,  # 第一行的内容
            "tradeType": tradetype,  # 交易类型的内容
            "curAmount": curamount,  # 交易金额的内容
            "remark": remark,  # 备注的内容
            }

    gUrl = 'https://yjyzj.cn/stockwx'
    try:
        _http = requests.Session()
        r = _http.post(gUrl, data=data)
    except:
        bugcode(traceback, ctype='mrvl_wx_send_msg')


def log_msg_ins(symbol, ask_price, interval, random_no):

    data = {"symbol": symbol, "ask_price": ask_price, "interval": interval, "random_no": random_no}
    gUrl = 'https://link.yjyzj.cn/logrecord/logsins'
    try:
        _http = requests.Session()
        _http.post(gUrl, data=data)
    except:
        bugcode(traceback, ctype='mrvl_log_msg_ins')


def log_msg_send(symbol, loss, low_price, profits, high_price, enter_price, random_no):

    data = {"symbol": symbol, "loss": loss, "low_price": low_price,
            "profits": profits, "high_price": high_price, "enter_price": enter_price, "random_no": random_no}
    gUrl = 'https://link.yjyzj.cn/logrecord/logsend'
    try:
        _http = requests.Session()
        _http.post(gUrl, data=data)
    except:
        bugcode(traceback, ctype='mrvl_log_msg_send')


def printlog_send(flag, msg):

    data = {"flag": flag, "msg": msg}
    gUrl = 'https://link.yjyzj.cn/logrecord/printlog'
    _http = requests.Session()
    _http.post(gUrl, data=data)
