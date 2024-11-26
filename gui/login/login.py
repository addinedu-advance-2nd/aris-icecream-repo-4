import sys
import json


#from gui.main.main_test import MainWindow
from gui.login.join_membership_page import Join_mem
from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QGroupBox
from PyQt5.QtGui import *

from database.gui.user.userConnect import *

# Login 클래스 정의
class Login(QtWidgets.QMainWindow):
    login_button_change = pyqtSignal()
    def __init__(self):
        super(Login, self).__init__()

        # 각 페이지 UI 파일 로드
        self.login = uic.loadUi("./gui/login/login.ui")
        self.login.setStyleSheet("QMainWindow {background: 'white';}")
        #self.page1 = MainWindow
        #self.join_mem = Join_mem


        #page1 logo 그림 표시
        self.pixmap = QPixmap()
        self.pixmap.load("./gui/main/image/logo_green.png")
        label_width = self.login.logo.width()
        label_height = self.login.logo.height()
        caled_pixmap = self.pixmap.scaled(label_width, label_height, Qt.KeepAspectRatio)
        self.login.logo.setPixmap(caled_pixmap)
        self.login.logo.resize(caled_pixmap.width(), self.pixmap.height())

        # 스택 위젯 설정
        self.stacked_widget = QtWidgets.QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)
        self.stacked_widget.addWidget(self.login)


         # 페이지 전환을 위한 버튼 클릭 이벤트 설정
        #self.login.join_membership_button.clicked.connect(self.show_join_mem)
        self.login.join_membership_button.clicked.connect(self.open_new_window)
        self.login.home_button.clicked.connect(self.close_window)

        # 이전 페이지 버튼 누르면 시그널 연결
        #self.join_mem = Join_mem()
        #self.join_mem.goto_main_page.connect(self.close_window)

        #id_text = self.login.id.text()
        #USER_ID = id_text      

        #로그인 버튼을 누를 경우 ID,PW 출력 후 page1로 이동 
        self.login.log_in_button.setDefault(True)  # 기본 엔터 버튼 설정
        self.login.log_in_button.clicked.connect(self.collect_data)

        # pw 입력창에 글자 입력 후 엔터 치면 page1로 이동
        self.login.pw.returnPressed.connect(self.on_enter_pressed)


    def on_enter_pressed(self):
        self.login.log_in_button.click()

    def collect_data(self):
        id_text = self.login.id.text()
        pw_text = self.login.pw.text()


        self.id_pw = [id_text, pw_text]

        print(self.id_pw)     
        loginInfo = {}
        loginInfo['id'] = id_text
        loginInfo['pw'] = pw_text
        
        result = checkLogin(loginInfo)
        QtWidgets.QMessageBox.information(self, '회원가입', result['msg'])
        if('성공' in result['msg']):   
          userInfoJson = {'id':loginInfo['id'], 'userCode' : result['userCode'], 'auth' : result['auth']}
          print(userInfoJson)
          with open('./gui/login/label_text.txt', 'w') as file:
            #file.write(USER_ID)  # 텍스트 파일에 저장
            file.write(json.dumps(userInfoJson))
          #self.update_main_page()
          
          self.login.id.setText("")
          self.login.pw.setText("")
          self.login_button_change.emit()
          self.parent().setCurrentIndex(0)

    def open_next_window(self):
        # 입력 필드의 텍스트를 다음 창으로 전달
        text = self.login.id.text()
        self.page1.set_label_text(text)
        self.page1.show()

    def save_label_to_file(self):
        label_text = self.login.id.text()  # QLabel의 텍스트 가져오기
        with open('./gui/login/label_text.txt', 'w') as file:
            file.write(label_text)  # 텍스트 파일에 저장

    def update_main_page(self):
        self.parent().parent().update_label("Updated from Secondary Page")
        self.close()
          
          
     
    def open_new_window(self):
        self.join_page = Join_mem()
        self.stacked_widget.addWidget(self.join_page)
        self.stacked_widget.setCurrentWidget(self.join_page)
        self.join_page.goto_main_page.connect(self.close_window)


        # 창을 최대화된 상태로 표시
        #self.new_window.showMaximized()
        #self.new_window.show()

    def close_window(self):
        #self.stacked_widget.setCurrentWidget(self.page1)
        #self.game_main.close()
        #self.game_main.stop()
        self.stacked_widget.setCurrentWidget(self.login)
        self.parent().setCurrentIndex(0)



if __name__ == "__main__":
    app = QApplication([])
    window = Login()
    window.show()
    app.exec_()