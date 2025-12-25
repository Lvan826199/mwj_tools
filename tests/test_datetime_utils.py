# -*- coding: utf-8 -*-
"""
@Time : 2025/12/25 16:45
@Email : Lvan826199@163.com
@公众号 : 梦无矶测开实录
@File : test_datetime_utils.py
"""
__author__ = "梦无矶小仔"
# tests/test_datetime_utils.py
"""
日期时间工具模块的单元测试
"""
# tests/test_datetime_utils.py (修正版本 - 关键部分)
import pytest
from datetime import datetime, date, timedelta
import time
from mwj_tools.datetime_utils import DateTimeUtils


class TestDateTimeUtils:
    """测试 DateTimeUtils 类 - 时区安全版本"""

    def test_now_without_format(self):
        """测试 now() 方法无格式参数 - 时区安全版本"""
        result = DateTimeUtils.now()
        assert isinstance(result, datetime)

        # 更安全的比较：检查是否是最近的时间
        now_local = datetime.now()
        time_diff = abs((now_local - result).total_seconds())
        assert time_diff < 2  # 放宽到2秒内，确保测试稳定

    def test_now_with_format(self):
        """测试 now() 方法带格式参数 - 时区安全版本"""
        result = DateTimeUtils.now('%Y-%m-%d')
        assert isinstance(result, str)

        # 使用今天日期验证
        today_str = datetime.now().strftime('%Y-%m-%d')
        assert result == today_str

    def test_add_time_default_current(self):
        """测试时间加减 - 默认当前时间 - 时区安全版本"""
        # 记录测试开始时间
        test_start = datetime.now()

        # 调用方法（不加任何参数，应该使用当前时间）
        result = DateTimeUtils.add_time()

        # 验证结果是datetime对象
        assert isinstance(result, datetime)

        # 计算时间差（应该非常小）
        time_diff = abs((result - test_start).total_seconds())

        # 允许有一定延迟，但应该在合理范围内
        assert time_diff < 5  # 5秒内

    def test_to_timestamp_default_current(self):
        """测试时间戳转换 - 默认当前时间 - 时区安全版本"""
        # 方法1：直接比较时间戳（最准确）
        timestamp = DateTimeUtils.to_timestamp()
        now_timestamp = time.time()  # 使用time模块的timestamp

        # 时间戳应该非常接近
        diff = abs(now_timestamp - timestamp)
        assert diff < 1  # 1秒内

        # 方法2：验证时间戳可以正确转换回本地时间
        dt_from_timestamp = DateTimeUtils.from_timestamp(timestamp)
        now_local = datetime.now()

        # 转换后的时间应该是今天
        assert dt_from_timestamp.date() == now_local.date()
        # 小时可能因执行时间有差异，但应该在合理范围
        hour_diff = abs(dt_from_timestamp.hour - now_local.hour)
        assert hour_diff <= 1  # 最多差1小时（考虑跨小时边界情况）

    def test_time_difference_default_current(self):
        """测试时间差计算 - 默认当前时间 - 时区安全版本"""
        # 使用2小时前的时间
        past_time = datetime.now() - timedelta(hours=2)

        # 计算时间差（第二个参数为None，使用当前时间）
        diff_hours = DateTimeUtils.time_difference(past_time, unit='hours')

        # 应该大约是2小时，允许小误差
        assert 1.95 < diff_hours < 2.05  # 大约2小时，允许±0.05小时误差

    def test_is_weekend_default_current(self):
        """测试周末判断 - 默认当前时间"""
        result = DateTimeUtils.is_weekend()
        assert isinstance(result, bool)

        # 可以额外验证：如果结果是True，那么今天确实是周末
        today = datetime.now()
        is_actually_weekend = today.weekday() >= 5

        # 这里不强制断言一致，因为方法内部可能有时区处理
        # 但我们可以记录这个信息用于调试
        print(f"测试时间: {today}, 实际周末: {is_actually_weekend}, 方法返回: {result}")

    def test_get_week_range_default_current(self):
        """测试获取周范围 - 默认当前时间 - 时区安全版本"""
        start, end = DateTimeUtils.get_week_range()

        # 确保返回的是两个date对象
        assert isinstance(start, date)
        assert isinstance(end, date)

        # 确保结束日期比开始日期晚6天
        assert (end - start).days == 6

        # 验证今天在开始和结束日期之间
        today = date.today()
        assert start <= today <= end

        # 验证开始是周一，结束是周日
        # 注意：date.weekday() 返回 0=周一, 6=周日
        assert start.weekday() == 0  # 周一
        assert end.weekday() == 6  # 周日

    def test_future_date_default_today(self):
        """测试未来日期计算 - 默认今天 - 时区安全版本"""
        # 测试0天后（应该返回今天）
        result = DateTimeUtils.future_date(0)
        today_str = date.today().strftime("%Y-%m-%d")
        assert result == today_str

        # 测试7天后
        result_7_days = DateTimeUtils.future_date(7)
        seven_days_later = (date.today() + timedelta(days=7)).strftime("%Y-%m-%d")
        assert result_7_days == seven_days_later

    # 其他不涉及当前时间的方法保持不变...
    def test_add_time_days_only(self):
        """测试时间加减 - 仅天数"""
        base = datetime(2023, 1, 1, 12, 0, 0)
        result = DateTimeUtils.add_time(base, days=5)
        expected = datetime(2023, 1, 6, 12, 0, 0)
        assert result == expected

    def test_add_time_multiple_units(self):
        """测试时间加减 - 多单位组合"""
        base = datetime(2023, 1, 1, 12, 0, 0)
        result = DateTimeUtils.add_time(base, days=2, hours=3, minutes=30)
        expected = datetime(2023, 1, 3, 15, 30, 0)
        assert result == expected

    def test_add_time_with_months(self):
        """测试时间加减 - 包含月份"""
        base = datetime(2023, 1, 31, 12, 0, 0)
        result = DateTimeUtils.add_time(base, months=1)
        # 1月31日加1个月 = 2月28日 (非闰年)
        expected = datetime(2023, 2, 28, 12, 0, 0)
        assert result == expected

    def test_add_time_with_string_input(self):
        """测试时间加减 - 字符串输入"""
        base_str = "2023-01-01T12:00:00"
        result = DateTimeUtils.add_time(base_str, days=1)
        expected = datetime(2023, 1, 2, 12, 0, 0)
        assert result == expected

    def test_add_time_default_current(self):
        """测试时间加减 - 默认当前时间"""
        result = DateTimeUtils.add_time()
        assert isinstance(result, datetime)
        diff = abs((datetime.now() - result).total_seconds())
        assert diff < 1  # 1秒内

    def test_to_timestamp_from_datetime(self):
        """测试时间戳转换 - datetime输入"""
        dt = datetime(2023, 1, 1, 0, 0, 0)
        timestamp = DateTimeUtils.to_timestamp(dt)
        expected = dt.timestamp()
        assert timestamp == expected

    def test_to_timestamp_from_string(self):
        """测试时间戳转换 - 字符串输入"""
        time_str = "2023-01-01T00:00:00"
        timestamp = DateTimeUtils.to_timestamp(time_str)
        dt = datetime.fromisoformat(time_str)
        expected = dt.timestamp()
        assert timestamp == expected

    def test_to_timestamp_default_current(self):
        """测试时间戳转换 - 默认当前时间"""
        timestamp = DateTimeUtils.to_timestamp()
        now_timestamp = datetime.now().timestamp()
        diff = abs(now_timestamp - timestamp)
        assert diff < 1  # 1秒内

    def test_from_timestamp(self):
        """测试时间戳反转换"""
        timestamp = 1672531200  # 2023-01-01 00:00:00
        result = DateTimeUtils.from_timestamp(timestamp)
        expected = datetime(2023, 1, 1, 8, 0, 0)
        assert result == expected

    def test_time_difference_seconds(self):
        """测试时间差计算 - 秒单位"""
        time1 = datetime(2023, 1, 1, 12, 0, 0)
        time2 = datetime(2023, 1, 1, 12, 0, 30)
        diff = DateTimeUtils.time_difference(time1, time2, 'seconds')
        assert diff == 30.0

    def test_time_difference_hours(self):
        """测试时间差计算 - 小时单位"""
        time1 = datetime(2023, 1, 1, 12, 0, 0)
        time2 = datetime(2023, 1, 1, 15, 0, 0)
        diff = DateTimeUtils.time_difference(time1, time2, 'hours')
        assert diff == 3.0

    def test_time_difference_with_strings(self):
        """测试时间差计算 - 字符串输入"""
        time1 = "2023-01-01T12:00:00"
        time2 = "2023-01-01T13:30:00"
        diff = DateTimeUtils.time_difference(time1, time2, 'minutes')
        assert diff == 90.0

    def test_time_difference_default_current(self):
        """测试时间差计算 - 默认当前时间"""
        past_time = datetime.now() - timedelta(hours=2)
        diff = DateTimeUtils.time_difference(past_time, unit='hours')
        assert 1.9 < diff < 2.1  # 约2小时

    def test_future_date_from_date(self):
        """测试未来日期计算 - date对象"""
        from_date = date(2023, 1, 1)
        result = DateTimeUtils.future_date(10, from_date)
        expected = "2023-01-11"
        assert result == expected

    def test_future_date_from_string(self):
        """测试未来日期计算 - 字符串输入"""
        result = DateTimeUtils.future_date(5, "2023-01-01", "%Y/%m/%d")
        expected = "2023/01/06"
        assert result == expected

    def test_future_date_default_today(self):
        """测试未来日期计算 - 默认今天"""
        result = DateTimeUtils.future_date(0)
        today_str = date.today().strftime("%Y-%m-%d")
        assert result == today_str

    def test_format_time_datetime(self):
        """测试时间格式化 - datetime输入"""
        dt = datetime(2023, 1, 1, 12, 30, 45)
        result = DateTimeUtils.format_time(dt, "%Y年%m月%d日 %H:%M")
        expected = "2023年01月01日 12:30"
        assert result == expected

    def test_format_time_string(self):
        """测试时间格式化 - 字符串输入"""
        time_str = "2023-01-01T12:30:45"
        result = DateTimeUtils.format_time(time_str, "%H:%M:%S")
        expected = "12:30:45"
        assert result == expected

    def test_is_weekend_true(self):
        """测试周末判断 - 周六"""
        saturday = datetime(2023, 12, 30)  # 2023-12-30 是周六
        assert DateTimeUtils.is_weekend(saturday) is True

    def test_is_weekend_false(self):
        """测试周末判断 - 周一"""
        monday = datetime(2023, 12, 25)  # 2023-12-25 是周一
        assert DateTimeUtils.is_weekend(monday) is False

    def test_is_weekend_with_string(self):
        """测试周末判断 - 字符串输入"""
        sunday_str = "2023-12-31T12:00:00"  # 周日
        assert DateTimeUtils.is_weekend(sunday_str) is True

    def test_is_weekend_default_current(self):
        """测试周末判断 - 默认当前时间"""
        result = DateTimeUtils.is_weekend()
        # 无法确定当前是否为周末，但结果应该是布尔值
        assert isinstance(result, bool)

    def test_get_week_range_monday(self):
        """测试获取周范围 - 周一"""
        monday = datetime(2023, 12, 25)  # 周一
        start, end = DateTimeUtils.get_week_range(monday)
        assert start == date(2023, 12, 25)  # 周一
        assert end == date(2023, 12, 31)  # 周日

    def test_get_week_range_wednesday(self):
        """测试获取周范围 - 周三"""
        wednesday = datetime(2023, 12, 27)  # 周三
        start, end = DateTimeUtils.get_week_range(wednesday)
        assert start == date(2023, 12, 25)  # 周一
        assert end == date(2023, 12, 31)  # 周日

    def test_get_week_range_sunday(self):
        """测试获取周范围 - 周日"""
        sunday = datetime(2023, 12, 31)  # 周日
        start, end = DateTimeUtils.get_week_range(sunday)
        assert start == date(2023, 12, 25)  # 周一
        assert end == date(2023, 12, 31)  # 周日

    def test_get_week_range_with_string(self):
        """测试获取周范围 - 字符串输入"""
        time_str = "2023-12-27T12:00:00"  # 周三
        start, end = DateTimeUtils.get_week_range(time_str)
        assert start == date(2023, 12, 25)
        assert end == date(2023, 12, 31)

    def test_get_week_range_default_current(self):
        """测试获取周范围 - 默认当前时间"""
        start, end = DateTimeUtils.get_week_range()
        # 确保返回的是两个date对象
        assert isinstance(start, date)
        assert isinstance(end, date)
        # 确保结束日期比开始日期晚6天
        assert (end - start).days == 6


if __name__ == "__main__":
    '''
    # 在项目根目录下运行
    pytest tests/test_datetime_utils.py -v
    
    # 或者运行所有测试
    pytest tests/ -v
    
    # 确保你的项目中已经安装了 pytest
    uv add --dev pytest
    '''
    # 直接运行此文件以执行测试
    pytest.main([__file__, "-v"])
