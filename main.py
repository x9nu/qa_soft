from PyQt5.QtWidgets import QApplication
from gui import MainApp

class MainAppGUI(MainApp):
    def loadQuestions(self):
        super().loadQuestions()  # 调用 MainApp 类的 loadQuestions 方法

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    main_app = MainAppGUI()
    main_app.show()
    sys.exit(app.exec_())
