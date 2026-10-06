"""
=========================================
学习笔记：WOE与IV计算（Day 9）
日期：2026-10-04
=========================================
- WOE = ln( (坏样本占比) / (好样本占比) )
- IV = Σ (坏样本占比 - 好样本占比) × WOE
- 作用：衡量分箱后特征的预测能力，常用于评分卡特征筛选。
"""
import pandas as pd
import numpy as np
pd.set_option('display.unicode.east_asian_width', True)
print('IV 值的经验判断：,IV < 0.02：预测力极弱,0.2 ≤ IV < 0.1：预测力弱,0.1 ≤ IV < 0.3：预测力中等,0.3 ≤ IV < 0.5：预测力强,IV ≥ 0.5：预测力极强（但要警惕过拟合）')





print('---模块一：准备数据并分箱---')
# 模拟 100 个客户，年龄、月收入、是否违约
np.random.seed(42)
df=pd.DataFrame({
    "客户ID": [f"C{i:03d}" for i in range(1, 101)],
    "年龄": np.random.randint(18, 60, 100),
    "月收入": np.random.randint(3000, 30000, 100),
    "是否违约": np.random.choice([True, False], 100, p=[0.3, 0.7])
})

#对年龄分箱
bins=[18,30,45,60]
labels=['青年','中年','老年']
df['年龄段']=pd.cut(df['年龄'], bins=bins, labels=labels, right=False)

#对月收入分箱
df['收入分组']=pd.qcut(df['月收入'],q=4,labels=['低','中低','中高','高'])

print('数据前五行：')
print(df.head())

print('---模块二：计算woe和iv---')

def calculate_woe_iv(df,feature,target):
     """
    计算某个特征分箱后的WOE和IV
    df: DataFrame
    feature: 特征列名（如'年龄段'）
    target: 目标列名（如'是否违约'）
    返回: 包含统计信息的DataFrame，以及IV值
    """

     #1.按特征分组，统计好坏样本数
     grouped=df.groupby(feature,observed=True)[target].agg(['count','sum'])
     grouped.columns = ['总样本数', '坏样本数']
     grouped['好样本数'] = grouped['总样本数'] - grouped['坏样本数']\

     #2.计算总坏样本数量和总好样本数
     total_bad=grouped['坏样本数'].sum()
     total_good=grouped['好样本数'].sum()

     #3.计算好坏样本占比
     grouped['坏样本占比'] = grouped['坏样本数'] / total_bad
     grouped['好样本占比'] = grouped['好样本数'] / total_good
     # 4. 计算WOE
     # 防止除零，加一个极小值
     grouped['WOE'] = np.log((grouped['坏样本占比'] + 1e-10) / (grouped['好样本占比'] + 1e-10))
     # 5. 计算IV
     grouped['IV贡献'] = (grouped['坏样本占比'] - grouped['好样本占比']) * grouped['WOE']
     iv = grouped['IV贡献'].sum()
    
     return grouped, iv

df['收入分档']=pd.cut(df['月收入'],bins=[0,5000,15000,30000],labels=['低','中','高'])
income_level_woe,income_level_iv=calculate_woe_iv(df,'收入分档','是否违约')
print('收入分档的woe')
print(income_level_woe)
print('收入分档的iv')
print(income_level_iv)




#计算年龄段woe和iv
age_woe,age_iv=calculate_woe_iv(df,'年龄段','是否违约')
print('年龄段的woe')
print(age_woe)
print(f'年龄段的iv:{age_iv:.4f}')

#计算收入分组的woe和iv
income_woe,income_iv=calculate_woe_iv(df,'收入分组','是否违约')
print('收入分组的woe')
print(income_woe)
print(f'收入分组的iv:{income_iv:.4f}')

# 练习2：循环计算多个特征的IV
print("--- 练习2：多个特征IV比较 ---")

# 1. 定义要计算的特征列表
features = ['年龄段', '收入分组', '收入分档']  # 假设你练习1已经建好了'收入分档'列
target = '是否违约'

# 2. 用一个字典收集结果
iv_results = {}

for feat in features:
    _, iv = calculate_woe_iv(df, feat, target)  # 忽略第一个返回值，只取IV
    iv_results[feat] = iv
    print(f"特征「{feat}」的 IV 值为：{iv:.4f}")

# 3. 找出 IV 最大的特征
best_feature = max(iv_results, key=iv_results.get)#.get遍历所有iv字典中的所有值
print(f"\n预测力最强的特征是:{best_feature},IV = {iv_results[best_feature]:.4f}")




#3.可视化woe和iv
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False

#画年龄段的woe
age_woe['WOE'].plot(kind='bar',title='年龄段woe',color='steelblue')
plt.ylabel('WOE')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('age_woe.png')
plt.show()

#画收入分组的woe
income_woe['WOE'].plot(kind='bar', title='收入分组WOE', color='orange')
plt.ylabel('WOE')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('income_woe.png')
plt.show()

#画收入分档的woe
income_level_woe['WOE'].plot(kind='bar',title='收入分档woe',color='pink')
plt.ylabel('WOE')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('income_level_woe.png')
plt.show()