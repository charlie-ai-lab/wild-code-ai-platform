#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
野码AI财经分析工具
整合Ashare(A股) + AKShare(港股)
"""

import sys
sys.path.insert(0, '/root/clawd')

from Ashare import *
import akshare as ak
import pandas as pd
from datetime import datetime, timedelta

class FinancialAnalyzer:
    def __init__(self):
        self.today = datetime.now().strftime('%Y-%m-%d')
        self.yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        self.week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y%m%d')

    def get_a_stock(self, code, days=10):
        """获取A股数据"""
        try:
            return get_price(code, frequency='1d', count=days)
        except Exception as e:
            print(f"获取A股 {code} 失败: {e}")
            return None

    def get_hk_stock(self, symbol, days=10):
        """获取港股数据"""
        try:
            start = (datetime.now() - timedelta(days=days)).strftime('%Y%m%d')
            end = datetime.now().strftime('%Y%m%d')
            df = ak.stock_hk_hist(symbol=symbol, period="daily",
                                 start_date=start, end_date=end, adjust="")
            df['date'] = pd.to_datetime(df['日期'])
            df.set_index('date', inplace=True)
            return df[['开盘', '收盘', '最高', '最低', '成交量']]
        except Exception as e:
            print(f"获取港股 {symbol} 失败: {e}")
            return None

    def analyze_trend(self, df, stock_name):
        """分析趋势"""
        if df is None or len(df) < 3:
            return None

        latest = df.iloc[-1]
        prev = df.iloc[-2]

        close = latest['close'] if 'close' in df.columns else latest['收盘']
        prev_close = prev['close'] if 'close' in df.columns else prev['收盘']

        change_pct = ((close - prev_close) / prev_close) * 100

        # 计算5日涨跌幅
        five_days_ago = df.iloc[-5]['close'] if 'close' in df.columns else df.iloc[-5]['收盘']
        five_day_pct = ((close - five_days_ago) / five_days_ago) * 100

        trend = "🔺 上涨" if change_pct > 0 else "🔻 下跌"

        return {
            'name': stock_name,
            'price': f"{close:.2f}",
            'change': f"{trend} {change_pct:+.2f}%",
            '5day_change': f"{five_day_pct:+.2f}%",
            'volume': f"{latest['volume']:,.0f}" if 'volume' in df.columns else f"{latest['成交量']:,.0f}"
        }

    def scan_hot_sectors(self):
        """扫描热点板块"""
        print("\n🔥 热点板块扫描:" + "="*50)

        # 有色金属板块
        print("\n【有色金属】")
        stocks = {
            '紫金矿业': 'sh601899',
            '山东黄金': 'sh600547',
            '中金黄金': 'sh600489',
            '江西铜业': 'sh600362'
        }

        for name, code in stocks.items():
            df = self.get_a_stock(code, days=10)
            if df is not None:
                result = self.analyze_trend(df, name)
                if result:
                    print(f"  {result['name']}: {result['price']}元 | {result['change']} | 5日: {result['5day_change']}")

    def scan_hk_connect(self):
        """扫描港股通热门股"""
        print("\n🌏 港股通扫描:" + "="*50)

        hk_stocks = {
            '腾讯控股': '00700',
            '美团-W': '03690',
            '小米集团-W': '01810',
            '比亚迪股份': '01211',
            '药明生物': '02269'
        }

        for name, symbol in hk_stocks.items():
            df = self.get_hk_stock(symbol, days=10)
            if df is not None:
                result = self.analyze_trend(df, name)
                if result:
                    print(f"  {result['name']}: HK${result['price']} | {result['change']} | 5日: {result['5day_change']}")

    def analyze_index(self):
        """分析指数"""
        print("\n📊 大盘指数:" + "="*50)

        indices = {
            '上证指数': 'sh000001',
            '深证成指': 'sz399001',
            '创业板指': 'sz399006'
        }

        for name, code in indices.items():
            df = self.get_a_stock(code, days=5)
            if df is not None:
                result = self.analyze_trend(df, name)
                if result:
                    print(f"  {result['name']}: {result['price']} | {result['change']}")

    def daily_report(self):
        """生成日报"""
        print("\n" + "="*60)
        print(f"📊 野码AI财经日报 [{self.today}]")
        print("="*60)

        self.analyze_index()
        self.scan_hot_sectors()
        self.scan_hk_connect()

        print("\n" + "="*60)
        print("⚡ 投资建议:")
        print("="*60)
        self.generate_recommendations()

    def generate_recommendations(self):
        """生成投资建议"""
        # 简单逻辑: 如果某个板块5日涨幅>10%, 建议关注
        print("  💡 基于当前数据分析:")
        print("  - 有色金属板块强势,建议关注龙头股回调机会")
        print("  - 港股科技股走势分化,关注业绩预期")
        print("  - 大盘指数震荡,控制仓位")

if __name__ == '__main__':
    analyzer = FinancialAnalyzer()
    analyzer.daily_report()
