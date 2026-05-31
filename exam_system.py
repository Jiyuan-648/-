import os
import random
from student import Student


class ExamSys:
    """学生信息与考场管理系统类，封装所有业务功能"""
    def __init__(self):
        # 存储所有Student对象的列表
        self.students = []
        # 存储考场安排后的学生列表（打乱顺序后）
        self.arranged_students = []
        # 启动时自动从文件加载学生信息
        self.load_students()

    def load_students(self):
        """
        从"人工智能编程语言学生名单.txt"文件中读取学生信息，
        解析每一行数据并创建Student对象，存入self.students列表。
        文件格式：第一行为表头（序号	姓名	性别	班级	学号	学院），
        后续每行为一个学生的数据，以制表符（\t）分隔。
        """
        filename = "人工智能编程语言学生名单.txt"
        try:
            with open(filename, "r", encoding="utf-8") as f:
                lines = f.readlines()
            # 跳过第一行表头，从第二行开始解析学生数据
            for line in lines[1:]:
                line = line.strip()
                if not line:
                    continue
                parts = line.split("\t")
                if len(parts) < 6:
                    continue
                seq_no = parts[0]
                name = parts[1]
                gender = parts[2]
                class_name = parts[3]
                student_id = parts[4]
                college = parts[5]
                stu = Student(seq_no, name, gender, class_name, student_id, college)
                self.students.append(stu)
            print(f"成功加载 {len(self.students)} 名学生信息。")
        except FileNotFoundError:
            print(f"错误：找不到文件 '{filename}'，请确认文件已放置在程序根目录下。")

    def find_student(self):
        """
        查询学生信息：用户输入学号，系统查找并打印该学生的完整信息。
        如果学号不存在则给出友好错误提示。
        """
        student_id = input("请输入要查询的学号：").strip()
        for stu in self.students:
            if stu.student_id == student_id:
                print("\n查询结果：")
                print(stu)
                return
        # 遍历完未找到则提示错误
        print(f"未找到该学号对应的学生，请检查输入是否正确。")

    def random_roll_call(self):
        """
        随机点名：用户输入需要点名的学生数量，
        系统返回对应数量的不重复随机学生名单（姓名+学号）。
        使用try-except处理输入中的各种边界情况。
        """
        user_input = input("请输入需要点名的学生数量：").strip()
        try:
            n = int(user_input)
        except ValueError:
            print("输入错误：请输入一个有效的数字。")
            return

        if n <= 0:
            print("输入错误：点名人数必须大于0。")
            return

        if n > len(self.students):
            print(f"输入错误：点名人数（{n}）超过了学生总人数（{len(self.students)}）。")
            return

        # 使用random.sample实现不重复随机抽取
        selected = random.sample(self.students, n)
        print("\n本次随机点名结果：")
        for i, stu in enumerate(selected, 1):
            print(f"{i}. {stu.name} {stu.student_id}")

    def generate_exam_arrangement(self):
        """
        生成考场安排表：将全班学生顺序随机打乱，
        在程序根目录下输出"考场安排表.txt"，
        每一行格式：考场座位号,姓名,学号
        """
        # 打乱学生列表副本，不影响原始列表
        self.arranged_students = self.students[:]
        random.shuffle(self.arranged_students)
        filename = "考场安排表.txt"
        with open(filename, "w", encoding="utf-8") as f:
            for i, stu in enumerate(self.arranged_students, 1):
                f.write(f"{i},{stu.name},{stu.student_id}\n")
        print(f"考场安排表已生成，共 {len(self.arranged_students)} 名学生，请查看 '{filename}'。")

    def generate_admission_tickets(self):
        """
        生成准考证：在程序根目录下创建"准考证"文件夹，
        根据已生成的考场安排信息，为每名学生生成独立的准考证文件。
        文件名：座位号.txt，内容包含考场座位号、姓名和学号。
        如果文件夹已存在则正常覆盖或更新其中的文件（不报错）。
        """
        if not self.arranged_students:
            print("提示：尚未生成考场安排表，正在自动生成...")
            self.generate_exam_arrangement()
        # 创建准考证文件夹，exist_ok=True 保证文件夹已存在时不报错
        dirname = "准考证"
        os.makedirs(dirname, exist_ok=True)
        for i, stu in enumerate(self.arranged_students, 1):
            # 文件名使用座位号，如 1.txt, 2.txt
            ticket_filename = os.path.join(dirname, f"{i}.txt")
            with open(ticket_filename, "w", encoding="utf-8") as f:
                f.write(f"考场座位号:{i}\n")
                f.write(f"姓名:{stu.name}\n")
                f.write(f"学号:{stu.student_id}\n")
        print(f"准考证文件已生成，共 {len(self.arranged_students)} 份，请查看 '{dirname}/' 文件夹。")
