import sys

from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QGroupBox
from PyQt5.QtGui import *

from database.gui.user.userConnect import *

# MainWindow 클래스 정의
class Join_mem(QtWidgets.QMainWindow):
    goto_main_page = pyqtSignal()  # 앞 페이지의 함수를 호출하기 위한 시그널

    def __init__(self):

        super(Join_mem, self).__init__()

        # 각 페이지 UI 파일 로드
        self.join_mem = uic.loadUi("./gui/login/join_membership_page.ui")
        self.join_mem.setStyleSheet("QMainWindow {background: 'white';}")
        #self.join_mem = Join_mem

             #page1 logo 그림 표시
        self.pixmap = QPixmap()
        self.pixmap.load("./gui/main/image/logo_green.png")
        label_width = self.join_mem.logo.width()
        label_height = self.join_mem.logo.height()
        caled_pixmap = self.pixmap.scaled(label_width, label_height, Qt.KeepAspectRatio)
        self.join_mem.logo.setPixmap(caled_pixmap)
        self.join_mem.logo.resize(caled_pixmap.width(), self.pixmap.height())

        # 스택 위젯 설정
        self.stacked_widget = QtWidgets.QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)
        self.stacked_widget.addWidget(self.join_mem)

        #가입 완료 버튼을 누를 경우 ID,PW 출력 후 login 페이지로 이동 
        self.join_mem.sing_up_complete.clicked.connect(self.collect_data)

        # 화면 닫기 버튼을 누를 경우 홈페이지로 이동
        self.join_mem.home_button.clicked.connect(self.trigger_front_function)

    def collect_data(self):
        name_text = self.join_mem.name.text()
        id_text = self.join_mem.id.text()
        pw_text = self.join_mem.pw.text()
        pw_re_text = self.join_mem.pw_re.text()
        name_text = self.join_mem.name.text()
        tel_text = self.join_mem.tel.text()
        email_text = self.join_mem.email.text()

        self.member_information = [id_text, pw_text,pw_re_text, name_text, tel_text, email_text]
        #print(self.member_information)
        if(pw_text != pw_re_text):
            # About 버튼 클릭 이벤트
            QtWidgets.QMessageBox.information(self, '회원가입', '비밀번호가 일치하지 않습니다.')
        elif (tel_text.isnumeric() == False) :
            QtWidgets.QMessageBox.information(self, '회원가입', '전화번호는 숫자만 입력해주세요.')
        else:
            result = insertSignUp(self.member_information)
            print(result['msg'])
            QtWidgets.QMessageBox.information(self, '회원가입', result['msg'])
            if '성공' in result['msg']:
                self.close()
                self.goto_main_page.emit()

    def trigger_front_function(self):
        """앞 페이지로 시그널 송출"""
        self.goto_main_page.emit()
       
      

if __name__ == "__main__":
    app = QApplication([])
    window = Join_mem()
    window.show()
    app.exec_()