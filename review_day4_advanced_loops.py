"""
=========================================
复习笔记：条件与循环进阶
日期:2026-09-25
=========================================
- 列表推导式：[表达式 for 变量 in 列表 if 条件]
- 嵌套循环:for 外层 in 外层列表: for 内层 in 内层列表:
- enumerate:同时获取索引和值,避免手动维护计数器
- zip:将两个列表按位置打包成元组，适合合并客户姓名和收入
"""

print("--- 模块一：列表推导式 ---")
customers = [
    {"name": "张三", "age": 30, "income": 15000, "overdue": False, "debt_ratio": 0.5},
    {"name": "李四", "age": 22, "income": 4800, "overdue": True, "debt_ratio": 0.8},
    {"name": "王五", "age": 45, "income": 25000, "overdue": False, "debt_ratio": 0.3},
    {"name": "赵六", "age": 17, "income": 8000, "overdue": False, "debt_ratio": 0.6}
]
# 1. 传统方式：筛选出所有高风险客户的姓名
high_risk_list = []
for c in customers:
    if c["income"] < 5000 or c["overdue"]:
        high_risk_list.append(c["name"])
print(f"传统方式筛选高风险客户：{high_risk_list}")

# 2. 列表推导式：一行搞定
high_risk_comp =[c['name']for c in customers if c['income']<5000 or c['overdue']]
print(f"列表推导式筛选高风险客户：{high_risk_comp}")
all_annual_income = sum([c['income']*12 for c in customers])
print(f"所有客户的年收入总和为：{all_annual_income}元") 
high_debt_ratio_customers = [c['name'] for c in customers if c['debt_ratio'] > 0.5]
print(f"债务比率大于0.5的客户有：{high_debt_ratio_customers}")

print("--- 模块二：嵌套循环 ---")
customers_loans=[
    {"name": "张三", "loans": [5000, 2000, 3000]},
    {"name": "李四", "loans": [10000]},
    {"name": "王五", "loans": [20000, 15000]}
]
for index,c in enumerate(customers_loans):
    total_loans = 0
    for loan in c["loans"]:
        total_loans += loan
    print(f"第{index+1}位客户：{c['name']}的贷款总额为：{total_loans}元")


print("--- 模块三:enumerate与zip ---")
names = ["张三", "李四", "王五"]
incomes = [15000, 4800, 25000]
for index,(name,income) in enumerate(zip(names, incomes)):
    print(f"第{index+1}位客户：{name}的收入为：{income}元")