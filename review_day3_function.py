"""
=========================================
复习笔记:函数与模块(Functions & Modules)
日期:2026-09-24
=========================================
- 函数 def:把一段可复用的逻辑封装起来，通过参数接收输入，通过 return 返回结果。
- 参数：函数定义时的占位符，调用时传入实际值。
- 返回值：函数执行完后的输出，用 return 返回，调用处可以接收。
- 模块 import:导入 Python 自带的或第三方的功能包（如 math, random)。
- 风控场景：封装 check_risk(income, overdue, age) 函数，便于批量判断客户风险。
"""
print('---风控函数封装练习---')
def check_risk(income, overdue, age,debt_ratio):
    """
    风控函数:根据收入、逾期次数和年龄判断客户风险等级
    :param income: 收入水平
    :param overdue: 逾期次数
    :param age: 年龄
    :param debt_ratio: 债务比率
    :return: 风险等级字符串
    """
    if debt_ratio>0.7:
        return '高风险','债务比率过高'
    if age<18:
        return '高风险','未成年'
    if income>=5000 and not overdue:
        return '低风险','收入充足且无逾期'
    else:
        return '高风险','有逾期记录或收入不足'
customers = [
    {"name": "张三", "age": 30, "income": 15000, "overdue": False, "debt_ratio": 0.5},
    {"name": "李四", "age": 22, "income": 4800, "overdue": True, "debt_ratio": 0.8},
    {"name": "王五", "age": 45, "income": 25000, "overdue": False, "debt_ratio": 0.3},
    {"name": "赵六", "age": 17, "income": 8000, "overdue": False, "debt_ratio": 0.6}  # 测试未成年人
]

for c in customers:
    risk,reason=check_risk(c['income'], c['overdue'], c['age'], c['debt_ratio'])
    print(f'客户{c['age']}岁，收入{c['income']}元，逾期:{c['overdue']}，债务比率{c['debt_ratio']:.1f}，风险等级: {risk}, 原因:({reason})')
import math,random
customers_random=[]
for i in range(5):
    random_income=random.randint(3000, 30000)
    random_age=random.randint(18, 60)
    random_overdue=random.choice([True, False])
    random_debt_ratio=round(random.uniform(0.1, 0.9),2)
    customers_random.append({"name": f"客户{i+1}", "age": random_age, "income": random_income, "overdue": random_overdue, "debt_ratio": random_debt_ratio})

for check in customers_random:
    risk,reason=check_risk(check['income'], check['overdue'], check['age'], check['debt_ratio'])
    print(f'{check['name']}   客户{check['age']}岁，收入{check['income']}元，逾期:{check['overdue']}，债务比率{check['debt_ratio']:.1f}，风险等级: {risk}, 原因:({reason})')



