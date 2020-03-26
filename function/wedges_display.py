# -*- coding: utf-8 -*-
"""
@author: luqi
@Created on
@instruction：
@Version update log: 用于风机点位尾流扇区展示
                     2020.3.26优化扇区划分颜色，及绘图展现形式
"""

import os
from matplotlib.patches import Wedge, Circle, Polygon
from matplotlib.collections import PatchCollection
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

plt.rcParams['savefig.dpi'] = 200
plt.rcParams['figure.dpi'] = 100
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签,'SimHei'黑体
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


def wedgeplt(x_axis, y_axis, label, x_i, y_i, rotor, tur_id, patches, image_property, save_path):
    """
    用于【单机位点】尾流影响扇区/测试扇区示意图绘制
    :param x_axis: 全场机位x，平面经度坐标，list/series
    :param y_axis: 全场机位y，平面经度坐标，list/series
    :param label: 全场机位编号，list/series
    :param x_i: 对应绘制扇区机位i，平面经度坐标x，float
    :param y_i: 对应绘制扇区机位i，平面经度坐标y，float
    :param rotor: 对应绘制扇区机位i的叶轮直径，list/series
    :param tur_id: 对应绘制扇区机位i的机位编号，str
    :param patches:存储楔形wedge
    :param image_property: str, 尾流影响wake-influenced/测试自由流free-flow扇区
    :param save_path: 存储路径
    :return:
    """
    fig = plt.figure(figsize=(12, 6), tight_layout=True)
    ax1 = fig.add_subplot(1, 1, 1)
    tursite = ax1.scatter(x_axis, y_axis, marker='^', s=20, label='Center')
    ax1.set_title('{} Turbine {} Sector(s) Display'.format(tur_id, image_property), fontsize=20)

    for i in range(0, len(x_axis)):  # 标注机位编号
        ax1.text(x_axis[i], y_axis[i], label[i])

    p = PatchCollection(patches, alpha=0.6)
    if image_property == 'wake-influenced':
        # p.set_color(c='orange') # Set both the edgecolor and the facecolor.
        p.set_edgecolor(c=None)
        p.set_facecolor(c='orange')
        legend_patch = mpatches.Patch(color='orange', label='wake-influenced sectors')  # 创建特殊的artists，添加到图例中
    elif image_property == 'free-flow':
        # p.set_color(c='green')
        p.set_edgecolor(c=None)
        p.set_facecolor(c='green')
        legend_patch = mpatches.Patch(color='green', label='free-flow sectors')

    ax1.add_collection(p)
    ax1.legend(handles=[tursite, legend_patch], fontsize=10, loc='lower left')
    ax1.set_aspect('equal')
    # fig.colorbar(p, ax=ax1)

    fig.savefig(os.path.join(save_path, '{}机位{}扇区示意图.png'.format(tur_id, str(image_property))))
    # plt.show()
    plt.close("all")


