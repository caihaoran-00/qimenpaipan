# -*- coding: utf-8 -*-
"""
农历转换模块
使用zhdate库进行公历转农历转换
"""

import datetime
from zhdate import ZhDate

class LunarConverter:
    """农历转换器"""
    
    # 天干
    TIAN_GAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    
    # 地支
    DI_ZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    
    # 生肖
    ZODIAC = ["鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]
    
    # 时辰对应的地支
    SHI_CHEN = {
        23: "子", 0: "子", 1: "丑", 2: "丑", 3: "寅", 4: "寅",
        5: "卯", 6: "卯", 7: "辰", 8: "辰", 9: "巳", 10: "巳",
        11: "午", 12: "午", 13: "未", 14: "未", 15: "申", 16: "申",
        17: "酉", 18: "酉", 19: "戌", 20: "戌", 21: "亥", 22: "亥"
    }
    
    @staticmethod
    def get_lunar_date(year: int, month: int, day: int) -> str:
        """获取农历日期"""
        # 使用zhdate库进行转换
        lunar_date = ZhDate.from_datetime(datetime.datetime(year, month, day))
        return f"{lunar_date.chinese()}"
    
    @staticmethod
    def get_lunar_year(year: int) -> str:
        """获取农历年份"""
        gan_index = (year - 4) % 10
        zhi_index = (year - 4) % 12
        zodiac = LunarConverter.ZODIAC[zhi_index]
        return f"{LunarConverter.TIAN_GAN[gan_index]}{LunarConverter.DI_ZHI[zhi_index]}年({zodiac}年)"
    
    @staticmethod
    def get_dizhi_shi(hour: int) -> str:
        """获取地支时"""
        return LunarConverter.SHI_CHEN.get(hour, "未知时")