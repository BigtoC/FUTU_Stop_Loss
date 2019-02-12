# -*- coding: utf-8 -*-

import json
import codecs

with open('config.txt', 'r', encoding='utf-8-sig') as f:
    content = json.load(f)

# 单个股票亏损上限
ssl = content["单个股票亏损上限"]
stock_loss_line = ssl - ssl * 2

# 整个账户亏损上限
acll = content["整个账户亏损上限"]
acc_loss_line = acll - acll * 2

# 交易密码
unlock_pwd = content["交易密码"]

# 整个账户盈利上限
acc_gain_line = content["整个账户盈利上限"]

# 记录账户总亏损
today_loss = 0

today_cancel_list = []

acc_lock_flag = False

init_total_assets = 0



