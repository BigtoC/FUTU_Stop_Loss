# -*- coding: utf-8 -*-

from futu import *
import strategy
import config
import modify_order_list
from prohibit_trade import ban, ban_all
from check_time import time_to_sell, time_to_sleep
import print_alert

stock_loss_line = config.stock_loss_line # 单个股票亏损上限
acc_loss_line = config.acc_loss_line  # 整个账户亏损上限
trade_pwd = config.unlock_pwd  # 交易密码
acc_gain_line = config.acc_gain_line  # 整个账户盈利上限


trd_ctx = OpenHKTradeContext(host="127.0.0.1", port=11111)  # 交易API

print("\n ---------- 解锁交易 ---------- ")
unlock = trd_ctx.unlock_trade(password=trade_pwd)
print(unlock)

print("\n ---------- 获取交易业务账户列表 ---------- ")
account_list = trd_ctx.get_acc_list()
print(account_list)

print("\n ---------- 获取账户资金数据 ---------- ")
account_info = trd_ctx.accinfo_query(trd_env=TrdEnv.REAL)
print(account_info)

print("\n ---------- 获取账户持仓列表 ---------- ")
# return a tuple with a '0' and a DataFrame
position_info = trd_ctx.position_list_query(trd_env=TrdEnv.REAL)
p2 = position_info[1].drop(['cost_price_valid', 'pl_ratio_valid', 'pl_val_valid'], axis=1)
print('0', p2, '\n')

print_alert.running_alert()

config.init_total_assets = account_info[1].loc[0]['total_assets']

while True:
    strategy.initial(stock_loss_line, acc_loss_line, trd_ctx)

    if config.acc_lock_flag:
        ban_all(trd_ctx)
    else:
        if time_to_sell():
            strategy.sell_all(False)
            modify_order_list.modify(trd_ctx)
            if time_to_sleep():
                time.sleep(3500)
        else:
            strategy.run_strategy()
            # ban(trd_ctx)
    modify_order_list.modify(trd_ctx)


# trd_ctx.close()