def wedgeplt_overall(x_axis, y_axis, label, x_i, y_i, rotor, tur_id, patches_wake, patches_freeflow, save_path):
    """
    用于【单机位点】尾流影响扇区/测试扇区示意图绘制
    :param x_axis: 全场机位x，平面经度坐标，list/series
    :param y_axis: 全场机位y，平面经度坐标，list/series
    :param label: 全场机位编号，list/series
    :param x_i: 对应绘制扇区机位i，平面经度坐标x，float
    :param y_i: 对应绘制扇区机位i，平面经度坐标y，float
    :param rotor: 对应绘制扇区机位i的叶轮直径，list/series
    :param tur_id: 对应绘制扇区机位i的机位编号，str
    :param patches_wake:存储楔形wedge
    :param patches_freeflow:存储楔形wedge
    :param save_path: 存储路径
    :return:
    """
    fig = plt.figure(figsize=(12, 6), tight_layout=True)
    ax1 = fig.add_subplot(1, 1, 1)
    tursite = ax1.scatter(x_axis, y_axis, marker='^', s=20, label='Center')
    ax1.set_title('{} Turbine Wake&Freeflow Sector(s) Display'.format(tur_id), fontsize=20)

    for i in range(0, len(x_axis)):  # 标注机位编号
        ax1.text(x_axis[i], y_axis[i], label[i])

    p_wake = PatchCollection(patches_wake, alpha=0.6)
    p_wake.set_edgecolor(c=None)
    p_wake.set_facecolor(c='orange')
    legend_patch_wake = mpatches.Patch(color='orange', label='wake-influenced sectors')
    p_freeflow = PatchCollection(patches_freeflow, alpha=0.6)
    p_freeflow.set_edgecolor(c=None)
    p_freeflow.set_facecolor(c='green')
    legend_patch_freeflow = mpatches.Patch(color='green', label='free-flow sectors')

    ax1.add_collection(p_wake)
    ax1.add_collection(p_freeflow)
    ax1.legend(handles=[tursite, legend_patch_wake, legend_patch_freeflow], fontsize=10, loc='lower left')
    ax1.set_aspect('equal')
    # fig.colorbar(p, ax=ax1)

    fig.savefig(os.path.join(save_path, '{}机位尾流&自由流扇区示意图.png'.format(tur_id)))
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
    tursite = ax2.scatter(x_axis, y_axis, marker='^', s=20, label='Center')
    ax2.set_title('Windfarm Turbine Group {} Sectors Display'.format(image_property), fontsize=20)

    for i in range(0, len(x_axis)):  # 标注机位编号
        ax2.text(x_axis[i], y_axis[i], label[i])

    p = PatchCollection(patches, alpha=0.6)
    if image_property == 'wake-influenced':
        # p.set_color(c='orange') # Set both the edgecolor and the facecolor.
        p.set_edgecolor(c=None)
        p.set_facecolor(c='orange')
        legend_patch = mpatches.Patch(color='orange', label='wake-influenced sectors')  # 创建特殊的artists，添加到图例中
    elif image_property == 'free-flow':
        # p.set_color(c='green')
        p.set_edgecolor(c=None)
        p.set_facecolor(c='green')
        legend_patch = mpatches.Patch(color='green', label='free-flow sectors')

    ax2.add_collection(p)
    ax2.legend(handles=[tursite, legend_patch], fontsize=10, loc='lower left')
    ax2.set_aspect('equal')

    fig.savefig(os.path.join(save_path, '风电场{}扇区示意图.png'.format(str(image_property))))
    # plt.show()
    plt.close("all")


def wedgeplts_overall(x_axis, y_axis, label, patches_wake, patches_freeflow, save_path):
    """
    用于【全场机位点】尾流影响扇区/测试扇区示意图绘制
    :param x_axis: 全场机位x，平面经度坐标，list/series
    :param y_axis: 全场机位y，平面经度坐标，list/series
    :param label: 全场机位编号，list/series
    :param patches_wake：存储楔形尾流wedge = Wedge((site_info['X(m)'][i], site_info['Y(m)'][i]), radii, theta2, theta1)
    :param patches_freeflow：存储楔形自由流wedge = Wedge((site_info['X(m)'][i], site_info['Y(m)'][i]), radii, theta2, theta1)
    :param save_path: 存储路径
    :return:
    """
    fig = plt.figure(figsize=(12, 6), tight_layout=True)
    ax2 = fig.add_subplot(1, 1, 1)
    tursite = ax2.scatter(x_axis, y_axis, marker='^', s=20, label='Center')
    ax2.set_title('Windfarm Turbine Group Wake&Freeflow Sectors Display', fontsize=20)

    for i in range(0, len(x_axis)):  # 标注机位编号
        ax2.text(x_axis[i], y_axis[i], label[i])

    p_wake = PatchCollection(patches_wake, alpha=0.6)
    p_wake.set_edgecolor(c=None)
    p_wake.set_facecolor(c='orange')
    legend_patch_wake = mpatches.Patch(color='orange', label='wake-influenced sectors')
    p_freeflow = PatchCollection(patches_freeflow, alpha=0.6)
    p_freeflow.set_edgecolor(c=None)
    p_freeflow.set_facecolor(c='green')
    legend_patch_freeflow = mpatches.Patch(color='green', label='free-flow sectors')

    ax2.add_collection(p_wake)
    ax2.add_collection(p_freeflow)
    ax2.legend(handles=[tursite, legend_patch_wake, legend_patch_freeflow], fontsize=10, loc='lower left')
    ax2.set_aspect('equal')

    fig.savefig(os.path.join(save_path, '风电场尾流&自由流扇区示意图.png'))
    # plt.show()
    plt.close("all")
