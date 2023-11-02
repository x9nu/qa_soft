from PyQt5.QtWidgets import QApplication
from gui import MainApp
from excel_processor import load_questions_from_excel
from PyQt5.QtWidgets import QFileDialog

class MainAppGUI(MainApp):
    def loadQuestions(self):
        # 打开文件对话框让用户选择题库Excel文件
        file_path, _ = QFileDialog.getOpenFileName(self, "加载题库", "", "Excel文件 (*.xlsx *.xls)")
        if file_path:
            # 使用excel_processor模块的函数来加载问题
            self.questions = load_questions_from_excel(file_path)
            # 将问题加载到界面上
            self.populateQuestionList()

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    main_app = MainAppGUI()
    main_app.show()
    sys.exit(app.exec_())
