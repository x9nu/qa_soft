from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout,\
    QWidget, QLabel, QListWidget, QListWidgetItem, QFileDialog, QMessageBox, QSplitter, QCheckBox
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QColor, QFont

from excel_processor import load_questions_from_excel
from record import update_record, get_error_question_numbers

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('刷题软件')
        self.file_path=''
        self.questions = []  # 题目列表
        self.current_question_index = -1  # 当前题目索引
        self.single_choice_index=0
        self.true_false_index=0
        self.option_buttons = []
        self.question_states = {}  # 用于保存每个题目的状态
        self.correct=0
        self.errors=[]
        self.initUI()
        self.setMinimumHeight(600)
        # self.showMaximized()  # 使窗口最大化

    def initUI(self):
        # 设置全局字体大小
        font = QFont()
        font.setPointSize(14)  # 设置字体大小为14
        self.setFont(font)

        # 创建一个水平分割器
        splitter = QSplitter(self)

        # 左侧布局
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        self.question_list = QListWidget()
        self.question_list.itemClicked.connect(self.displaySelectedQuestion)
        left_layout.addWidget(self.question_list)

        self.load_button = QPushButton('加载题库')
        self.load_button.clicked.connect(self.loadQuestions)
        left_layout.addWidget(self.load_button)

        # 在左侧布局中添加一个复选框
        self.only_wrong_checkbox = QCheckBox('只刷错题')
        left_layout.addWidget(self.only_wrong_checkbox)

        left_widget.setMaximumWidth(250)  # 设置最大宽度
        left_widget.setMinimumWidth(250)  # 设置最小宽度
        splitter.addWidget(left_widget)  # 添加到分割器

        # 右侧布局
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_widget.setMinimumWidth(400)  # 设置最小宽度
        # self.question_type_label = QLabel('题型：')
        # right_layout.addWidget(self.question_type_label)

        self.question_label = QLabel('题目：')
        self.question_label.setWordWrap(True)  # 启用自动换行
        right_layout.addWidget(self.question_label)

        self.option_buttons = []
        for i in range(4):  # 假设最多4个选项
            btn = QPushButton()
            btn.clicked.connect(self.checkAnswer)
            right_layout.addWidget(btn)
            self.option_buttons.append(btn)
        splitter.addWidget(right_widget)  # 添加到分割器

        # 提交布局
        submit_widget = QWidget()
        submit_layout = QVBoxLayout(submit_widget)
        submit_widget.setMaximumWidth(200)  # 设置最大宽度
        submit_widget.setMinimumWidth(200)  # 设置最小宽度

        self.submit_button = QPushButton('交卷')
        self.submit_button.clicked.connect(self.submitAnswers)
        submit_layout.addWidget(self.submit_button)

        splitter.addWidget(submit_widget)  # 添加到分割器

        # 设置主窗口的中央部件为分割器
        self.setCentralWidget(splitter)

        # 调整按钮大小
        for btn in self.option_buttons:
            btn.setFont(font)
            btn.setMinimumHeight(40)  # 设置按钮的最小高度为40像素

        # 调整 QLabel 字体大小
        # self.question_type_label.setFont(font)
        self.question_label.setFont(font)

    def loadQuestions(self):
        self.question_states={}
        # 打开文件对话框让用户选择题库Excel文件
        self.file_path, _ = QFileDialog.getOpenFileName(self, "加载题库", "", "Excel文件 (*.xlsx *.xls)")

        if self.file_path:  # 确保用户已选择文件
            # 使用你的函数从Excel文件中加载题目
            all_questions = load_questions_from_excel(self.file_path)

            # 判断是否只加载错题
            if self.only_wrong_checkbox.isChecked():
                error_question_numbers = get_error_question_numbers('团子', self.file_path)

                self.questions = {}
                for q_type in ['单选', '判断']:
                    self.questions[q_type] = [
                        q for q in all_questions[q_type] if q['序号'] in error_question_numbers[q_type]
                    ]
            else:
                self.questions = all_questions

            # print(self.questions)

            # 清空题目列表
            self.question_list.clear()

            # 在题目列表中添加新加载的题目
            for question_type, questions in self.questions.items():
                for i, question in enumerate(questions, 1):
                    item_text = f"{question_type} {question['序号']}"
                    self.question_list.addItem(item_text)

    def displaySelectedQuestion(self, item):
        try:
            # 获取当前题目的类型和索引
            current_row = self.question_list.currentRow()
            question_type = '单选' if '单选' in self.question_list.currentItem().text() else '判断'

            if question_type == '单选':
                question_index = current_row
            else:
                question_index = current_row - len(self.questions['单选'])

            question_data = self.questions[question_type][question_index]

            # 清除之前的背景颜色
            for btn in self.option_buttons:
                btn.setStyleSheet("")

            # # 恢复保存的状态
            # state = self.question_states.get(current_row)
            # if state:
            #     self.option_buttons[state['selected_index']].setStyleSheet("background-color: red")
            #     self.option_buttons[state['correct_index']].setStyleSheet("background-color: green")
            # 恢复保存的状态
            state = self.question_states.get((question_type, question_index))
            if state:
                self.option_buttons[state['selected_index']].setStyleSheet("background-color: red")
                self.option_buttons[state['correct_index']].setStyleSheet("background-color: green")

            # 显示题目
            self.question_label.setText(f"{question_data['题目']}")

            # 显示选项
            if question_type == '单选':
                for i, option in enumerate(['A', 'B', 'C', 'D']):
                    self.option_buttons[i].setText(f"{option}. {question_data[option]}")
                    self.option_buttons[i].setVisible(True)
            elif question_type == '判断':
                self.option_buttons[0].setText("正确")
                self.option_buttons[1].setText("错误")
                for i in range(2):
                    self.option_buttons[i].setVisible(True)
                for btn in self.option_buttons[2:]:
                    btn.setVisible(False)

        except IndexError:
            print(f"Error: No question found at index {question_index} for {question_type} questions.")
        except Exception as e:
            print(f"An unexpected error occurred while displaying the question: {e}")

    def checkAnswer(self):
        sender = self.sender()
        selected_index = self.option_buttons.index(sender)

        # 获取当前题目的类型和索引
        current_row = self.question_list.currentRow()
        question_type = '单选' if '单选' in self.question_list.currentItem().text() else '判断'
        question_index = current_row if question_type == '单选' else current_row - len(self.questions['单选'])

        # 获取题目数据和正确答案
        question_data = self.questions[question_type][question_index]
        print()
        correct_answer = question_data['答案']

        # 确定正确答案的索引
        if question_type == '单选':
            correct_index = ord(correct_answer) - ord('A')
        else:
            correct_index = 0 if correct_answer else 1

        # 获取当前题目在列表中的项
        current_item = self.question_list.currentItem()

        # 检查所选答案是否正确，并相应地更新背景颜色
        if selected_index==correct_index:
            current_item.setForeground(QColor('green'))
            sender.setStyleSheet("background-color: green")
            self.option_buttons[selected_index].setStyleSheet("background-color: green")
            # 如果答案正确，从错误列表中移除题目
            # self.errors = [e for e in self.errors if e != {'type': question_type, 'index': question_data['序号']}]
            QTimer.singleShot(1000, self.loadNextQuestion)  # 正确时，1秒后加载下一题
        else:
            # 如果答案错误，将列表中的项颜色设置为红色
            current_item.setForeground(QColor('red'))
            sender.setStyleSheet("background-color: red")
            self.option_buttons[selected_index].setStyleSheet("background-color: red")
            self.option_buttons[correct_index].setStyleSheet("background-color: green")
            # 如果答案错误，将题目添加到错误列表（如果还没有添加过）
            # 如果这个错误还没有被记录，那么添加它
            if selected_index != correct_index:
                # 确保错误记录是字典格式，并包含特定类型的错误列表
                if not isinstance(self.errors, dict):
                    self.errors = {'单选': [], '判断': []}
                error_index = question_data['序号']
                # 如果这个错误还没有被记录，那么添加它
                if error_index not in self.errors[question_type]:
                    self.errors[question_type].append(error_index)
            # error = {'type': question_type, 'index': question_data['序号']}
            # if error not in self.errors:
            #     print("error",error)
            #     self.errors.append(error)
        print("23")
        # 更新题目状态
        self.question_states[(question_type, question_index)] = {
            'type':question_type,
            'selected_index': selected_index,
            'correct_index': correct_index,
            'error': self.errors.copy()  # 存储当前的错误列表副本
        }
        print(self.question_states[question_type,question_index])

    def loadNextQuestion(self):
        try:
            self.current_question_index+=1
            next_row = self.question_list.currentRow() + 1
            if next_row < self.question_list.count():
                self.question_list.setCurrentRow(next_row)
                item = self.question_list.currentItem()
                self.displaySelectedQuestion(item)  # 确保 item 是有效的并且已被传递
            # else:
            #     print("load next else")
        except Exception as e:
            print(f"An error occurred while loading the next question: {e}")

    def submitAnswers(self):
        accuracy = 1.0
        print("errors:",self.errors)
        update_record('record.json', '团子', self.file_path, accuracy, self.errors)
        QMessageBox.information(self, "完成", "交卷成功！")

# if __name__ == '__main__':
#     import sys
#     app = QApplication(sys.argv)
#     main_app = MainApp()
#     main_app.show()
#     sys.exit(app.exec_())