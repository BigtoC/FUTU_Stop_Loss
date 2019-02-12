# -*- coding: utf-8 -*-

from futu import *
import pandas as pd
import config
import print_alert

# set format of output DataFrame
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)
pd.set_option('display.max_colwidth', 50)

stock_loss_line = 0  # 单个股票亏损上限
acc_loss_line = 0  # 整个账户亏损上限
trd_ctx = None


# 初始化，赋值
def initial(sll, al, tc):
    global stock_loss_line  # 单个股票亏损上限
    stock_loss_line = sll
    global acc_loss_line  # 整个账户亏损上限
    acc_loss_line = al
    global trd_ctx
    trd_ctx = tc


# 下单
def place_order(item):
    code = item['code']  # 股票代码
    today_pl_val = item['today_pl_val']  # 当天盈亏金额
    pl_val = item['pl_val']
    config.today_loss += pl_val
    # stock_name = item['stock_name']  # 股票名称
    can_sell_val = item['can_sell_qty']  # 可卖数量
    nominal_price = item['nominal_price']  # 当时市价
    sell_price = nominal_price

    order_trd_side = None
    order_type = None
    order_status = None
    order_id = None
    order_code = None
    order_stock_name = None
    order_qty = None
    order_price = None
    order_updated_time = None
    order_last_err_msg = None

    # print(f'item: {item}')

    if can_sell_val > 0:
        sell = trd_ctx.place_order(price=sell_price,
                                   qty=can_sell_val,
                                   code=code,
                                   trd_side=TrdSide.SELL,
                                   trd_env=TrdEnv.REAL)

        # print(f'sell: {sell}')

    #     for i, po_df in sell[1].iterrows():
    #         order_trd_side = po_df['trd_side']
    #         order_type = po_df['order_type']
    #         order_status = po_df['order_status']
    #         order_id = po_df['order_id']
    #         order_code = po_df['code']
    #         order_stock_name = po_df['stock_name']
    #         order_qty = po_df['qty']
    #         order_price = po_df['price']
    #         order_updated_time = po_df['updated_time']
    #         order_last_err_msg = po_df['last_err_msg']
    #
    #     log_write = f'股票代码：{order_code}, ' \
    #                 f'股票名称：{order_stock_name}, ' \
    #                 f'当时市价：{nominal_price}, ' \
    #                 f'每股盈亏: {pl_val/order_qty}, ' \
    #                 f'可卖数量: {can_sell_val}, ' \
    #                 f'卖出价格：{order_price}，' \
    #                 f'总共盈亏: {pl_val}, ' \
    #                 f'交易方向: {order_trd_side}, ' \
    #                 f'订单类型: {order_type}, ' \
    #                 f'订单状态: {order_status}, ' \
    #                 f'订单号码: {order_id}, ' \
    #                 f'卖出数量: {order_qty}, ' \
    #                 f'错误描述: {order_last_err_msg}, ' \
    #                 f'更新时间: {order_updated_time}'
    #
    #     with open("record.txt", "a") as fs:
    #         fs.write(log_write)
    #         fs.write('\n\n')
    #         fs.close()
    #     print(log_write)
    #     config.today_cancel_list.append(order_code)
    #
    # else:
    #     pass


# 主程序
def run_strategy():
    total_pl_val = 0
    # print(f'设定的单个股票亏损上限是：{stock_loss_line}\n')
    # print(f'设定的整个账户亏损上限是：{acc_loss_line}\n')

    position_info = trd_ctx.position_list_query(trd_env=TrdEnv.REAL)
    p2 = position_info[1].drop(['cost_price_valid', 'pl_ratio_valid', 'pl_val_valid'], axis=1)

    for idx, item in p2.iterrows():
        today_pl_val = item['today_pl_val']  # 当天盈亏金额
        total_pl_val += today_pl_val  # 计算整个账户当日的盈亏金额

    # 清仓
    if total_pl_val <= acc_loss_line or total_pl_val >= config.acc_gain_line:
        log_begin_clear = f'账户当日盈/亏{total_pl_val}，开始清仓，{time.asctime(time.localtime(time.time()))}\n'
        # with open("record.txt", "a") as fc:
        #     fc.write(log_begin_clear)
        #     fc.close()
        # print(log_begin_clear)
        sell_all(True)
    else:
        position_info = trd_ctx.position_list_query(trd_env=TrdEnv.REAL)
        p2 = position_info[1].drop(['cost_price_valid', 'pl_ratio_valid', 'pl_val_valid'], axis=1)
        for idx, item in p2.iterrows():
            pl_val = item['pl_val']  # 单个股票盈亏金额

            if pl_val <= stock_loss_line:
                place_order(item)  # 执行下单程序
            else:
                pass


def sell_all(is_lock):
    position_info = trd_ctx.position_list_query(trd_env=TrdEnv.REAL)
    p2 = position_info[1].drop(['cost_price_valid', 'pl_ratio_valid', 'pl_val_valid'], axis=1)
    for idx, item in p2.iterrows():
        place_order(item)  # 执行下单程序

    log_clear = f'开始清仓，{time.asctime(time.localtime(time.time()))}\n\n'
    with open("record.txt", "a") as fc:
        fc.write(log_clear)
        fc.close()
    print(log_clear)
    if is_lock:
        config.acc_lock_flag = True
        print('Account is locked!')
    else:
        config.acc_lock_flag = False

