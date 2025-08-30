# -*- coding: utf-8 -*-
"""
奇门遁甲常量定义
包含枚举类型和常量数据
"""

from enum import Enum

class TianGan(Enum):
    """天干枚举"""
    JIA = 1   # 甲
    YI = 2    # 乙
    BING = 3  # 丙
    DING = 4  # 丁
    WU = 5    # 戊
    JI = 6    # 己
    GENG = 7  # 庚
    XIN = 8   # 辛
    REN = 9   # 壬
    GUI = 10  # 癸
    
    def __str__(self):
        names = {1: "甲", 2: "乙", 3: "丙", 4: "丁", 5: "戊", 
                6: "己", 7: "庚", 8: "辛", 9: "壬", 10: "癸"}
        return names[self.value]

class DiZhi(Enum):
    """地支枚举"""
    ZI = 1    # 子
    CHOU = 2  # 丑
    YIN = 3   # 寅
    MAO = 4   # 卯
    CHEN = 5  # 辰
    SI = 6    # 巳
    WU = 7    # 午
    WEI = 8   # 未
    SHEN = 9  # 申
    YOU = 10  # 酉
    XU = 11   # 戌
    HAI = 12  # 亥
    
    def __str__(self):
        names = {1: "子", 2: "丑", 3: "寅", 4: "卯", 5: "辰", 
                6: "巳", 7: "午", 8: "未", 9: "申", 10: "酉", 
                11: "戌", 12: "亥"}
        return names[self.value]

class Men(Enum):
    """八门枚举"""
    XIU = 1   # 休门
    SHENG = 2 # 生门
    SHANG = 3 # 伤门
    DU = 4    # 杜门
    JING = 5  # 景门
    SI = 6    # 死门
    JING2 = 7 # 惊门
    KAI = 8   # 开门
    
    def __str__(self):
        names = {1: "休门", 2: "生门", 3: "伤门", 4: "杜门", 
                5: "景门", 6: "死门", 7: "惊门", 8: "开门"}
        return names[self.value]

class Shen(Enum):
    """八神枚举"""
    ZHIFU = 1     # 值符
    TENGHE = 2    # 螣蛇
    TAIYIN = 3    # 太阴
    LIUHE = 4     # 六合
    BAIHU = 5     # 白虎
    XUANWU = 6    # 玄武
    JIUTIAN = 7   # 九天
    JIUDI = 8     # 九地
    
    def __str__(self):
        names = {1: "值符", 2: "螣蛇", 3: "太阴", 4: "六合", 
                5: "白虎", 6: "玄武", 7: "九天", 8: "九地"}
        return names[self.value]

class Star(Enum):
    """九星枚举"""
    TIANPENG = 1   # 天蓬
    TIANRUI = 2    # 天芮
    TIANCHONG = 3  # 天冲
    TIANFU = 4     # 天辅
    TIANQIN = 5    # 天禽
    TIANXIN = 6    # 天心
    TIANZHU = 7    # 天柱
    TIANREN = 8    # 天任
    TIANYING = 9   # 天英
    
    def __str__(self):
        names = {1: "天蓬", 2: "天芮", 3: "天冲", 4: "天辅", 
                5: "天禽", 6: "天心", 7: "天柱", 8: "天任", 9: "天英"}
        return names[self.value]

class Palace(Enum):
    """九宫枚举"""
    KAN = 1    # 坎一宫
    KUN = 2    # 坤二宫
    ZHEN = 3   # 震三宫
    XUN = 4    # 巽四宫
    ZHONG = 5  # 中五宫
    QIAN = 6   # 乾六宫
    DUI = 7    # 兑七宫
    GEN = 8    # 艮八宫
    LI = 9     # 离九宫
    
    def __str__(self):
        names = {1: "坎一宫", 2: "坤二宫", 3: "震三宫", 4: "巽四宫", 
                5: "中五宫", 6: "乾六宫", 7: "兑七宫", 8: "艮八宫", 9: "离九宫"}
        return names[self.value]

# 节气数据
JIEQI_LIST = [
    "立春", "雨水", "惊蛰", "春分", "清明", "谷雨",
    "立夏", "小满", "芒种", "夏至", "小暑", "大暑", 
    "立秋", "处暑", "白露", "秋分", "寒露", "霜降",
    "立冬", "小雪", "大雪", "冬至", "小寒", "大寒"
]

JIEQI_APPROX_DATES = [
    (2, 4), (2, 19), (3, 5), (3, 20), (4, 5), (4, 20),
    (5, 5), (5, 21), (6, 6), (6, 21), (7, 7), (7, 23),
    (8, 8), (8, 23), (9, 8), (9, 23), (10, 8), (10, 23),
    (11, 7), (11, 22), (12, 7), (12, 22), (1, 6), (1, 20)
]