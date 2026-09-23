"""
=========================================
复习笔记:列表与字典(List & Dict)
日期:2026-09-23
=========================================
- 列表 list:用 [] 表示，有序，用来存一批数据（如多个客户）
- 字典 dict:用 {} 表示，键值对，用来存单个对象的多个属性（如一个客户的姓名、收入）
- 核心组合：列表套字典 -> [ {"name": "张三", "income": 15000}, {"name": "李四", ...} ]
- 循环：用 for 遍历列表，用 dict["key"] 取值
"""

print("----客户数据批量管理系统----")
customers = [{"name": "张三", "age": 30, "income": 15000, "overdue": False},{"name": "李四", "age": 22, "income": 4800, "overdue": True},{"name": "王五", "age": 45, "income": 25000, "overdue": False}]  # 用来存储多个客户的列表
for customer in customers:  # 遍历列表
    name = customer["name"]  # 取字典的值
    age = customer["age"]
    income = customer["income"]
    overdue = customer["overdue"]
    if income >= 5000 and not overdue:  # 判断风险等级
        risk_level = "低风险"
    else:
        risk_level = "高风险"
    print(f"客户姓名：{name}，年龄：{age}，收入：{income}，是否逾期：{overdue}，风险等级：{risk_level}")
customers.append({"name": "赵六", "age": 35, "income": 8000, "overdue": False})  # 添加新客户

print(f"\n当前客户总数:{len(customers)}")  # len() 获取列表长度
total_income = sum(customer["income"] for customer in customers)  # 计算总收入
print(f"当前客户总收入:{total_income:,.2f}元")  # 格式化输出总收入，保留两位小数并加上千分位分隔符
avg_income = total_income / len(customers)  # 计算平均收入
print(f"当前客户平均收入:{avg_income:,.2f}元")  # 格式化输出平均收入，保留两位小数并加上千分位分隔符