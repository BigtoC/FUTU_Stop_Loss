# -*- coding: utf-8 -*-

import time


def time_to_sell():
    current_time = time.localtime()
    hour = current_time[3]
    minute = current_time[4]

    if hour == 11 and minute == 59:
        return True
    if hour == 15 and minute == 59:
        return True
    else:
        return False


def time_to_sleep():
    current_time = time.localtime()
    hour = current_time[3]
    if hour == 12:
        return True
    else:
        return False

