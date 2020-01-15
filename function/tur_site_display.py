# -*- coding: utf-8 -*-
"""
@author: luqi
@Created on
@instruction：
@Version update log: 用于风电场机位点展示
"""

import matplotlib.pyplot as plt
import os

plt.rcParams['savefig.dpi'] = 200
plt.rcParams['figure.dpi'] = 100
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


def turbinesite(x_axis, y_axis, label, rotor, save_path):
    """
    风电场机位、机型示意图展示
    :param x_axis: 平面经度坐标，list/series
    :param y_axis: 平面纬度坐标，list/series
    :param label: 机位编号，string
    :param rotor: 机型叶轮直径（m），list/series
    :param save_path: 保存文件夹路径
    :return: 返回一个实际无效的‘fig画布’
    """
    fig = plt.figure(figsize=(12, 6), tight_layout=True)
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.scatter(x_axis, y_axis, marker='^', s=20, label='Center')
    ax1.scatter(x_axis, y_axis, marker='o', c=rotor / max(rotor), s=rotor, alpha=0.3, label='1.0(D)')
    ax1.legend(fontsize=10, loc='lower left')
    ax1.set_title('Turbine Site Display', fontsize=20)
    ax1.set_aspect('equal')
    for i in range(0, len(x_axis)):
        ax1.text(x_axis[i], y_axis[i], label[i])
    fig.savefig(os.path.join(save_path, '风电场机位、机型示意图.png'))
    # fig.show()
    plt.close("all")

    return fig
