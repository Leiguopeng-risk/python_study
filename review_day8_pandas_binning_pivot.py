"""
=========================================
学习笔记：pandas分箱与透视表（Day 8）
日期：2026-10-03
=========================================
- 分箱：pd.cut(列, bins=[...], labels=[...]) 自定义区间
- 等频分箱：pd.qcut(列, q=4) 按分位数分箱
- 透视表：pd.pivot_table(df, values, index, columns, aggfunc)
- 可视化：matplotlib 画柱状图、直方图，看违约率分布
-qcut：按分位数（等频）分箱，每个箱子里样本数量尽量一样多**
-cut：按数值区间（等宽）分箱，区间宽度固定，样本数量不均匀
函数	分箱逻辑	                                     特点
pd.cut	等宽，区间差值固定	               适合数值范围均匀，看区间大小
pd.qcut	等频，每组样本数量相近	 适合做分位数分层，消除极端值区间过大问题





"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
pd.set_option('display.unicode.east_asian_width', True)
plt.rcParams['font.sans-serif'] = ['SimHei']  # 正常显示中文
plt.rcParams['axes.unicode_minus'] = False    # 正常显示负号

print('---模块一：数据分箱（binning）---')

# 模拟二十个客户的年龄，月收入，是否违约
np.random.seed(42)
df=pd.DataFrame({
    "客户ID": [f"C{i:03d}" for i in range(1, 21)],#  f"C{i:03d}"：格式化字符串，03d代表补零到 3 位
    "年龄": np.random.randint(18, 60, 20),#`randint(low, high, size)`：生成 20 个整数，范围 `[18,60)` → 最小 18，最大 59
    "月收入": np.random.randint(3000, 30000, 20),
    "是否违约": np.random.choice([True, False], 20, p=[0.3, 0.7])#从[True,False]随机选20个 p=[0.3,0.7]：True 概率 30%（违约），False 概率 70%（不违约）
})
print('原始数据前五行')
print(df.head())

# 1. 自定义分箱：按年龄分成 青年/中年/老年

bins = [18, 30, 45, 60]
labels = ["青年", "中年", "老年"]
df["年龄段"] = pd.cut(df["年龄"], bins=bins, labels=labels, right=False)
# right=False 表示左闭右开，如 [18,30)
#- `x`：一维序列（DataFrame 某一列，如 df [' 月收入 ']）
#- `bins`：分箱方式
#  - 传整数：`bins=3` → 自动分成 3 个等宽区间
#  - 传列表：自定义区间边界 `bins=[0,10000,20000,30000]`
#- `right=True`（默认）：区间**右闭** `(a,b]`；`right=False` → `[a,b)`
#- `labels`：给每个区间设置名字，不写则返回区间字符串
#- `include_lowest=False`：是否把最小值包含进第一个区间

print("\n按年龄段分箱后：")
print(df[["年龄", "年龄段"]].head(10))


#练习1 收入档次
df['收入档次']=pd.cut(df['月收入'], bins=[0, 5000, 15000, 30000], labels=["低", "中", "高"], right=False)
print("\n按月收入档次分箱后：")
print(df[["月收入", "收入档次"]].head(10))

# 2.等频分箱：按收入分成四组（每组人数相同）
df['收入分组']=pd.qcut(df['月收入'], q=4, labels=["低", "中低", "中高", "高"])
# pd.qcut(x, q, labels=None, duplicates='raise')
#- `x`：Series / 一维数组
#- `q`：整数：`q=4` → 四分位数，分成 4 组，每组大约 25% 数据 列表：`q=[0, 0.25, 0.5, 0.75, 1]`，自定义分位数边界
#- `labels`：分组名称
#- `duplicates='raise'`：如果多个数据相同导致分箱边界重复，会报错；改成`duplicates='drop'`忽略
print("\n按月收入分组后：")
print(df[["月收入", "收入分组"]].head(10))



# 3. 统计每个年龄段的违约率
age_default=df.groupby("年龄段")["是否违约"].mean().reset_index()
print("\n每个年龄段的违约率：")
print(age_default)


print('\n---模块二:透视表（pivot table）---')
# 1. 简单透视：年龄段 vs 是否违约（计算平均违约率）
pivot1=pd.pivot_table(df, values="是否违约", index="年龄段", aggfunc="mean").reset_index()
#- `data`：DataFrame
#- `index`：放在行上的分组字段
#- `columns`：放在列上的分组字段
#- `values`：需要聚合计算的字段
# `aggfunc`：聚合函数，默认`mean`平均值；可以是`sum`/`count`/`max`/`min`，也可以传列表`[np.mean, np.sum]`
#- `fill_value`：填充缺失值
#- `margins=True`：增加 总计行 / 总计列 (All)
print('各年龄段的违约率透视表：')
print(pivot1)

# 2.多维透视：年龄段 vs 收入分组 vs 是否违约（计算平均违约率）
pivot2=pd.pivot_table(df, values="是否违约",
                       index="年龄段", 
                       columns="收入分组", 
                       aggfunc="mean").reset_index()
print("\n年龄段 + 收入分组 的违约率：")
print(pivot2)

# 3.整合透视表：同时看违约率和人数
pivot3=pd.pivot_table(df, values="是否违约",
                       index="年龄段",
                       aggfunc=['mean','count'])
print("\n年龄段的违约率和人数：")
print(pivot3)

#练习 2（透视表）：用 pivot_table 做出“收入档次 vs 是否违约”的违约率透视表。
pivot4=pd.pivot_table(df, values="是否违约", index="收入档次", aggfunc="mean").reset_index()
print("\n收入档次的违约率透视表：")
print(pivot4)




print('\n---模块三:可视化---')
# 1. 柱状图：各年龄段违约率
age_default.plot(kind='bar',title='各年龄段违约率',color="steelblue")
plt.ylabel('违约率')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('age_default_bar.png')
plt.show()
#- `kind="bar"`：垂直柱状图
#- `kind="barh"`：水平条形图
#- `kind="line"`：折线图（默认）
#- `kind="pie"`：饼图
#- `kind="hist"`：直方图
#- `figsize=(8,4)`：画布大小（宽，高）
#- `color="orange"`：柱子颜色
#- `ylabel` / `xlabel`：坐标轴名字
#- `rot=0`：x 标签旋转角度


# 2. 直方图：月收入分布
df['月收入'].plot(kind='hist',bins=10,title='月收入分布直方图',color="black")
plt.xlabel('月收入')
plt.tight_layout()
plt.savefig('income_hist.png')
plt.show()

#练习 3（可视化）：用 plot(kind="bar") 画出各“收入档次”的违约率柱状图，并保存为 income_default_rate.png。
default_rate = df.groupby('收入档次', observed=True)['是否违约'].mean()

# 2. 再画柱状图
default_rate.plot(kind='bar', title='各收入档次违约率', color='orange')
plt.ylabel('违约率')
plt.xlabel('收入档次')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('income_default_rate.png')  # 保存图片
plt.show()

#income_default_rate.png。

#练习 4（综合）：用 qcut 把“年龄”等频分成 3 组，然后看这三组的违约率差异
# 练习 4（综合）：用 qcut 把“年龄”等频分成 3 组，然后看这三组的违约率差异
df["年龄分组"] = pd.qcut(df["年龄"], q=3, labels=["年轻", "中年", "老年"])

# 先按分组求违约率
age_default_rate = df.groupby("年龄分组", observed=True)["是否违约"].mean()

# 再画柱状图
age_default_rate.plot(kind="bar", title="不同年龄段违约率差异", color="teal")
plt.xlabel("年龄段")
plt.ylabel("违约率")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("age_group_default_rate.png")  # 记得加 .png 后缀
plt.show()











