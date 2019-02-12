# -*- coding: utf-8 -*-

import check_order_list as c
import count_interval
from futu import *
import config
import time

stock_loss_line = config.stock_loss_line - config.stock_loss_line * 2


def modify(trd_ctx):
    # print('start checking')
    modify_list = c.check_order_modify(trd_ctx)
    if len(modify_list) == 0:  # if == 0, order list is empty now
        # print('pass')
        pass
    else:
        # print(modify_list)
        for m in modify_list:
            code = m['code']
            qty = m['qty']
            if code in config.today_cancel_list \
                    or c.check_order_sell_manually(code, trd_ctx):

                o_id = m['o_id']
                qty = m['qty']
                list_price = m['price']
                sell_price = list_price - count_interval.count(list_price)
                # print(f'sell_price is: {sell_price}')
                modify_result = trd_ctx.modify_order(ModifyOrderOp.NORMAL,
                                                     order_id=o_id,
                                                     qty=qty,
                                                     price=sell_price,
                                                     trd_env=TrdEnv.REAL)
                # print(modify_result)
                time.sleep(1)
            else:
                pass

