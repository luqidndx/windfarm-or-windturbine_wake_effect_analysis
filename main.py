# -*- coding: utf-8 -*-
"""
@author: luqi
@Created on
@instruction：
@Version update log: 2020.3.26优化扇区划分颜色，及绘图展现形式
                     2020.3.27修复扇区跨越360度在intervals处理中bug，且发现最新的最新的Python-intervals已经更名为portin
"""

import intervals as I
import pandas as pd
import numpy as np
import math
import datetime
import timeit
import os
import warnings

from matplotlib.patches import Wedge
from function import tur_site_display
from function import distance
from function import angular_deflection
from function import making_directionary
from function import wedges_display

start = timeit.default_timer()

warnings.filterwarnings('ignore')
report_version_time = datetime.datetime.now().strftime('%Y%m%d-%H%M')
output_path = 'output/{}'.format(report_version_time)
making_directionary.making_dir(output_path)
site_info = pd.read_csv('input_windfarm_info/site_info.csv', header=0)

windfarm_fig = tur_site_display.turbinesite(site_info['X(m)'], site_info['Y(m)'], site_info['LABEL'],
                                            site_info['rotor diameter(m)'], output_path)

writer = pd.ExcelWriter(os.path.join(output_path, 'Detailed-analysis-results.xlsx'))
wake_patches_all = []  # 存储尾流影响扇区楔形绘图信息
free_patches_all = []  # 存储自由流扇区楔形绘图信息
for i in range(len(site_info['LABEL'])):  # 第一层主循环，循环所有风机的测试扇区
    wake_patches = []  # 存储尾流影响扇区楔形绘图信息
    free_patches = []  # 存储自由流扇区楔形绘图信息
    result = site_info[['LABEL', 'X(m)', 'Y(m)']]
    influence_sectors = I.empty()
    for j in range(len(site_info['LABEL'])):  # 第二层循环，计算i号风机与所有其他风机相关位置关系、受影响扇区，并确定i号风机测试扇区
        if j == i:  # 跳过自身
            continue
        ln = distance.distance(site_info['X(m)'][i], site_info['Y(m)'][i],
                               site_info['X(m)'][j], site_info['Y(m)'][j])
        ld = ln / site_info['rotor diameter(m)'][i]
        if ld > 20:
            influence_degree = 0
        else:
            influence_degree = 1.3 * (math.atan(2.5 * ld ** (-1) + 0.15) / math.pi * 180) + 10
        tem_azimuth = math.degrees(np.arctan2(site_info['Y(m)'][j] - site_info['Y(m)'][i],  # Y轴坐标差
                                              site_info['X(m)'][j] - site_info['X(m)'][i]))  # X轴坐标差
        # numpy.arctan2(y-cor, x-cor)，对应的坐标系为x正方向为0，逆时针到180°，顺时针到-180°,角度为i指向j的向量
        azimuth = angular_deflection.angular_deflection(tem_azimuth)  # 笛卡尔坐标系转风能坐标系

        if ((azimuth - influence_degree / 2) >= 0) & ((azimuth + influence_degree / 2) <= 360):  # 扇区没有跨360°
            influence_sector = I.open(round(azimuth - influence_degree / 2, 2),
                                      round(azimuth + influence_degree / 2, 2))
        elif ((azimuth - influence_degree / 2) < 0) & ((azimuth + influence_degree / 2) > 0):  # 左侧跨360°
            influence_sector = I.open(round(360 + (azimuth - influence_degree / 2), 2), 360) | I.open(0, round(
                azimuth + influence_degree / 2, 2))
        elif (azimuth + influence_degree / 2) > 360:  # 右侧跨360°
            influence_sector = I.open(round(azimuth - influence_degree / 2, 2), 360) | I.open(0, round(
                azimuth + influence_degree / 2 - 360, 2))
        else:
            print('有判断情况溢出！')

        result.loc[j, 'Ln'] = round(ln, 2)
        result.loc[j, 'Ln/Dn'] = round(ld, 2)
        result.loc[j, 'influence_degree'] = round(influence_degree, 2)
        result.loc[j, 'azimuth'] = round(azimuth, 2)
        result.loc[j, 'influence_sector'] = str(influence_sector)  # 转为str存入防止数据类型异常报错
        influence_sectors = influence_sectors.union(influence_sector)  # 机位影响扇区
    free_sectors = I.closed(0, 360) - influence_sectors  # 测试扇区
    result.loc[i, 'influence_sectors'] = str(influence_sectors)
    result.loc[i, 'freeflow_sectors'] = str(free_sectors)
    site_info.loc[i, 'influence_sectors'] = str(influence_sectors)  # site_info最终存入'Summary'的sheet
    site_info.loc[i, 'freeflow_sectors'] = str(free_sectors)
    radii = 2 * site_info['rotor diameter(m)'][i]
    for sector_wake in list(influence_sectors):
        theta1 = 90 - sector_wake.lower  # 调整到笛卡尔坐标系的画图方向
        theta2 = 90 - sector_wake.upper
        wedge = Wedge((site_info['X(m)'][i], site_info['Y(m)'][i]), radii, theta2, theta1)
        wake_patches_all.append(wedge)
        wake_patches.append(wedge)
    for sector_free in list(free_sectors):
        theta1 = 90 - sector_free.lower
        theta2 = 90 - sector_free.upper
        wedge = Wedge((site_info['X(m)'][i], site_info['Y(m)'][i]), radii, theta2, theta1)
        free_patches_all.append(wedge)
        free_patches.append(wedge)

    result.to_excel(writer, sheet_name='WTG{}'.format(site_info['LABEL'][i]), startrow=0, startcol=0, index=False)

    """【单机位点】尾流影响扇区/测试扇区示意图绘制"""
    wedges_display.wedgeplt(site_info['X(m)'], site_info['Y(m)'], site_info['LABEL'], site_info['X(m)'][i],
                            site_info['Y(m)'][i], site_info['rotor diameter(m)'][i], site_info['LABEL'][i],
                            wake_patches, 'wake-influenced', output_path)
    wedges_display.wedgeplt(site_info['X(m)'], site_info['Y(m)'], site_info['LABEL'], site_info['X(m)'][i],
                            site_info['Y(m)'][i], site_info['rotor diameter(m)'][i], site_info['LABEL'][i],
                            free_patches, 'free-flow', output_path)
    wedges_display.wedgeplt_overall(site_info['X(m)'], site_info['Y(m)'], site_info['LABEL'], site_info['X(m)'][i],
                                    site_info['Y(m)'][i], site_info['rotor diameter(m)'][i], site_info['LABEL'][i],
                                    wake_patches, free_patches, output_path)
site_info.to_excel(writer, sheet_name='Summary', startrow=0, startcol=0, index=False)
writer.close()

"""【全场机位点】尾流影响扇区/测试扇区示意图绘制"""
wedges_display.wedgeplts(site_info['X(m)'], site_info['Y(m)'], site_info['LABEL'], wake_patches_all, 'wake-influenced',
                         output_path)  # 输出全场尾流影响扇区情况
wedges_display.wedgeplts(site_info['X(m)'], site_info['Y(m)'], site_info['LABEL'], free_patches_all, 'free-flow',
                         output_path)  # 输出全场自由流扇区影响情况
wedges_display.wedgeplts_overall(site_info['X(m)'], site_info['Y(m)'], site_info['LABEL'], wake_patches_all,
                                 free_patches_all, output_path)  # 输出全场尾流/自由流扇区影响情况

end = timeit.default_timer()
print('Running time: %s Seconds' % (end - start))
print('Finished')
