# -*- coding: utf-8 -*-
"""
奇门遁甲排盘系统入口文件
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from qimen_system import QiMenDunJia

if __name__ == "__main__":
    # 创建2025年8月20日17:43的奇门盘
    qimen = QiMenDunJia(2025, 8, 20, 17, 43)
    
    # 显示排盘结果
    qimen.display()