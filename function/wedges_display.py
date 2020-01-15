# -*- coding: utf-8 -*-
"""
@author: luqi
@Created on
@instruction：
@Version update log: 用于风机点位尾流扇区展示
"""
import numpy as np
import intervals as I
import os
from matplotlib.patches import Wedge, Circle, Polygon
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt

plt.rcParams['savefig.dpi'] = 200
plt.rcParams['figure.dpi'] = 100
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


def wedgeplt(x_axis, y_axis, label, x_i, y_i, rotor, tur_id, sectors, image_property, save_path):
    """
    用于【单机位点】尾流影响扇区/测试扇区示意图绘制
    :param x_axis: 全场机位x，平面经度坐标，list/series
    :param y_axis: 全场机位y，平面经度坐标，list/series
    :param label: 全场机位编号，list/series
    :param x_i: 对应绘制扇区机位i，平面经度坐标x，float
    :param y_i: 对应绘制扇区机位i，平面经度坐标y，float
    :param rotor: 对应绘制扇区机位i的叶轮直径，list/series
    :param tur_id: 对应绘制扇区机位i的机位编号，str
    :param sectors: 风能领域0~360顺时针，正北为零，再绘图时候，需转为正东为0逆时针，转换关系[90-原角度区间]再取逆时针就是调换区间位置
    :param image_property: str, 尾流影响wake-influenced/测试自由流free-flow扇区
    :param save_path: 存储路径
    :return:
    """
    fig = plt.figure(figsize=(12, 6), tight_layout=True)
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.scatter(x_axis, y_axis, marker='^', s=20, label='Center')
    ax1.set_title('Single Turbine {} Sector(s) Display'.format(image_property), fontsize=20)

    for i in range(0, len(x_axis)):  # 标注机位编号
        ax1.text(x_axis[i], y_axis[i], label[i])

    patches = []  # 存储绘图扇区，画楔形（扇形）
    radii = 2 * rotor
    for sector in list(sectors):  # 多扇区处理
        theta1 = 90 - sector.lower  # 坐标系处理：[90-原角度区间]，再调换区间前后顺序
        theta2 = 90 - sector.upper  # 坐标系处理：[90-原角度区间]，再调换区间前后顺序
        wedge = Wedge((x_i, y_i), radii, theta2, theta1)  # 坐标系处理：[90-原角度区间]，再调换区间前后顺序
        patches.append(wedge)
    colors = 100 * np.random.rand(len(patches))
    p = PatchCollection(patches, alpha=0.4)
    p.set_array(np.array(colors))
    ax1.add_collection(p)
    ax1.legend(fontsize=10, loc='lower left')
    ax1.set_aspect('equal')
    # fig.colorbar(p, ax=ax1)

    fig.savefig(os.path.join(save_path, '{}机位{}扇区示意图.png'.format(tur_id, str(image_property))))
    # plt.show()
    plt.close("all")


def wedgeplts(x_axis, y_axis, label, patches, image_property, save_path):
    """
    用于【全场机位点】尾流影响扇区/测试扇区示意图绘制
    :param x_axis: 全场机位x，平面经度坐标，list/series
    :param y_axis: 全场机位y，平面经度坐标，list/series
    :param label: 全场机位编号，list/series
    :param patches：存储楔形wedge = Wedge((site_info['X(m)'][i], site_info['Y(m)'][i]), radii, theta2, theta1)
    :param image_property: str, 尾流影响wake-influenced/测试自由流free-flow扇区
    :param save_path: 存储路径
    :return:
    """
    fig = plt.figure(figsize=(12, 6), tight_layout=True)
    ax2 = fig.add_subplot(1, 1, 1)
    ax2.scatter(x_axis, y_axis, marker='^', s=20, label='Center')
    ax2.set_title('Windfarm Turbine Group {} Sectors Display'.format(image_property), fontsize=20)

    for i in range(0, len(x_axis)):  # 标注机位编号
        ax2.text(x_axis[i], y_axis[i], label[i])

    colors = 100 * np.random.rand(len(patches))
    p = PatchCollection(patches, alpha=0.4)
    p.set_array(np.array(colors))
    ax2.add_collection(p)
    ax2.legend(fontsize=10, loc='lower left')
    ax2.set_aspect('equal')

    fig.savefig(os.path.join(save_path, '风电场{}扇区示意图.png'.format(str(image_property))))
    # plt.show()
    plt.close("all")
