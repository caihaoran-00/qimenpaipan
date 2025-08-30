# -*- coding: utf-8 -*-
"""
奇门遁甲核心计算模块
包含排盘算法和相关计算
"""

from typing import List, Dict, Any
from collections import deque
from .constants import Men, Shen, Star, Palace

class QiMenCalculator:
    """奇门遁甲计算器"""
    
    def __init__(self, sizhu_calculator):
        self.sizhu_calculator = sizhu_calculator
        self.sizhu = self.sizhu_calculator.get_sizhu()
        self.palaces = self._initialize_palaces()
        self.yinyang, self.ju = self.calculate_ju()
    
    def _initialize_palaces(self) -> List[Dict[str, Any]]:
        """初始化九宫格"""
        palaces = []
        for i in range(9):
            palace = {
                'number': i + 1,
                'name': Palace(i + 1),
                'tiangan': None,    # 天干（三奇六仪）
                'star': None,       # 九星
                'men': None,        # 八门
                'shen': None,       # 八神
                'dizhi': None,      # 地支
                'is_rumu': False,   # 是否入墓
                'is_jixing': False, # 是否击刑
                'is_menpo': False,  # 是否门迫
                'is_kongwang': False, # 是否空亡
                'changsheng': None, # 长生状态
                'yima': False,      # 是否驿马
                'guiren': False     # 是否贵人
            }
            palaces.append(palace)
        return palaces
    
    def calculate_ju(self) -> tuple:
        """计算局数和阴阳遁"""
        # 获取日柱干支
        ri_gan_str, ri_zhi_str = self.sizhu['日柱']
        
        # 简化的局数计算（实际应根据节气和日干支精确计算）
        ri_gan_value = [k for k, v in {1: "甲", 2: "乙", 3: "丙", 4: "丁", 5: "戊", 
                                      6: "己", 7: "庚", 8: "辛", 9: "壬", 10: "癸"}.items() 
                       if v == ri_gan_str][0]
        ri_zhi_value = [k for k, v in {1: "子", 2: "丑", 3: "寅", 4: "卯", 5: "辰", 
                                     6: "巳", 7: "午", 8: "未", 9: "申", 10: "酉", 
                                     11: "戌", 12: "亥"}.items() if v == ri_zhi_str][0]
        
        # 确定阴阳遁（简化：8月为阴遁）
        if self.sizhu_calculator.month in [11, 12, 1, 2, 3, 4, 5]:
            yinyang = "阳"
        else:
            yinyang = "阴"
        
        # 局数计算（简化）
        ju = (ri_gan_value + ri_zhi_value) % 9
        if ju == 0:
            ju = 9
            
        return yinyang, ju
    
    def pai_di_pan(self):
        """排地盘 - 三奇六仪"""
        # 确定戊的起始宫位
        start_positions = {
            1: 4, 2: 4, 3: 4,  # 一、二、三局从巽四宫开始
            4: 1, 5: 1, 6: 1,  # 四、五、六局从坎一宫开始
            7: 7, 8: 7, 9: 7   # 七、八、九局从兑七宫开始
        }
        
        start_palace = start_positions[self.ju]
        
        # 三奇六仪顺序
        from .constants import TianGan
        if self.yinyang == "阳":
            sequence = [TianGan.WU, TianGan.JI, TianGan.GENG, 
                       TianGan.XIN, TianGan.REN, TianGan.GUI,
                       TianGan.DING, TianGan.BING, TianGan.YI]
        else:
            sequence = [TianGan.WU, TianGan.BING, TianGan.DING,
                       TianGan.GUI, TianGan.REN, TianGan.XIN,
                       TianGan.GENG, TianGan.JI, TianGan.YI]
        
        # 填充地盘
        for i, tiangan in enumerate(sequence):
            palace_index = (start_palace - 1 + i) % 9
            self.palaces[palace_index]['tiangan'] = tiangan
    
    def pai_tian_pan(self):
        """排天盘 - 九星"""
        # 九星顺序
        stars_order = [
            Star.TIANPENG, Star.TIANRUI, Star.TIANCHONG,
            Star.TIANFU, Star.TIANQIN, Star.TIANXIN,
            Star.TIANZHU, Star.TIANREN, Star.TIANYING
        ]
        
        # 确定值符星（时干对应的星）
        shi_gan_str, _ = self.sizhu['时柱']
        shi_gan_value = [k for k, v in {1: "甲", 2: "乙", 3: "丙", 4: "丁", 5: "戊", 
                                       6: "己", 7: "庚", 8: "辛", 9: "壬", 10: "癸"}.items() 
                        if v == shi_gan_str][0]
        
        star_mapping = {
            5: Star.TIANPENG, 6: Star.TIANRUI, 7: Star.TIANCHONG,
            8: Star.TIANFU,   9: Star.TIANQIN, 10: Star.TIANXIN,
            4: Star.TIANZHU,  3: Star.TIANREN, 2: Star.TIANYING
        }
        
        zhi_fu_star = star_mapping.get(shi_gan_value, Star.TIANPENG)
        
        # 找到时干在地盘的位置
        zhi_fu_position = None
        for i, palace in enumerate(self.palaces):
            if palace['tiangan'] and str(palace['tiangan']) == shi_gan_str:
                zhi_fu_position = i
                break
        
        if zhi_fu_position is not None:
            # 排布九星
            star_index = stars_order.index(zhi_fu_star)
            for i in range(9):
                palace_index = (zhi_fu_position + i) % 9
                self.palaces[palace_index]['star'] = stars_order[(star_index + i) % 9]
    
    def pai_men(self):
        """排八门"""
        # 八门顺序
        men_order = [
            Men.XIU, Men.SHENG, Men.SHANG,
            Men.DU, Men.JING, Men.SI,
            Men.JING2, Men.KAI
        ]
        
        # 确定值使门（时支对应的门）
        _, shi_zhi_str = self.sizhu['时柱']
        shi_zhi_value = [k for k, v in {1: "子", 2: "丑", 3: "寅", 4: "卯", 5: "辰", 
                                      6: "巳", 7: "午", 8: "未", 9: "申", 10: "酉", 
                                      11: "戌", 12: "亥"}.items() if v == shi_zhi_str][0]
        
        men_mapping = {
            1: Men.XIU, 2: Men.SHENG, 3: Men.SHANG, 4: Men.DU,
            5: Men.JING, 6: Men.SI, 7: Men.JING2, 8: Men.KAI,
            9: Men.XIU, 10: Men.SHENG, 11: Men.SHANG, 12: Men.DU
        }
        
        zhi_shi_men = men_mapping.get(shi_zhi_value, Men.XIU)
        
        # 找到值使门的位置（简化处理）
        start_position = (self.ju - 1) % 9
        
        # 排布八门（中五宫无门）
        men_index = men_order.index(zhi_shi_men)
        men_count = 0
        for i in range(9):
            palace_index = (start_position + i) % 9
            if palace_index != 4:  # 跳过中五宫
                self.palaces[palace_index]['men'] = men_order[(men_index + men_count) % 8]
                men_count += 1
    
    def pai_shen(self):
        """排八神"""
        # 八神顺序
        if self.yinyang == "阳":
            shen_order = [
                Shen.ZHIFU, Shen.TENGHE, Shen.TAIYIN,
                Shen.LIUHE, Shen.BAIHU, Shen.XUANWU,
                Shen.JIUDI, Shen.JIUTIAN
            ]
        else:
            shen_order = [
                Shen.ZHIFU, Shen.JIUTIAN, Shen.JIUDI,
                Shen.XUANWU, Shen.BAIHU, Shen.LIUHE,
                Shen.TAIYIN, Shen.TENGHE
            ]
        
        # 找到值符星的位置
        zhi_fu_position = None
        for i, palace in enumerate(self.palaces):
            if palace['star']:
                zhi_fu_position = i
                break
        
        if zhi_fu_position is not None:
            # 排布八神（中五宫无神）
            shen_count = 0
            for i in range(9):
                palace_index = (zhi_fu_position + i) % 9
                if palace_index != 4:  # 跳过中五宫
                    self.palaces[palace_index]['shen'] = shen_order[shen_count % 8]
                    shen_count += 1
    
    def check_special_conditions(self):
        """检查特殊条件"""
        # 简化的特殊条件判断
        from .constants import TianGan, Palace
        for palace in self.palaces:
            if palace['tiangan'] in [TianGan.BING, TianGan.DING] and palace['name'] == Palace.KUN:
                palace['is_rumu'] = True
            elif palace['tiangan'] == TianGan.WU and palace['name'] == Palace.KUN:
                palace['is_rumu'] = True
    
    def calculate_changsheng(self):
        """计算十二长生状态"""
        # 十二长生状态
        CHANGSHENG_STATES = [
            "长生", "沐浴", "冠带", "临官", "帝旺", 
            "衰", "病", "死", "墓", "绝", "胎", "养"
        ]
        
        # 天干对应的长生位（在十二地支中的位置）
        from .constants import TianGan, DiZhi
        TIANGAN_CHANGSHENG = {
            TianGan.JIA: 12,  # 甲长生在亥
            TianGan.YI: 8,    # 乙长生在午
            TianGan.BING: 3,  # 丙长生在寅
            TianGan.DING: 10, # 丁长生在酉
            TianGan.WU: 3,    # 戊长生在寅
            TianGan.JI: 10,   # 己长生在酉
            TianGan.GENG: 6,  # 庚长生在巳
            TianGan.XIN: 1,   # 辛长生在子
            TianGan.REN: 9,   # 壬长生在申
            TianGan.GUI: 4    # 癸长生在卯
        }
        
        # 地支对应的位置
        DIZHI_POSITION = {
            DiZhi.ZI: 1, DiZhi.CHOU: 2, DiZhi.YIN: 3, DiZhi.MAO: 4,
            DiZhi.CHEN: 5, DiZhi.SI: 6, DiZhi.WU: 7, DiZhi.WEI: 8,
            DiZhi.SHEN: 9, DiZhi.YOU: 10, DiZhi.XU: 11, DiZhi.HAI: 12
        }
        
        # 阳干顺行，阴干逆行
        YANG_GAN = [TianGan.JIA, TianGan.BING, TianGan.WU, TianGan.GENG, TianGan.REN]
        
        # 简化的地支映射（根据宫位）
        PALACE_DIZHI = {
            0: DiZhi.ZI,  # 坎一宫 - 子
            1: DiZhi.WEI, # 坤二宫 - 未
            2: DiZhi.YIN, # 震三宫 - 寅
            3: DiZhi.CHEN, # 巽四宫 - 辰
            4: DiZhi.CHEN, # 中五宫 - 辰/戌
            5: DiZhi.WU,  # 乾六宫 - 戌
            6: DiZhi.YOU, # 兑七宫 - 酉
            7: DiZhi.CHOU, # 艮八宫 - 丑
            8: DiZhi.WU   # 离九宫 - 午
        }
        
        for i, palace in enumerate(self.palaces):
            if palace['tiangan']:
                tiangan = palace['tiangan']
                # 获取宫位对应的地支
                dizhi = PALACE_DIZHI.get(i, DiZhi.ZI)  # 默认子
                dizhi_pos = DIZHI_POSITION[dizhi]
                
                # 获取天干的长生位
                if tiangan in TIANGAN_CHANGSHENG:
                    changsheng_pos = TIANGAN_CHANGSHENG[tiangan]
                    
                    # 计算相对位置差
                    if tiangan in YANG_GAN:
                        # 阳干顺行
                        diff = (dizhi_pos - changsheng_pos) % 12
                        if diff < 0:
                            diff += 12
                    else:
                        # 阴干逆行
                        diff = (changsheng_pos - dizhi_pos) % 12
                        if diff < 0:
                            diff += 12
                    
                    # 确定长生状态
                    palace['changsheng'] = CHANGSHENG_STATES[diff]
                else:
                    palace['changsheng'] = "未知"
            else:
                palace['changsheng'] = None
    
    def calculate_yima_and_guiren(self):
        """计算驿马和贵人"""
        # 驿马计算（简化）
        # 通常根据日支来确定驿马
        rizhi_str = self.sizhu['日柱'][1]  # 日支
        
        # 驿马口诀：寅申巳亥在辰戌丑未，辰戌丑未在寅申巳亥，子午卯酉在巳申寅亥
        YIMA_MAP = {
            '寅': '申', '申': '寅', '巳': '亥', '亥': '巳',
            '辰': '戌', '戌': '辰', '丑': '未', '未': '丑',
            '子': '午', '午': '子', '卯': '酉', '酉': '卯'
        }
        
        yima = YIMA_MAP.get(rizhi_str, '未知')
        
        # 天乙贵人计算（简化）
        # 甲戊庚牛羊，乙己鼠猴乡，丙丁猪鸡位，壬癸蛇兔藏，六辛逢虎马
        rigan_str = self.sizhu['日柱'][0]  # 日干
        
        GUIREN_MAP = {
            '甲': ['丑', '未'], '戊': ['丑', '未'], '庚': ['丑', '未'],
            '乙': ['子', '申'], '己': ['子', '申'],
            '丙': ['亥', '酉'], '丁': ['亥', '酉'],
            '壬': ['巳', '卯'], '癸': ['巳', '卯'],
            '辛': ['寅', '午']
        }
        
        guiren = GUIREN_MAP.get(rigan_str, ['未知'])
        
        # 简化处理：将驿马和贵人信息添加到结果中
        self.yima = yima
        self.guiren = guiren
    
    def pai_pan(self):
        """完整排盘"""
        self.pai_di_pan()    # 排地盘
        self.pai_tian_pan()  # 排天盘
        self.pai_men()       # 排八门
        self.pai_shen()      # 排八神
        self.check_special_conditions()  # 检查特殊条件
        self.calculate_changsheng()      # 计算长生状态
        self.calculate_yima_and_guiren() # 计算驿马和贵人
    
    def get_result(self) -> Dict[str, Any]:
        """获取排盘结果"""
        return {
            'sizhu': self.sizhu,
            'ju': f"{self.yinyang}{self.ju}局",
            'palaces': [
                {
                    'name': str(palace['name']),
                    'tiangan': str(palace['tiangan']) if palace['tiangan'] else None,
                    'star': str(palace['star']) if palace['star'] else None,
                    'men': str(palace['men']) if palace['men'] else None,
                    'shen': str(palace['shen']) if palace['shen'] else None,
                    'is_rumu': palace['is_rumu'],
                    'is_jixing': palace['is_jixing'],
                    'is_menpo': palace['is_menpo'],
                    'is_kongwang': palace['is_kongwang'],
                    'changsheng': palace['changsheng'],
                    'yima': palace['yima'],
                    'guiren': palace['guiren']
                }
                for palace in self.palaces
            ],
            'yima': self.yima,
            'guiren': self.guiren
        }