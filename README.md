# 刘子扬-25361125-第二次人工智能编程作业

仓库链接: https://github.com/Jiyuan-648/-

## 1. 任务拆解与AI协作策略

（请简述你在编写代码前，是如何将这个大任务拆解给 AI 的？先让 AI 写了什么，后写了什么？）

在开始编写代码之前，我首先通读了作业文档的全部要求，明确了三个核心约束：必须使用面向对象编程、代码须拆分为三个模块文件、只能使用 os 和 random 标准库。基于这些约束，我将任务拆分为以下步骤与 AI 协作：

步骤1：先让 AI 生成 Student 类。我只提供了学生名单文件的表头字段（序号、姓名、性别、班级、学号、学院），要求 AI 定义对应的属性和一个 `__str__` 方法用于查询时打印完整信息。这个任务简单明确，AI 一次就给出了符合要求的结果。

步骤2：在 Student 类完成后，让 AI 搭建 ExamSys 类的框架，重点是 `load_students()` 方法。我告诉 AI 学生名单是制表符分隔的文本文件、第一行是表头、编码为 UTF-8，并明确要求用 try-except 捕获 FileNotFoundError。这一步是后续所有功能的数据基础。

步骤3：依次实现 find_student、random_roll_call、generate_exam_arrangement、generate_admission_tickets 四个功能。每完成一个功能，我让 AI 解释代码逻辑，确认我理解后再进入下一个。random_roll_call 的异常处理是重点，我明确向 AI 列出了需要捕获的三种边界情况。

步骤4：最后实现 run() 主菜单循环和 main.py 入口，将各部分串联成完整系统。

整个过程中，我始终坚持"局部代码让 AI 辅助，整体设计由自己把控"的原则。

## 2. 核心Prompt迭代记录

（展示一次你通过修改提示词，让 AI 的代码从"不符合要求"变成"完美符合工程规范"的过程）

初代 Prompt：
> "帮我写一个随机点名的功能，输入人数返回随机学生名单。"

AI 生成的问题/缺陷：
AI 第一版代码使用了 `random.choice()` 在一个循环中反复抽取，但没有做去重处理，可能导致同一个学生被多次点名。此外，代码直接将 `input()` 的返回值传给 `int()`，如果用户输入了非数字字符（如 "abc"），程序会直接崩溃抛出 ValueError，完全没有异常处理。输入人数为负数或0也没有任何校验。

优化后的 Prompt（追问）：
> "上面的随机点名功能有几个问题需要修复：
> 1. 必须保证抽取的学生不重复，请使用 random.sample 替代 random.choice；
> 2. 使用 try-except 捕获用户输入非数字字符的情况，给出友好提示而非崩溃；
> 3. 增加判断：如果输入人数小于等于0、或超过学生总人数，都要给出明确的错误提示。
> 另外，代码中只能使用 random 模块，不要引入其他第三方库。"

AI 收到追问后，使用 `random.sample()` 一次性完成不重复抽取，并在输入处理外围加了完整的 try-except 和条件判断。这次输出的代码直接通过了我的所有边界测试（输入 "abc"、输入 -3、输入 100 等场景），达到了作业要求的工程规范。

## 3. Debug与异常处理记录

（记录一次解决报错或发现AI逻辑漏洞的过程）

报错类型/漏洞现象：
在首次运行 `generate_admission_tickets` 功能时，程序抛出 `FileNotFoundError`，提示找不到路径。Traceback 定位在 `os.makedirs(dirname)` 这一行。一开始以为是文件夹权限问题，但检查后发现报错原因是：在调用 `generate_admission_tickets` 前没有先生成考场安排，`self.arranged_students` 列表为空，但 AI 初版代码直接使用了 `os.makedirs(dirname)` 而没有加 `exist_ok=True`，更重要的是也没有检查安排表是否存在就直接遍历生成文件。

解决过程：
我先自己看了 Traceback，理解了错误发生的调用链。然后将错误信息和上下文一起喂给 AI，追问："当 arranged_students 为空时，generate_admission_tickets 应该先自动调用 generate_exam_arrangement 生成考场安排，而不是直接报错退出。" 同时提醒 AI 将 `os.makedirs(dirname)` 改为 `os.makedirs(dirname, exist_ok=True)`，防止重复运行时因文件夹已存在而报错。最终修改了 generate_admission_tickets 开头增加了判断逻辑，并在 mkdir 调用中加上了 exist_ok 参数，问题彻底解决。

## 4. 人工代码审查 (Code Review)

（请贴出一段 AI 生成的核心逻辑代码，并加上你自己的逐行中文注释，证明你完全理解了它的运行机制）

```python
def random_roll_call(self):
    """
    随机点名：用户输入需要点名的学生数量，
    系统返回对应数量的不重复随机学生名单（姓名+学号）。
    使用try-except处理输入中的各种边界情况。
    """
    # 接收用户输入并去掉首尾空格
    user_input = input("请输入需要点名的学生数量：").strip()
    try:
        # 尝试将输入字符串转为整数，如果输入的不是数字会触发ValueError
        n = int(user_input)
    except ValueError:
        # 捕获非数字输入，给出友好提示后直接返回，不让程序崩溃
        print("输入错误：请输入一个有效的数字。")
        return

    # 边界判断1：点名人数必须大于0
    if n <= 0:
        print("输入错误：点名人数必须大于0。")
        return

    # 边界判断2：点名人数不能超过班级总人数
    if n > len(self.students):
        print(f"输入错误：点名人数（{n}）超过了学生总人数（{len(self.students)}）。")
        return

    # 使用random.sample从学生列表中随机抽取n个不重复的学生
    # sample保证每个学生最多被选中一次，且结果顺序也是随机的
    selected = random.sample(self.students, n)
    print("\n本次随机点名结果：")
    # enumerate(selected, 1) 让序号从1开始，而不是默认的0
    for i, stu in enumerate(selected, 1):
        print(f"{i}. {stu.name} {stu.student_id}")
```

这段代码的核心逻辑是：先通过 try-except 将可能出错的类型转换保护起来，再用两个 if 条件分别拦截"人数≤0"和"人数超限"两种非法输入。只有当所有校验都通过后，才调用 `random.sample` 进行不重复随机抽取。这样的三层防护（类型校验→范围校验→逻辑校验）保证了无论用户输入什么内容，程序都能给出合理的反馈而不会崩溃。
