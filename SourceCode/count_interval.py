# -*- coding: utf-8 -*-


def count(price):
    if price < 0.01:
        return price
    elif 0.01 <= price <= 0.25:
        return 0.001
    elif 0.25 < price <= 0.5:
        return 0.005
    elif 0.5 < price <= 10:
        return 0.01
    elif 10 < price <= 20:
        return 0.02
    elif 20 < price <= 100:
        return 0.05
    elif 100 < price <= 200:
        return 0.1
    elif 200 < price <= 500:
        return 0.2
    elif 500 < price <= 1000:
        return 0.5
    elif 1000 < price <= 2000:
        return 1.0
    elif 2000 < price <= 5000:
        return 2.0
    elif 5000 < price <= 9995:
        return 5


# print(count(9996))
