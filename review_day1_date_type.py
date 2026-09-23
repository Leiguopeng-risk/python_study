
print("----客户数据录入系统----")
name = input("请输入客户姓名：")
age = int(input("请输入客户年龄："))
income = float(input("请输入客户收入："))
print("客户信息录入成功！")
if income < 5000 or age < 18:
    risk_level = "高风险"
else:
    risk_level = "低风险"
print(f"客户姓名：{name}，年龄：{age}，收入：{income}，风险等级：{risk_level}")#这有一块关于f-string的学习
print("----客户数据录入系统结束----")