# -*- coding: utf-8 -*-
"""
@author: luqi
@Created on
@instruction：
@Version update log: 创建文件夹
"""
import os


def making_dir(folder_path):
    """
    创建未存在的文件夹
    :param folder_path:
    :return:
    """
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
