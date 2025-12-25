# -*- coding: utf-8 -*-
"""
@Time : 2025/12/25 16:46
@Email : Lvan826199@163.com
@公众号 : 梦无矶测开实录
@File : datetime_example.py
"""
__author__ = "梦无矶小仔"
# !/usr/bin/env python3
"""
日期时间工具使用示例
"""
from mwj_tools import DateTimeUtils


def datetime_examples():
    """日期时间功能演示"""

    # 1. 获取当前时间
    print("当前时间:", DateTimeUtils.now())
    print("格式化当前时间:", DateTimeUtils.now("%Y-%m-%d %H:%M:%S"))

    # 2. 时间加减
    print("\n--- 时间加减 ---")
    now = DateTimeUtils.now()
    print("当前时间:", now)
    print("一天后:", DateTimeUtils.add_time(now, days=1))
    print("一个月后:", DateTimeUtils.add_time(now, months=1))
    print("3天5小时后:", DateTimeUtils.add_time(now, days=3, hours=5))

    # 3. 时间戳转换
    print("\n--- 时间戳 ---")
    timestamp = DateTimeUtils.to_timestamp()
    print("当前时间戳:", timestamp)
    print("时间戳转时间:", DateTimeUtils.from_timestamp(timestamp))

    # 4. 时间差计算
    print("\n--- 时间差 ---")
    time1 = "2024-01-01 10:00:00"
    time2 = "2024-01-02 14:30:00"
    diff_hours = DateTimeUtils.time_difference(time1, time2, 'hours')
    print(f"时间差: {diff_hours:.2f} 小时")

    # 5. 未来日期计算
    print("\n--- 未来日期 ---")
    print("100天后是:", DateTimeUtils.future_date(100))
    print("从2024-06-01起180天后是:",
          DateTimeUtils.future_date(180, "2024-06-01"))

    # 6. 周判断
    print("\n--- 周判断 ---")
    print("今天是周末吗?", DateTimeUtils.is_weekend())
    week_start, week_end = DateTimeUtils.get_week_range()
    print(f"本周范围: {week_start} 到 {week_end}")


if __name__ == "__main__":
    datetime_examples()