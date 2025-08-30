# -*- coding: utf-8 -*-
"""
四柱计算器
基于传统命理学算法计算四柱干支
"""

import datetime
from typing import Tuple
from .constants import TianGan, DiZhi, JIEQI_LIST, JIEQI_APPROX_DATES

class SolarTerm:
    """二十四节气处理"""
    
    @staticmethod
    def get_term_date(year: int, term_index: int) -> datetime.date:
        """获取指定年份的节气日期（简化版）"""
        month, day = JIEQI_APPROX_DATES[term_index]
        if year % 4 == 0 and term_index >= 2:  # 闰年调整
            day -= 1
        return datetime.date(year, month, day)
    
    @staticmethod
    def get_current_term(year: int, month: int, day: int) -> Tuple[int, str]:
        """获取当前日期所在的节气"""
        date = datetime.date(year, month, day)
        for i in range(24):
            term_date = SolarTerm.get_term_date(year, i)
            if date >= term_date:
                if i == 23 or date < SolarTerm.get_term_date(year, i + 1):
                    return i, JIEQI_LIST[i]
        return 0, JIEQI_LIST[0]

class SiZhuCalculator:
    """四柱计算器"""
    
    def __init__(self, year: int, month: int, day: int, hour: int, minute: int):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.true_hour = self._calculate_true_solar_time()
        self.nian_zhu = self._calculate_nian_zhu()
        self.yue_zhu = self._calculate_yue_zhu()
        self.ri_zhu = self._calculate_ri_zhu()
        self.shi_zhu = self._calculate_shi_zhu()
    
    def _calculate_true_solar_time(self) -> int:
        """计算真太阳时（简化版）"""
        # 真太阳时 = 平太阳时 + 时差
        # 这里简单处理：北京时间减15分钟左右
        # 但为了不影响时辰归属，我们只在边界时间进行调整
        adjusted_minute = self.minute - 15
        adjusted_hour = self.hour
        
        if adjusted_minute < 0:
            adjusted_minute += 60
            adjusted_hour -= 1
        
        if adjusted_hour < 0:
            adjusted_hour += 24
            
        # 如果调整后的时间在时辰边界上，保持原时辰
        # 例如17:00调整为16:45，仍然属于酉时
        original_shichen = (self.hour + 1) // 2
        if original_shichen == 0:
            original_shichen = 12
        adjusted_shichen = (adjusted_hour + 1) // 2
        if adjusted_shichen == 0:
            adjusted_shichen = 12
            
        # 如果时辰改变，调整回原时辰
        if original_shichen != adjusted_shichen:
            return self.hour
            
        return adjusted_hour
    
    def _calculate_nian_zhu(self) -> Tuple[TianGan, DiZhi]:
        """计算年柱"""
        # 以立春为界判断年份
        li_chun_date = SolarTerm.get_term_date(self.year, 0)
        current_date = datetime.date(self.year, self.month, self.day)
        actual_year = self.year - 1 if current_date < li_chun_date else self.year
        
        # 年干 = (年份 - 3) % 10
        year_gan_value = (actual_year - 3) % 10
        if year_gan_value == 0:
            year_gan_value = 10
        year_gan = TianGan(year_gan_value)
        
        # 年支 = (年份 - 3) % 12
        year_zhi_value = (actual_year - 3) % 12
        if year_zhi_value == 0:
            year_zhi_value = 12
        year_zhi = DiZhi(year_zhi_value)
        
        return year_gan, year_zhi
    
    def _calculate_yue_zhu(self) -> Tuple[TianGan, DiZhi]:
        """计算月柱"""
        # 获取当前节气
        term_index, term_name = SolarTerm.get_current_term(self.year, self.month, self.day)
        
        # 月支：根据节气确定
        # 寅月(立春-惊蛰)、卯月(惊蛰-清明)...丑月(小寒-立春)
        yue_zhi_value = (term_index // 2 + 3) % 12
        if yue_zhi_value == 0:
            yue_zhi_value = 12
        yue_zhi = DiZhi(yue_zhi_value)
        
        # 月干：根据年干通过"五虎遁"口诀推算
        # 甲己之年丙作首，乙庚之岁戊为头
        # 丙辛必定寻庚起，丁壬壬位顺行流
        # 若问戊癸何方发，甲寅之上好追求
        nian_gan, _ = self.nian_zhu
        
        wuhudun_rules = {
            TianGan.JIA: TianGan.BING,  # 甲→丙
            TianGan.YI: TianGan.WU,     # 乙→戊
            TianGan.BING: TianGan.GENG, # 丙→庚
            TianGan.DING: TianGan.REN,  # 丁→壬
            TianGan.WU: TianGan.JIA,    # 戊→甲
            TianGan.JI: TianGan.BING,   # 己→丙
            TianGan.GENG: TianGan.WU,   # 庚→戊
            TianGan.XIN: TianGan.GENG,  # 辛→庚
            TianGan.REN: TianGan.REN,   # 壬→壬
            TianGan.GUI: TianGan.JIA    # 癸→甲
        }
        
        start_gan = wuhudun_rules[nian_gan]
        # 从寅月开始计算距离
        yin_index = 3  # 寅的索引是3
        distance = (yue_zhi_value - yin_index) % 12
        yue_gan_value = (start_gan.value + distance - 1) % 10
        if yue_gan_value == 0:
            yue_gan_value = 10
        # 修正：应该包括起始位置
        yue_gan_value = (start_gan.value + distance) % 10
        if yue_gan_value == 0:
            yue_gan_value = 10
        yue_gan = TianGan(yue_gan_value)
        
        return yue_gan, yue_zhi
    
    def _calculate_ri_zhu(self) -> Tuple[TianGan, DiZhi]:
        """计算日柱"""
        # 仅支持1901-2100年的日柱计算
        year, month, day = self.year, self.month, self.day
        
        if not (1901 <= year <= 2100):
            raise ValueError(f"日柱计算仅支持1901-2100年，当前年份: {year}")
        
        # 1. 计算当年第几天
        # 判断是否闰年
        is_leap = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
        
        # 每月天数
        days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if is_leap:
            days_in_month[1] = 29
        
        # 计算到指定日期的天数
        days = 0
        for i in range(month - 1):
            days += days_in_month[i]
        days += day
        
        # 2. 基础计算
        year_last_two = year % 100
        
        if 1901 <= year <= 2000:
            # 1901-2000年公式
            # [(年尾二位数-1)*5 + (年尾二位数-1)/4 + 当年第几天 + 15] mod 60
            base_calc = ((year_last_two - 1) * 5 + (year_last_two - 1) // 4 + days + 15) % 60
        else:
            # 2001-2100年公式
            # [(年尾二位数-1)*5 + (年尾二位数-1)/4 + 当年第几天] mod 60
            base_calc = ((year_last_two - 1) * 5 + (year_last_two - 1) // 4 + days) % 60
        
        # 3. 对应干支
        remainder = base_calc
        if remainder == 0:
            remainder = 60
        
        # 天干：余数÷10的余数对应天干（0为癸）
        tiangan_index = remainder % 10
        if tiangan_index == 0:
            tiangan_index = 10
        
        # 地支：余数÷12的余数对应地支（0为亥）
        dizhi_index = remainder % 12
        if dizhi_index == 0:
            dizhi_index = 12
        
        ri_gan = TianGan(tiangan_index)
        ri_zhi = DiZhi(dizhi_index)
        
        return ri_gan, ri_zhi
    
    def _calculate_shi_zhu(self) -> Tuple[TianGan, DiZhi]:
        """计算时柱"""
        # 时支：根据真太阳时确定
        # 子时(23-1)、丑时(1-3)、寅时(3-5)...亥时(21-23)
        # 修正时支计算方法
        hour = self.true_hour
        
        if hour == 23 or hour == 0:
            shi_zhi_value = 1  # 子时
        elif 1 <= hour <= 2:
            shi_zhi_value = 2  # 丑时
        elif 3 <= hour <= 4:
            shi_zhi_value = 3  # 寅时
        elif 5 <= hour <= 6:
            shi_zhi_value = 4  # 卯时
        elif 7 <= hour <= 8:
            shi_zhi_value = 5  # 辰时
        elif 9 <= hour <= 10:
            shi_zhi_value = 6  # 巳时
        elif 11 <= hour <= 12:
            shi_zhi_value = 7  # 午时
        elif 13 <= hour <= 14:
            shi_zhi_value = 8  # 未时
        elif 15 <= hour <= 16:
            shi_zhi_value = 9  # 申时
        elif 17 <= hour <= 18:
            shi_zhi_value = 10  # 酉时
        elif 19 <= hour <= 20:
            shi_zhi_value = 11  # 戌时
        elif 21 <= hour <= 22:
            shi_zhi_value = 12  # 亥时
        else:
            shi_zhi_value = 1  # 默认子时
            
        shi_zhi = DiZhi(shi_zhi_value)
        
        # 时干：根据日干通过"五鼠遁"口诀推算
        # 甲己还加甲，乙庚丙作初
        # 丙辛从戊起，丁壬庚子居
        # 戊癸何方发，壬子是真途
        ri_gan, _ = self.ri_zhu
        
        wushudun_rules = {
            TianGan.JIA: TianGan.JIA,   # 甲→甲
            TianGan.YI: TianGan.BING,   # 乙→丙
            TianGan.BING: TianGan.WU,   # 丙→戊
            TianGan.DING: TianGan.GENG, # 丁→庚
            TianGan.WU: TianGan.REN,    # 戊→壬
            TianGan.JI: TianGan.JIA,    # 己→甲
            TianGan.GENG: TianGan.BING, # 庚→丙
            TianGan.XIN: TianGan.WU,    # 辛→戊
            TianGan.REN: TianGan.GENG,  # 壬→庚
            TianGan.GUI: TianGan.REN    # 癸→壬
        }
        
        start_gan = wushudun_rules[ri_gan]
        shi_gan_value = (start_gan.value + shi_zhi_value - 1) % 10
        if shi_gan_value == 0:
            shi_gan_value = 10
        shi_gan = TianGan(shi_gan_value)
        
        return shi_gan, shi_zhi
    
    def get_sizhu(self) -> dict:
        """获取四柱结果"""
        return {
            '年柱': (str(self.nian_zhu[0]), str(self.nian_zhu[1])),
            '月柱': (str(self.yue_zhu[0]), str(self.yue_zhu[1])),
            '日柱': (str(self.ri_zhu[0]), str(self.ri_zhu[1])),
            '时柱': (str(self.shi_zhu[0]), str(self.shi_zhu[1]))
        }