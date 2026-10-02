"""
=========================================
学习笔记：pandas进阶（Day 7）
日期：2026-10-02
=========================================
- apply：把自定义函数应用到整列或整行
- map：把映射关系应用到Series（常用于替换标签）
- lambda：匿名函数，配合apply/map写一行函数
- merge：按某列合并两张表（类似SQL的JOIN）
- crosstab：交叉表，行风控多维统计
"""
import pandas as pd
import numpy as np
pd.set_option('display.unicode.east_asian_width',True)#显示中文

print('---模块一：apply/map/lambda---')

df=pd.DataFrame({
    "客户ID": ["C001", "C002", "C003", "C004", "C005"],
    "姓名": ["张三", "李四", "王五", "赵六", "孙七"],
    "年龄": [30, 22, 45, 17, 35],
    "月收入": [15000, 4800, 25000, 8000, 12000],
    "是否违约": [False, True, False, False, True]
})
# 1. apply：自定义函数应用整列（例子为单列表判定）
def income_level(income):
    if income >=20000:
        return "高收入"
    elif income >=8000:
        return "中等收入"
    else:
        return "低收入"
df['收入等级']=df['月收入'].apply(income_level)
print('用apply函数新增收入等级')
print(df)
#练习1 新增负债承受力(多列表判定)
def income_capacity(row):
    if row['月收入'] >=15000 and row['是否违约']==False:
        return "高"
    else:
        return "低"
df['负债承受力']=df.apply(income_capacity,axis=1)
print('\n用apply函数新增负债承受力')
print(df)


# 2. lambda：匿名函数，一行搞定
df['是否成年']=df['年龄'].apply(lambda x:'成年' if x >=18 else '未成年')
print('\n用lambda函数新增是否成年')
print(df)

#3. map标签映射（把True/False映射为中文）
df['违约标签']=df['是否违约'].map({True:'已违约',False:'未违约'})
print('\n用map函数新增违约标签')
print(df[["姓名", "是否违约", "违约标签"]])

print('\n---模块二:merge模块合并多表格---')
#1.客户信息表
customers=pd.DataFrame({
    "客户ID": ["C001", "C002", "C003", "C004"],
    "姓名": ["张三", "李四", "王五", "赵六"],
    "城市": ["上海", "北京", "上海", "广州"]
})
#2.贷款记录
loans=pd.DataFrame({
    "客户ID": ["C001", "C002", "C002", "C003", "C005"],
    "贷款金额": [50000, 20000, 15000, 80000, 30000],
    "贷款类型": ["消费贷", "信用贷", "信用贷", "房贷", "消费贷"]
})

# 1.inner_join:只保留两边都有的数据
inner_join=pd.merge(customers,loans,on="客户ID",how="inner")
print('inner_Join 只保留两边都有的客户')
print(inner_join)

# 2.left_join:保留左表所有数据，右表没有的用NaN填充
left_join=pd.merge(customers,loans,on="客户ID",how="left")
print('\nleft_Join 保留所有客户,右表没有的用NaN填充')
print(left_join)

# 练习2  2.5  .right_join:保留右表所有数据，左表没有的用NaN填充
right_join=pd.merge(customers,loans,on="客户ID",how="right")
print('\nright_Join 保留所有贷款记录,左表没有的用NaN填充')
print(right_join)




# 3.city_join: 按城市统计贷款总额(整合后聚合)
city_loan=pd.merge(customers,loans,on='客户ID',how='inner')
city_summary=city_loan.groupby('城市')['贷款金额'].sum()
print('\n按城市统计贷款总额')
print(city_summary)


print('\n---模块三:交叉表crosstab---')

df_risk=pd.DataFrame({
    "客户ID": ["C001", "C002", "C003", "C004", "C005", "C006", "C007", "C008"],
    "年龄段": ["青年", "青年", "中年", "中年", "老年", "青年", "中年", "老年"],
    "收入等级": ["高", "低", "高", "中", "中", "低", "低", "高"],
    "是否违约": [False, True, False, False, True, True, True, False]
})

# 1.交叉表：年龄段vs是否违约（统计人数）
ct_count=pd.crosstab(df_risk['年龄段'],df_risk['是否违约'])
print('交叉表统计人数：年龄段vs是否违约')
print(ct_count)

# 2.交叉表：按行计算百分比（看违约率）
ct_pct=pd.crosstab(df_risk['年龄段'],df_risk['是否违约'],normalize='index')
print('\n交叉表计算百分比：年龄段vs是否违约（违约率）')
print(ct_pct)

 # 3.多维交叉表：年龄+收入等级vs违约
ct_multi=pd.crosstab([df_risk['年龄段'],df_risk['收入等级']],df_risk['是否违约'])
print('\n年龄+收入等级vs违约情况')
print(ct_multi)

# 4. 用aggfunc做聚合（计算平均收入而非计数）
ct_mean=pd.crosstab(df_risk["年龄段"], df_risk["是否违约"], values=df_risk["客户ID"].map({"C001":15000,"C002":4800,"C003":25000,"C004":8000,"C005":12000,"C006":6000,"C007":5000,"C008":30000}), aggfunc='mean')
print('\n各年龄段不同违约状态的平均收入')
print(ct_mean)
# 练习3 “收入等级 vs 是否违约”的交叉表（人数统计和行百分比各一份）
ct_income_credit_count=pd.crosstab(df_risk['收入等级'],df_risk['是否违约'])
print('\n收入等级 vs 是否违约（人数统计）')
print(ct_income_credit_count)

#练习4 用 merge 把 customers 和 loans 合并后，按“城市”分组，计算每个城市的贷款笔数和平均贷款金额
city_loans=pd.merge(customers,loans,on='客户ID',how='inner')
city_summary=city_loans.groupby('城市').agg({'贷款金额': ['count', 'mean']})
print('\n每个城市的贷款笔数和平均贷款金额')
print(city_summary)