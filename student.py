class Student:
    """学生类，用于存储单个学生的基本信息"""
    def __init__(self, seq_no, name, gender, class_name, student_id, college):
        # 序号
        self.seq_no = seq_no
        # 姓名
        self.name = name
        # 性别
        self.gender = gender
        # 班级
        self.class_name = class_name
        # 学号
        self.student_id = student_id
        # 学院
        self.college = college

    def __str__(self):
        """返回学生的完整信息字符串，用于查询时打印"""
        return (
            f"序号：{self.seq_no}\n"
            f"姓名：{self.name}\n"
            f"性别：{self.gender}\n"
            f"班级：{self.class_name}\n"
            f"学号：{self.student_id}\n"
            f"学院：{self.college}"
        )
