# -*- coding: utf-8 -*-
"""
@author: luqi
@Created on
@instruction：
"""


def angular_deflection(degree):
    """
    本函数用于处理计算中numpy.arctan2(y-cor, x-cor)函数对应坐标系以x轴正方向为0°的偏转，统一到风能领域正北为0°
    :param degree:
    :return:
    """
    if degree <= 0:
        return -degree + 90
    elif degree <= 90:
        return 90 - degree
    else:
        return 360 - (degree - 90)
