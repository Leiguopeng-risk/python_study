"""
=========================================
学习笔记:pandas入门(Day 5)
日期:2026-09-26
=========================================
- 核心概念:DataFrame 是二维表格,Series 是一列数据。
- 数据读取:pd.read_csv() 读取 CSV 文件。
- 数据查看:head(), info(), describe(), shape。
- 数据筛选:df[df["列名"] > 值]（类比 Day 4 的列表推导式）。
"""
import pandas as pd
pd.set_option('display.unicode.east_asian_width', True)

print("--- 模块一：创建DataFrame ---")

data={
    "客户ID": ["C001", "C002", "C003", "C004", "C005"],
    "姓名": ["张三", "李四", "王五", "赵冉冉", '蕾果盆'],
    "年龄": [30, 22, 45, 18, 19],
    "月收入": [15000, 4800, 25000, 8000, 12000],
    "债务比率": [0.5, 0.8, 0.3, 0.6, 0.0],
    "是否违约": [False, True, False, False, False]
}
df=pd.DataFrame(data)
print(df)
c=df[(df['年龄']<18) | (df['债务比率']>0.7)][['姓名']]
print(c)
print('\n--- 模块二：读取CSV文件 ---')
df.to_csv("credit_data.csv", index=False, encoding="utf-8-sig")  # 保存为CSV文件
print('已保存为客户数据.csv文件')

df_read=pd.read_csv('credit_data.csv')  # 读取CSV文件
print(df_read.head())  # 查看前5行数据

print(f'\n数据形状(行数, 列数): {df_read.shape}')
print(f'\n数据基本信息:')

df_read.info()  

print(f'\n数据描述性统计:')
print(df_read.describe())

print('\n--- 模块三：pandas条件数据筛选 ---')
low_income=df_read[df_read["月收入"] < 5000]  # 筛选月收入低于5000的客户
print(f'\n月收入低于5000的客户数据:')
print(low_income)

high_risk=df_read[(df_read["月收入"] < 10000) | (df_read["是否违约"] == True)]  # 筛选月收入低于10000的客户
print(f'\n高风险客户数据:')
print(high_risk)

names_and_income=df_read[df_read['债务比率'] > 0.5][['姓名', '月收入']]  # 筛选债务比例大于0.5的客户的姓名和月收入
print(f'\n债务比例大于0.5的客户姓名和月收入:')
print(names_and_income)

income_average=df_read['月收入'].mean()  # 计算月收入的平均值
print(f'\n月收入的平均值: {income_average}')

debt_max=df_read['债务比率'].max()  # 计算债务比例的最大值
print(f'\n债务比例的最大值: {debt_max}')

c.to_csv('high_risk_customers.csv', index=False, encoding='utf-8-sig')  # 保存筛选结果为CSV文件
print('\n已保存筛选结果为high_risk_customers.csv文件')
