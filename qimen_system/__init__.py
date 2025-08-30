# -*- coding: utf-8 -*-
"""
奇门遁甲排盘主程序
"""

import datetime
import json
from .sizhu_calculator import SiZhuCalculator
from .qimen_calculator import QiMenCalculator
from .lunar_converter import LunarConverter

class QiMenDunJia:
    """奇门遁甲排盘主类"""
    
    def __init__(self, year: int, month: int, day: int, hour: int, minute: int):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        
        # 计算四柱
        self.sizhu_calculator = SiZhuCalculator(year, month, day, hour, minute)
        self.sizhu = self.sizhu_calculator.get_sizhu()
        
        # 计算奇门遁甲
        self.qimen_calculator = QiMenCalculator(self.sizhu_calculator)
        self.qimen_calculator.pai_pan()
        
        # 获取结果
        self.result = self.qimen_calculator.get_result()
    
    def display(self):
        """显示排盘结果"""
        # 获取农历信息
        lunar_date = LunarConverter.get_lunar_date(self.year, self.month, self.day)
        dizhi_shi = LunarConverter.get_dizhi_shi(self.hour)
        
        print(f"公历: {self.year}-{self.month:02d}-{self.day:02d} {self.hour:02d}:{self.minute:02d}")
        print(f"农历: {lunar_date}")
        print(f"四柱: {self.sizhu['年柱'][0]}{self.sizhu['年柱'][1]} "
              f"{self.sizhu['月柱'][0]}{self.sizhu['月柱'][1]} "
              f"{self.sizhu['日柱'][0]}{self.sizhu['日柱'][1]} "
              f"{self.sizhu['时柱'][0]}{self.sizhu['时柱'][1]}")
        
        print(f"局数: {self.result['ju']}")
        print(f"驿马: {self.result['yima']}, 贵人: {', '.join(self.result['guiren'])}")
        
        print("\n奇门盘面 (JSON格式):")
        
        # 按九宫格顺序重新组织数据，并使用中文字段名
        ordered_result = {
            "公历": f"{self.year}-{self.month:02d}-{self.day:02d} {self.hour:02d}:{self.minute:02d}",
            "农历": lunar_date,
            "四柱": self.result["sizhu"],
            "局数": self.result["ju"],
            "驿马": self.result["yima"],
            "贵人": self.result["guiren"],
            "宫位布局": {
                # 第一行：巽四宫 离九宫 坤二宫
                "第一行": {
                    "巽四宫": {
                        "天干": self.result["palaces"][3]["tiangan"],
                        "八神": self.result["palaces"][3]["shen"],
                        "九星": self.result["palaces"][3]["star"],
                        "八门": self.result["palaces"][3]["men"],
                        "长生": self.result["palaces"][3]["changsheng"],
                        "入墓": self.result["palaces"][3]["is_rumu"],
                        "击刑": self.result["palaces"][3]["is_jixing"],
                        "门迫": self.result["palaces"][3]["is_menpo"],
                        "空亡": self.result["palaces"][3]["is_kongwang"],
                        "驿马": self.result["palaces"][3]["yima"],
                        "贵人": self.result["palaces"][3]["guiren"]
                    },
                    "离九宫": {
                        "天干": self.result["palaces"][8]["tiangan"],
                        "八神": self.result["palaces"][8]["shen"],
                        "九星": self.result["palaces"][8]["star"],
                        "八门": self.result["palaces"][8]["men"],
                        "长生": self.result["palaces"][8]["changsheng"],
                        "入墓": self.result["palaces"][8]["is_rumu"],
                        "击刑": self.result["palaces"][8]["is_jixing"],
                        "门迫": self.result["palaces"][8]["is_menpo"],
                        "空亡": self.result["palaces"][8]["is_kongwang"],
                        "驿马": self.result["palaces"][8]["yima"],
                        "贵人": self.result["palaces"][8]["guiren"]
                    },
                    "坤二宫": {
                        "天干": self.result["palaces"][1]["tiangan"],
                        "八神": self.result["palaces"][1]["shen"],
                        "九星": self.result["palaces"][1]["star"],
                        "八门": self.result["palaces"][1]["men"],
                        "长生": self.result["palaces"][1]["changsheng"],
                        "入墓": self.result["palaces"][1]["is_rumu"],
                        "击刑": self.result["palaces"][1]["is_jixing"],
                        "门迫": self.result["palaces"][1]["is_menpo"],
                        "空亡": self.result["palaces"][1]["is_kongwang"],
                        "驿马": self.result["palaces"][1]["yima"],
                        "贵人": self.result["palaces"][1]["guiren"]
                    }
                },
                # 第二行：震三宫 中五宫 兑七宫
                "第二行": {
                    "震三宫": {
                        "天干": self.result["palaces"][2]["tiangan"],
                        "八神": self.result["palaces"][2]["shen"],
                        "九星": self.result["palaces"][2]["star"],
                        "八门": self.result["palaces"][2]["men"],
                        "长生": self.result["palaces"][2]["changsheng"],
                        "入墓": self.result["palaces"][2]["is_rumu"],
                        "击刑": self.result["palaces"][2]["is_jixing"],
                        "门迫": self.result["palaces"][2]["is_menpo"],
                        "空亡": self.result["palaces"][2]["is_kongwang"],
                        "驿马": self.result["palaces"][2]["yima"],
                        "贵人": self.result["palaces"][2]["guiren"]
                    },
                    "中五宫": {
                        "天干": self.result["palaces"][4]["tiangan"],
                        "八神": self.result["palaces"][4]["shen"],
                        "九星": self.result["palaces"][4]["star"],
                        "八门": self.result["palaces"][4]["men"],
                        "长生": self.result["palaces"][4]["changsheng"],
                        "入墓": self.result["palaces"][4]["is_rumu"],
                        "击刑": self.result["palaces"][4]["is_jixing"],
                        "门迫": self.result["palaces"][4]["is_menpo"],
                        "空亡": self.result["palaces"][4]["is_kongwang"],
                        "驿马": self.result["palaces"][4]["yima"],
                        "贵人": self.result["palaces"][4]["guiren"]
                    },
                    "兑七宫": {
                        "天干": self.result["palaces"][6]["tiangan"],
                        "八神": self.result["palaces"][6]["shen"],
                        "九星": self.result["palaces"][6]["star"],
                        "八门": self.result["palaces"][6]["men"],
                        "长生": self.result["palaces"][6]["changsheng"],
                        "入墓": self.result["palaces"][6]["is_rumu"],
                        "击刑": self.result["palaces"][6]["is_jixing"],
                        "门迫": self.result["palaces"][6]["is_menpo"],
                        "空亡": self.result["palaces"][6]["is_kongwang"],
                        "驿马": self.result["palaces"][6]["yima"],
                        "贵人": self.result["palaces"][6]["guiren"]
                    }
                },
                # 第三行：艮八宫 坎一宫 乾六宫
                "第三行": {
                    "艮八宫": {
                        "天干": self.result["palaces"][7]["tiangan"],
                        "八神": self.result["palaces"][7]["shen"],
                        "九星": self.result["palaces"][7]["star"],
                        "八门": self.result["palaces"][7]["men"],
                        "长生": self.result["palaces"][7]["changsheng"],
                        "入墓": self.result["palaces"][7]["is_rumu"],
                        "击刑": self.result["palaces"][7]["is_jixing"],
                        "门迫": self.result["palaces"][7]["is_menpo"],
                        "空亡": self.result["palaces"][7]["is_kongwang"],
                        "驿马": self.result["palaces"][7]["yima"],
                        "贵人": self.result["palaces"][7]["guiren"]
                    },
                    "坎一宫": {
                        "天干": self.result["palaces"][0]["tiangan"],
                        "八神": self.result["palaces"][0]["shen"],
                        "九星": self.result["palaces"][0]["star"],
                        "八门": self.result["palaces"][0]["men"],
                        "长生": self.result["palaces"][0]["changsheng"],
                        "入墓": self.result["palaces"][0]["is_rumu"],
                        "击刑": self.result["palaces"][0]["is_jixing"],
                        "门迫": self.result["palaces"][0]["is_menpo"],
                        "空亡": self.result["palaces"][0]["is_kongwang"],
                        "驿马": self.result["palaces"][0]["yima"],
                        "贵人": self.result["palaces"][0]["guiren"]
                    },
                    "乾六宫": {
                        "天干": self.result["palaces"][5]["tiangan"],
                        "八神": self.result["palaces"][5]["shen"],
                        "九星": self.result["palaces"][5]["star"],
                        "八门": self.result["palaces"][5]["men"],
                        "长生": self.result["palaces"][5]["changsheng"],
                        "入墓": self.result["palaces"][5]["is_rumu"],
                        "击刑": self.result["palaces"][5]["is_jixing"],
                        "门迫": self.result["palaces"][5]["is_menpo"],
                        "空亡": self.result["palaces"][5]["is_kongwang"],
                        "驿马": self.result["palaces"][5]["yima"],
                        "贵人": self.result["palaces"][5]["guiren"]
                    }
                }
            }
        }
        
        print(json.dumps(ordered_result, ensure_ascii=False, indent=2))

# 使用示例
if __name__ == "__main__":
    # 创建2025年8月20日17:43的奇门盘
    qimen = QiMenDunJia(2025, 8, 20, 17, 43)
    
    # 显示排盘结果
    qimen.display()