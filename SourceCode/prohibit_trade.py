# -*- coding: utf-8 -*-

from config import today_cancel_list
from check_order_list import check_order_cancel
from futu import *
import config

# trd_ctx = OpenHKTradeContext(host="127.0.0.1", port=11111)  # 交易API


def ban(trd_ctx):
    buy_list = check_order_cancel(trd_ctx)
    # print(f'buy_list: {buy_list}')
    for code in buy_list:
        if code in today_cancel_list:
            # print(f'code is: {code}')
            ban_stock_list = trd_ctx.order_list_query(code=code, trd_env=TrdEnv.REAL)[1]
            for idx, b in ban_stock_list.iterrows():
                if b['trd_side'] is 'BUY' and b['order_status'] is 'SUBMITTED':
                    ban_stock = b
                    # print(ban_stock)
                    ban_id = ban_stock['order_id']
                    # print(ban_id)
                    trd_ctx.modify_order(ModifyOrderOp.CANCEL, ban_id, 0, 0, trd_env=TrdEnv.REAL)


def ban_all(trd_ctx):
    ban_stock_list = trd_ctx.order_list_query(trd_env=TrdEnv.REAL)[1]
    for idx, b in ban_stock_list.iterrows():
        if b['trd_side'] is 'BUY' and b['order_status'] is 'SUBMITTED':
            ban_stock = b
            # print(ban_stock)
            ban_id = ban_stock['order_id']
            trd_ctx.modify_order(ModifyOrderOp.CANCEL, ban_id, 0, 0, trd_env=TrdEnv.REAL)

# ban(trd_ctx)

