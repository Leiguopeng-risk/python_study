"""
=========================================
学习笔记：pandas数据清洗与聚合（Day 6）
日期：2026-09-28
=========================================
- 缺失值检测：df.isnull().sum()
- 缺失值删除：df.dropna(subset=['列名'])
- 缺失值填充：df['列名'].fillna(值, inplace=True)
- 去重：df.drop_duplicates(subset=['主键'], keep='first')
- 分组聚合：df.groupby('列名').agg({'目标列': '计算方式'})
"""
import pandas as pd
import numpy as np
pd.set_option('display.unicode.east_asian_width', True)  # 设置显示宽度，适应中文字符


print('---模块一:缺失值处理---')
data_missing = {
    "客户ID": ["C001", "C002", "C003", "C004", "C005"],
    "姓名": ["张三", "李四", "王五", "赵六", "孙七"],
    "年龄": [30, 22, np.nan, 45, np.nan],       # 两个缺失
    "月收入": [15000, 4800, 25000, np.nan, 12000],  # 一个缺失
    "是否违约": [False, True, False, False, True]
}

df_missing = pd.DataFrame(data_missing)
print("原始数据(含缺失值):")
print(df_missing)
#1.检测缺失值,看缺失了几个
print("\n各列缺失值数量:")
print(df_missing.isnull().sum())

#2.删除缺失值：如果‘月收入’这一列缺失，直接删除这一行（因为风控必须要有收入）
df_drop=df_missing.dropna(subset=['月收入'])
print(f"\n删除月收入缺失值后的数据(剩余{len(df_drop)}行):")
print(df_drop)

df_missing["月收入"] = df_missing["月收入"].fillna(df_missing["月收入"].mean())
#fillna()：pandas 填充缺失值函数把这一列里面所有是 NaN 的位置，替换成括号里的值（14200）只修改月收入列，其他列（年龄）的 NaN 不受影响
df_missing.fillna(df_missing.mean(numeric_only=True))




#3.填充缺失值：年龄缺失，用平均年龄填充
ayg_age = df_missing['年龄'].mean()
print(f"\n年龄缺失值的平均值为: {ayg_age:.1f}岁")
#注意：fillna 通常建议直接复赋值给原列，已保存修改
df_missing['年龄'] = df_missing['年龄'].fillna(ayg_age)
print("\n用平均年龄填充后的数据:")
print(df_missing)


print('\n---模块二:重复值处理---')
data_dup={
    "客户ID": ["C001", "C002", "C002", "C003", "C004"],
    "姓名": ["张三", "李四", "李四", "王五", "赵六"],
    "月收入": [15000, 4800, 4800, 25000, 8000]
}
df_dup=pd.DataFrame(data_dup)
print("原始数据(含重复值):")
print(df_dup)

#查找重复行
print(f"\n重复行数量: {df_dup.duplicated(subset=['客户ID']).sum()}行")

#删除重复行，保留第一次出现的(keep='first')
df_clean=df_dup.drop_duplicates(subset=['客户ID'], keep='first')
print(f'\n去重后的数据(剩余{len(df_clean)}行）:')
print(df_clean)

print('\n---模块三:分组聚合---')

data_group = {
    "客户ID": ["C001", "C002", "C003", "C004", "C005", "C006"],
    "年龄段": ["青年", "青年", "中年", "中年", "老年", "青年"],
    "月收入": [15000, 4800, 25000, 8000, 12000, 6000],
    "是否违约": [False, True, False, False, True, True]
}
df_group = pd.DataFrame(data_group)

#1.按年龄段分组，计算每个年龄段的平均月收入
avg_income_by_age=df_group.groupby('年龄段')['月收入'].mean()
print('各年龄段平均月收入：')
print(avg_income_by_age)

#2.按年龄段分组，同时计算收入和违约人数
summary=df_group.groupby('年龄段').agg({
    '月收入': 'mean',
    '是否违约': 'sum'#True算1，False算0，sum()就是违约人数
})
print(f'\n各年龄段风控汇总:')
print(summary)
#3每个年龄段的最高月收入
age_max_income=df_group.groupby('年龄段').agg({'月收入':"max"})

print(f'\n各年龄段最高月收入:{age_max_income}')