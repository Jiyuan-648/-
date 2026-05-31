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
