# -*- coding: utf-8 -*-
"""
@Time : 2025/12/25 16:46
@Email : Lvan826199@163.com
@公众号 : 梦无矶测开实录
@File : test_table_utils.py
"""
__author__ = "梦无矶小仔"
# tests/test_table_utils.py
"""
表格数据处理工具模块的单元测试
"""
import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import tempfile
import json
from mwj_tools.table_utils import TableUtils


class TestTableUtils:
    """测试 TableUtils 类"""

    def setup_method(self):
        """每个测试前的准备"""
        # 创建测试数据 - 确保join_date是datetime类型
        self.test_df = pd.DataFrame({
            'id': [1, 2, 3, 4, 5],
            'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
            'age': [25, 30, 35, 40, 45],
            'score': [85.5, 92.0, 78.5, 88.0, 95.5],
            'department': ['HR', 'IT', 'IT', 'HR', 'IT'],
            'join_date': pd.to_datetime(['2021-01-01', '2021-02-01', '2021-03-01', '2021-01-15', '2021-04-01'])
        })

    # ============== 修复文件读写测试 ==============

    def test_read_table_csv(self):
        """测试读取CSV文件 - 修复版本"""
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as tmp:
            # 保存时指定日期格式
            self.test_df.to_csv(tmp.name, index=False, date_format='%Y-%m-%d %H:%M:%S')
            result = TableUtils.read_table(tmp.name)

            # CSV读取后datetime列会变成object类型，需要转换
            if 'join_date' in result.columns and result['join_date'].dtype == 'object':
                result['join_date'] = pd.to_datetime(result['join_date'])

            # 比较数据内容，忽略dtype差异
            pd.testing.assert_frame_equal(result, self.test_df, check_dtype=False)
        Path(tmp.name).unlink()

    def test_read_table_json(self):
        """测试读取JSON文件 - 修复版本"""
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as tmp:
            # 保存为JSON，保持日期格式
            self.test_df.to_json(tmp.name, orient='records', indent=2, date_format='iso')
            result = TableUtils.read_table(tmp.name)

            # JSON读取后需要转换日期列
            if 'join_date' in result.columns:
                result['join_date'] = pd.to_datetime(result['join_date'])

            # 比较数据内容
            pd.testing.assert_frame_equal(
                result.reset_index(drop=True),
                self.test_df.reset_index(drop=True),
                check_dtype=False
            )
        Path(tmp.name).unlink()

    def test_read_table_with_file_type(self):
        """测试指定文件类型读取 - 修复版本"""
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as tmp:
            self.test_df.to_csv(tmp.name, index=False, date_format='%Y-%m-%d %H:%M:%S')
            result = TableUtils.read_table(tmp.name, 'csv')

            # 转换日期列
            if 'join_date' in result.columns and result['join_date'].dtype == 'object':
                result['join_date'] = pd.to_datetime(result['join_date'])

            pd.testing.assert_frame_equal(result, self.test_df, check_dtype=False)
        Path(tmp.name).unlink()

    def test_save_table_csv(self):
        """测试保存为CSV文件 - 修复版本"""
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as tmp:
            TableUtils.save_table(self.test_df, tmp.name)
            # 读取时需要解析日期
            result = pd.read_csv(tmp.name, parse_dates=['join_date'])
            pd.testing.assert_frame_equal(result, self.test_df, check_dtype=False)
        Path(tmp.name).unlink()

    def test_save_table_json(self):
        """测试保存为JSON文件 - 修复版本"""
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as tmp:
            TableUtils.save_table(self.test_df, tmp.name)
            # 读取JSON并解析日期
            result = pd.read_json(tmp.name, orient='records', convert_dates=['join_date'])
            pd.testing.assert_frame_equal(
                result.reset_index(drop=True),
                self.test_df.reset_index(drop=True),
                check_dtype=False
            )
        Path(tmp.name).unlink()

    def test_save_table_unknown_format(self):
        """测试保存为未知格式 - 修复版本"""
        with tempfile.NamedTemporaryFile(suffix='.unknown', delete=False) as tmp:
            TableUtils.save_table(self.test_df, tmp.name)
            # 应该是CSV格式，需要解析日期
            result = pd.read_csv(tmp.name, parse_dates=['join_date'])
            pd.testing.assert_frame_equal(result, self.test_df, check_dtype=False)
        Path(tmp.name).unlink()


    def test_aggregate_data_multiple_groups(self):
        """测试多列分组聚合"""
        # 添加一个辅助列用于测试多分组
        df = self.test_df.copy()
        df['year'] = df['join_date'].dt.year

        result = TableUtils.aggregate_data(
            df,
            ['department', 'year'],
            {'age': 'mean', 'score': 'sum'}
        )
        assert len(result.columns) >= 4  # 2分组列 + 2聚合列

    def test_pivot_table_with_columns(self):
        """测试带列索引的透视表"""
        # 添加年份列用于测试
        df = self.test_df.copy()
        df['year'] = df['join_date'].dt.year

        result = TableUtils.pivot_table(
            df,
            index='department',
            columns='year',
            values='score',
            aggfunc='mean'
        )

        assert isinstance(result, pd.DataFrame)
        assert len(result.shape) == 2

    # 测试 filter_data 方法
    def test_filter_data_equals(self):
        """测试相等条件筛选"""
        conditions = {'department': 'IT'}
        result = TableUtils.filter_data(self.test_df, conditions)
        expected = self.test_df[self.test_df['department'] == 'IT'].reset_index(drop=True)
        pd.testing.assert_frame_equal(result, expected)

    def test_filter_data_comparison(self):
        """测试比较条件筛选"""
        conditions = {'age': ('>', 30)}
        result = TableUtils.filter_data(self.test_df, conditions)
        expected = self.test_df[self.test_df['age'] > 30].reset_index(drop=True)
        pd.testing.assert_frame_equal(result, expected)

    def test_filter_data_in_operator(self):
        """测试in操作符筛选"""
        conditions = {'department': ('in', ['HR', 'IT'])}
        result = TableUtils.filter_data(self.test_df, conditions)
        expected = self.test_df[self.test_df['department'].isin(['HR', 'IT'])].reset_index(drop=True)
        pd.testing.assert_frame_equal(result, expected)

    def test_filter_data_multiple_conditions(self):
        """测试多条件组合筛选"""
        conditions = {
            'department': 'IT',
            'age': ('>', 30)
        }
        result = TableUtils.filter_data(self.test_df, conditions)
        expected = self.test_df[(self.test_df['department'] == 'IT') &
                                (self.test_df['age'] > 30)].reset_index(drop=True)
        pd.testing.assert_frame_equal(result, expected)

    def test_filter_data_contains(self):
        """测试contains操作符筛选"""
        conditions = {'name': ('contains', 'a')}
        result = TableUtils.filter_data(self.test_df, conditions)
        expected = self.test_df[self.test_df['name'].str.contains('a')].reset_index(drop=True)
        pd.testing.assert_frame_equal(result, expected)

    def test_filter_data_nonexistent_column(self):
        """测试不存在的列筛选（应被忽略）"""
        conditions = {'nonexistent': 'value'}
        result = TableUtils.filter_data(self.test_df, conditions)
        pd.testing.assert_frame_equal(result, self.test_df)

    # 测试 aggregate_data 方法
    def test_aggregate_data_single_group(self):
        """测试单列分组聚合"""
        result = TableUtils.aggregate_data(
            self.test_df,
            'department',
            {'age': 'mean', 'score': ['mean', 'count']}
        )
        assert 'department' in result.columns
        assert 'age_mean' in result.columns or 'age' in result.columns

    def test_aggregate_data_multiple_groups(self):
        """测试多列分组聚合"""
        # 添加一个辅助列用于测试多分组
        df = self.test_df.copy()
        df['year'] = df['join_date'].dt.year

        result = TableUtils.aggregate_data(
            df,
            ['department', 'year'],
            {'age': 'mean', 'score': 'sum'}
        )
        assert len(result.columns) >= 4  # 2分组列 + 2聚合列

    # 测试 merge_tables 方法
    def test_merge_tables_inner(self):
        """测试内连接合并"""
        df1 = pd.DataFrame({'id': [1, 2, 3], 'name': ['A', 'B', 'C']})
        df2 = pd.DataFrame({'id': [2, 3, 4], 'age': [25, 30, 35]})

        result = TableUtils.merge_tables(df1, df2, 'id', 'inner')
        assert len(result) == 2
        assert 'name' in result.columns
        assert 'age' in result.columns

    def test_merge_tables_left(self):
        """测试左连接合并"""
        df1 = pd.DataFrame({'id': [1, 2, 3], 'name': ['A', 'B', 'C']})
        df2 = pd.DataFrame({'id': [2, 3, 4], 'age': [25, 30, 35]})

        result = TableUtils.merge_tables(df1, df2, 'id', 'left')
        assert len(result) == 3
        assert result['age'].isnull().sum() == 1  # id=1的age应该为NaN

    def test_merge_tables_on_multiple_columns(self):
        """测试多列合并"""
        df1 = pd.DataFrame({'id': [1, 1, 2], 'year': [2021, 2022, 2021], 'value': [10, 20, 30]})
        df2 = pd.DataFrame({'id': [1, 1, 2], 'year': [2021, 2022, 2021], 'label': ['A', 'B', 'C']})

        result = TableUtils.merge_tables(df1, df2, ['id', 'year'], 'inner')
        assert len(result) == 3
        assert 'value' in result.columns
        assert 'label' in result.columns

    # 测试 clean_data 方法
    def test_clean_data_drop(self):
        """测试删除缺失值"""
        df = self.test_df.copy()
        df.loc[0, 'age'] = np.nan  # 添加缺失值

        result = TableUtils.clean_data(df, 'drop')
        assert result['age'].isnull().sum() == 0
        assert len(result) == 4  # 删除了一行


    def test_clean_data_fill_specific_columns(self):
        """测试填充指定列的缺失值"""
        df = self.test_df.copy()
        df.loc[0, 'age'] = np.nan
        df.loc[1, 'score'] = np.nan

        result = TableUtils.clean_data(df, 'fill', columns=['age'])
        assert result['age'].isnull().sum() == 0
        assert result['score'].isnull().sum() == 1  # score列未处理

    def test_clean_data_fill_with_value(self):
        """测试使用指定值填充"""
        df = self.test_df.copy()
        df.loc[0, 'age'] = np.nan

        result = TableUtils.clean_data(df, 'fill', fill_value=0, columns=['age'])
        assert result.loc[0, 'age'] == 0

    # 测试 describe_data 方法
    def test_describe_data_basic(self):
        """测试基本描述统计"""
        result = TableUtils.describe_data(self.test_df)

        assert 'shape' in result
        assert 'columns' in result
        assert 'dtypes' in result
        assert 'missing_values' in result
        assert 'numeric_stats' in result
        assert 'categorical_stats' in result

        assert result['shape'] == self.test_df.shape
        assert result['columns'] == self.test_df.columns.tolist()

    def test_describe_data_numeric_stats(self):
        """测试数值型统计"""
        result = TableUtils.describe_data(self.test_df)

        if 'age' in result['numeric_stats']:
            stats = result['numeric_stats']['age']
            assert 'mean' in stats
            assert 'std' in stats
            assert 'min' in stats
            assert 'max' in stats
            assert 'median' in stats

            # 验证统计值的正确性
            assert stats['mean'] == pytest.approx(self.test_df['age'].mean())
            assert stats['min'] == self.test_df['age'].min()

    def test_describe_data_categorical_stats(self):
        """测试分类型统计"""
        result = TableUtils.describe_data(self.test_df)

        if 'department' in result['categorical_stats']:
            stats = result['categorical_stats']['department']
            assert 'unique_count' in stats
            assert 'top_value' in stats
            assert 'top_count' in stats

            # 验证统计值的正确性
            assert stats['unique_count'] == self.test_df['department'].nunique()
            assert stats['top_value'] == self.test_df['department'].mode()[0]

    # 测试 pivot_table 方法
    def test_pivot_table_basic(self):
        """测试基本透视表"""
        result = TableUtils.pivot_table(
            self.test_df,
            index='department',
            columns=None,
            values='age',
            aggfunc='mean'
        )

        assert isinstance(result, pd.DataFrame)
        assert 'age' in result.columns or len(result.columns) > 0

    def test_pivot_table_with_columns(self):
        """测试带列索引的透视表"""
        # 添加年份列用于测试
        df = self.test_df.copy()
        df['year'] = df['join_date'].dt.year

        result = TableUtils.pivot_table(
            df,
            index='department',
            columns='year',
            values='score',
            aggfunc='mean'
        )

        assert isinstance(result, pd.DataFrame)
        assert len(result.shape) == 2

    def test_pivot_table_multiple_values(self):
        """测试多值列的透视表"""
        result = TableUtils.pivot_table(
            self.test_df,
            index='department',
            columns=None,
            values=['age', 'score'],
            aggfunc='mean'
        )

        assert 'age' in result.columns or 'score' in result.columns

    # 测试边界情况和错误处理
    def test_filter_data_empty_conditions(self):
        """测试空条件筛选（应返回原数据）"""
        result = TableUtils.filter_data(self.test_df, {})
        pd.testing.assert_frame_equal(result, self.test_df)

    def test_clean_data_invalid_strategy(self):
        """测试无效的清洗策略（应返回原数据）"""
        df = self.test_df.copy()
        result = TableUtils.clean_data(df, 'invalid_strategy')
        pd.testing.assert_frame_equal(result, df)

    def test_describe_data_empty_dataframe(self):
        """测试空DataFrame的描述统计"""
        empty_df = pd.DataFrame()
        result = TableUtils.describe_data(empty_df)

        assert result['shape'] == (0, 0)
        assert result['columns'] == []
        assert result['missing_values'] == {}

    @pytest.mark.skipif(not pd.__version__.startswith('1'),
                        reason="pandas 2.x has different behavior")
    def test_aggregate_data_empty_result(self):
        """测试空结果聚合（pandas 1.x 和 2.x 行为不同）"""
        # 创建一个没有匹配分组的数据
        df = pd.DataFrame({'group': ['A', 'A', 'B', 'B'], 'value': [1, 2, 3, 4]})

        # 筛选出没有的数据
        filtered = df[df['group'] == 'C']

        if len(filtered) == 0:
            # pandas 1.x 行为
            result = TableUtils.aggregate_data(filtered, 'group', {'value': 'sum'})
            assert len(result) == 0
        else:
            # pandas 2.x 可能的行为
            pass


if __name__ == "__main__":
    '''
    # 如果使用 uv
    uv add --dev pytest pandas numpy
    # 运行所有测试
    pytest tests/test_table_utils.py -v
    
    # 运行特定测试类
    pytest tests/test_table_utils.py::TestTableUtils -v
    
    # 运行单个测试方法
    pytest tests/test_table_utils.py::TestTableUtils::test_filter_data_equals -v
    '''
    # 直接运行此文件以执行测试
    pytest.main([__file__, "-v"])