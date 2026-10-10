"""
=========================================
学习笔记：逻辑回归评分卡（Day 10）
日期：2026-10-08
=========================================
- 评分卡核心：逻辑回归 + WOE 转换 + 刻度映射
- 模型评估：AUC（区分度）、KS（风控最常用）
- 评分刻度：score = A - B * ln(odds)
  B = PDO / ln(2)，A = base_score + B * ln(base_odds)
- 输出：每个特征每个箱对应的分数
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, roc_curve
import matplotlib.pyplot as plt
pd.set_option('display.unicode.east_asian_width', True)
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

print('---模块一：准备数据与分箱---')

np.random.seed(42)
n=500
df=pd.DataFrame({
    "客户ID": [f"C{i:04d}" for i in range(1, n+1)],
    "年龄": np.random.randint(18, 60, n),
    "月收入": np.random.randint(3000, 30000, n),
    "负债率": np.round(np.random.uniform(0.1, 0.9, n), 2),
    "是否违约": np.random.choice([True, False], n, p=[0.3, 0.7])
})

# 分箱

df["年龄段"] = pd.cut(df["年龄"], bins=[18, 30, 45, 60], labels=["青年", "中年", "老年"], right=False)
df["收入分组"] = pd.qcut(df["月收入"], q=4, labels=["低", "中低", "中高", "高"])
df["负债分组"] = pd.cut(df["负债率"], bins=[0, 0.3, 0.6, 1.0], labels=["低负债", "中负债", "高负债"], right=False)



print('---模块二：woe转化---')
def calculate_woe_iv(df, feature, target):
    grouped=df.groupby(feature,observed=True)[target].agg(['count','sum'])
    grouped.columns=['总样本数','坏样本数']#直接给 `columns` 属性赋值，一次性替换所有列名：
    #- 第 1 列 `count` → 重命名为 **总样本数**：代表该分箱 / 分组内的全部样本数量
    #- 第 2 列 `sum` → 重命名为 **坏样本数**：代表该分箱内违约 / 负向样本（target=1）的数量
    grouped['好样本数'] = grouped['总样本数'] - grouped['坏样本数']
    #计算全体坏样本、好样本总数
    total_bad = grouped['坏样本数'].sum()
    total_good = grouped['好样本数'].sum()
    # 4. 计算每箱的坏样本占比、好样本占比
    grouped['坏样本占比'] = grouped['坏样本数'] / total_bad
    grouped['好样本占比'] = grouped['好样本数'] / total_good
    # 5. 计算 WOE = ln(坏样本占比 / 好样本占比)
    # 加 1e-10 防止分母为 0
    grouped['WOE'] = np.log((grouped['坏样本占比'] + 1e-10) / (grouped['好样本占比'] + 1e-10))
    # 6. 计算每个箱对 IV 的贡献：(坏占比 - 好占比) * WOE
    grouped['IV贡献'] = (grouped['坏样本占比'] - grouped['好样本占比']) * grouped['WOE']
    # 7. IV = 所有箱的 IV 贡献之和
    iv = grouped['IV贡献'].sum()

    return grouped, iv

def apply_woe(df,feature,woe_df):
    # 把箱标签到 WOE 的映射做成字典
    woe_map = woe_df['WOE'].to_dict()
    #转成字典是为了后续用`map`做高效的键值匹配，比逐行循环查找效率高很多

    # 用 map 替换原始值
    return df[feature].map(woe_map)


features = ['年龄段', '收入分组', '负债分组']
woe_dfs = {}
for feat in features:
    woe_df, iv = calculate_woe_iv(df, feat, '是否违约')
    woe_dfs[feat] = woe_df
    print(f"特征「{feat}」IV = {iv:.4f}")
    df[feat + '_WOE'] = apply_woe(df, feat, woe_df)


print("\nWOE转换后的数据前5行：")
print(df[['年龄段', '年龄段_WOE', '收入分组', '收入分组_WOE', '负债分组', '负债分组_WOE']].head())

print('\n---模块三：逻辑回归建模与评估---')

woe_features = [f + '_WOE' for f in features]
X = df[woe_features]
y = df['是否违约'].astype(int)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
#调用sklearn的train_test_split函数，将数据集按7:3拆分为训练集和测试集：
#test_size=0.3：30% 样本作为测试集，用于评估模型泛化能力；剩余 70% 为训练集，用于拟合模型。
#random_state=42：固定随机种子，保证每次运行代码的划分结果完全一致，实验可复现。
#返回值按固定顺序：训练集特征、测试集特征、训练集标签、测试集标签。


model = LogisticRegression()
model.fit(X_train, y_train)
#风控评分卡几乎都使用逻辑回归，核心原因是解释性极强，每个特征的权重可以对应到具体分数，业务上可解释、可落地，监管层面也更容易通过。

#预测概率
y_pred_proba = model.predict_proba(X_test)[:, 1]
#predict_proba(X_test)：输出测试集每个样本属于「0 类、1 类」的概率，结果是一个两列的数组。
#[:, 1]：只取第二列，也就是样本属于**1 类（违约 / 坏客户）**的概率。这是风控最关注的数值：概率越高，代表客户违约风险越高。


#AUC 含义：衡量模型整体的好坏区分能力 —— 随机抽取一个好客户和一个坏客户，模型给坏客户打更高风险分的概率。
auc = roc_auc_score(y_test, y_pred_proba)#调用roc_auc_score，根据真实标签和预测概率计算 AUC 值。
print(f"测试集 AUC = {auc:.4f}")


fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
ks = max(tpr - fpr)
print(f"测试集 KS = {ks:.4f}")

#  画 ROC 曲线
plt.figure(figsize=(6, 5))
plt.plot(fpr, tpr, label=f'AUC = {auc:.4f}')
plt.plot([0, 1], [0, 1], 'k--')
plt.xlabel('假正率 FPR')
plt.ylabel('真正率 TPR')
plt.title('ROC 曲线')
plt.legend()
plt.tight_layout()
plt.savefig('roc_curve.png')
plt.show()

print("\n--- 模块四：评分卡刻度转换 ---")

# 设定刻度参数
base_score = 600   # 基准分
base_odds = 30     # 基准odds（好客户:坏客户 = 30:1）
PDO = 40           # 每增加40分，odds翻倍

# 计算 A 和 B
B = PDO / np.log(2)
A = base_score + B * np.log(base_odds)

print(f"B = {B:.4f}, A = {A:.4f}")

# 对测试集客户打分

# 逻辑回归的线性输出：z = intercept + coef * X

z = model.decision_function(X_test)

# 将 z 转换为概率，再转换为 odds

odds = np.exp(z)  # 因为 z = ln(odds)，所以 odds = exp(z)

# 计算分数

scores = A - B * z
print(f"测试集客户分数范围：{scores.min():.0f} - {scores.max():.0f}")
print(f"前10个客户的分数：{scores[:10].round(0)}")

# 画分数分布

plt.figure(figsize=(7, 4))
plt.hist(scores, bins=30, color='steelblue', edgecolor='black')
plt.xlabel('信用分数')
plt.ylabel('人数')
plt.title('客户信用分数分布')
plt.tight_layout()
plt.savefig('score_distribution.png')
plt.show()