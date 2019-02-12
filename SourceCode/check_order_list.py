# -*- coding: utf-8 -*-

from futu import *
import config

# set format of output DataFrame
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)
pd.set_option('display.max_colwidth', 50)


def check_order_modify(trd_ctx):
    olq = trd_ctx.order_list_query(status_filter_list=['SUBMITTED'], trd_env=TrdEnv.REAL)

    order_list = olq[1]
    # print(order_list)

    modify_list = []  # Store codes that need to modify

    for idx, order in order_list.iterrows():
        if order['trd_side'] is 'SELL':
            order_item = {'code': order['code'], 'o_id': order['order_id'], 'qty': order['qty'], 'price': order['price']}
            modify_list.append(order_item)

    # print(f'There are {len(modify_list)} orders in list')

    return modify_list


def check_order_cancel(trd_ctx):
    olq = trd_ctx.order_list_query(status_filter_list=['SUBMITTED'], trd_env=TrdEnv.REAL)

    order_list = olq[1]

    buy_list = []  # Store codes that need to modify

    for idx, order in order_list.iterrows():
        if order['trd_side'] is 'BUY':
            buy_list.append(order['code'])  # 记录下状态为“买入”的订单，以供检查

    # print(f'buy_list: {buy_list}')
    return buy_list


def check_order_sell_manually(code, trd_ctx):
    pl_val = 0
    ol = trd_ctx.position_list_query(code=code, trd_env=TrdEnv.REAL)[1]
    for idx, o in ol.iterrows():
        pl_val = o['pl_val']
    # print(f'pal_val is {pl_val}')
    if pl_val < config.stock_loss_line:
        return True
    else:
        return False


# trd_ct = OpenHKTradeContext(host="127.0.0.1", port=11111)  # 交易API
# print(check_order_sell_manually('HK.00700', trd_ct))
