from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QListWidget, QListWidgetItem, QFileDialog
from PyQt5.QtCore import Qt
from excel_processor import load_questions_from_excel
class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('刷题软件')
        self.questions = []  # 题目列表
        self.current_question_index = -1
        self.initUI()

    def initUI(self):
        # 初始化主界面布局
        self.layout = QVBoxLayout()

        # 添加一个用于显示问题的标签
        self.question_label = QLabel('问题内容显示在这里')
        self.layout.addWidget(self.question_label)

        self.btn_load_questions = QPushButton('加载题库')
        self.btn_load_questions.clicked.connect(self.loadQuestions)  # 传递函数引用，而不是调用函数
        self.layout.addWidget(self.btn_load_questions)

        # 创建列表控件,添加一个列表来显示所有题目
        self.question_list = QListWidget()  # 确保这行代码在添加item之前
        self.question_list.itemClicked.connect(self.displaySelectedQuestion)  # 这里正确使用了itemClicked信号
        self.layout.addWidget(self.question_list)

        # 设置中央部件和布局
        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

    def loadQuestions(self):
        # 打开文件对话框让用户选择题库Excel文件
        file_path, _ = QFileDialog.getOpenFileName(self, "加载题库", "", "Excel文件 (*.xlsx *.xls)")
        if file_path:
            # 使用excel_processor模块的函数来加载问题
            self.questions = load_questions_from_excel(file_path)
            # 填充问题列表
            self.populateQuestionList('单选')  # 首先加载单选题
            self.populateQuestionList('判断')  # 然后加载判断题

    def populateQuestionList(self, question_type):
        # 获取指定类型的题目
        questions_of_type = self.questions.get(question_type, [])

        # 将题目添加到列表中
        for question in questions_of_type:
            # 确保序号是有效的
            if question['序号'] is not None and question['题目'] is not None:
                # 生成列表项的文本
                item_text = f"{question_type} {question['序号']}: {question['题目']}"
                item = QListWidgetItem(item_text)
                item.setData(Qt.UserRole, (question_type, question['序号']))  # 保存题型和序号
                self.question_list.addItem(item)

    def displaySelectedQuestion(self):
        item = self.question_list.currentItem()
        if not item:
            print("No item selected")
            return

        question_data = item.data(Qt.UserRole)
        question_type, question_number = question_data

        # 根据题型和序号找到问题
        question = next((q for q in self.questions[question_type] if str(q['序号']) == str(question_number)), None)

        if question:
            # 根据是单选题还是判断题来展示问题和选项
            if question_type == '单选':
                display_text = f"{question['题目']}\nA. {question['A']}\nB. {question['B']}\nC. {question['C']}\nD. {question['D']}"
            else:
                display_text = f"{question['题目']}\n答案: {'正确' if question['答案'] else '错误'}"

            self.question_label.setText(display_text)
        else:
            print(f"Question {question_number} not found")


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec_())
