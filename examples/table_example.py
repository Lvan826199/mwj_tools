# -*- coding: utf-8 -*-
"""
@Time : 2025/12/25 16:46
@Email : Lvan826199@163.com
@公众号 : 梦无矶测开实录
@File : table_example.py
"""
__author__ = "梦无矶小仔"
# !/usr/bin/env python3
"""
表格工具使用示例
"""
import pandas as pd
from mwj_tools import TableUtils


def table_examples():
    """表格处理功能演示"""

    # 创建示例数据
    data = {
        '姓名': ['张三', '李四', '王五', '赵六', '钱七'],
        '年龄': [25, 30, 35, 28, 32],
        '部门': ['技术部', '市场部', '技术部', '人事部', '市场部'],
        '工资': [8000, 7000, 9000, 6000, 7500],
        '入职日期': ['2022-01-15', '2021-03-20', '2020-08-10', '2023-02-28', '2021-11-05']
    }

    df = pd.DataFrame(data)
    print("原始数据:")
    print(df)

    # 1. 数据筛选
    print("\n--- 数据筛选 ---")
    # 筛选技术部员工
    tech_dept = TableUtils.filter_data(df, {'部门': '技术部'})
    print("技术部员工:")
    print(tech_dept)

    # 筛选年龄大于30的员工
    age_gt_30 = TableUtils.filter_data(df, {'年龄': ('>', 30)})
    print("\n年龄大于30的员工:")
    print(age_gt_30)

    # 2. 数据聚合
    print("\n--- 数据聚合 ---")
    # 按部门统计平均工资和人数
    dept_stats = TableUtils.aggregate_data(
        df,
        group_by='部门',
        aggregations={'工资': 'mean', '姓名': 'count'}
    )
    print("部门统计:")
    print(dept_stats)

    # 3. 数据清洗
    print("\n--- 数据清洗 ---")
    # 假设数据中有缺失值
    df_with_na = df.copy()
    df_with_na.loc[2, '工资'] = None
    print("包含缺失值的数据:")
    print(df_with_na)

    df_cleaned = TableUtils.clean_data(df_with_na, strategy='fill', fill_value=0)
    print("\n清洗后的数据:")
    print(df_cleaned)

    # 4. 数据描述
    print("\n--- 数据描述 ---")
    stats = TableUtils.describe_data(df)
    print(f"数据形状: {stats['shape']}")
    print(f"缺失值统计: {stats['missing_values']}")

    # 5. 数据透视表
    print("\n--- 数据透视表 ---")
    # 按部门和年龄分组查看工资
    pivot_df = TableUtils.pivot_table(
        df,
        index='部门',
        columns='年龄',
        values='工资',
        aggfunc='mean'
    )
    print("工资透视表:")
    print(pivot_df)

    # 6. 文件操作示例
    print("\n--- 文件操作 ---")
    # 保存为CSV
    TableUtils.save_table(df, 'example_data.csv')
    print("数据已保存到 example_data.csv")

    # 读取CSV文件
    loaded_df = TableUtils.read_table('example_data.csv')
    print("\n从文件读取的数据:")
    print(loaded_df)


if __name__ == "__main__":
    table_examples()