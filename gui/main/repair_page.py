import sys
import json


#from gui.main.main_test import MainWindow
#from gui.login.join_membership_page import Join_mem
from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QGroupBox
from PyQt5.QtGui import *

from database.gui.user.userConnect import *

# Repair 클래스 정의
class Repair(QtWidgets.QMainWindow):
    def __init__(self):
        super(Repair, self).__init__()

        # 화면 조건
        #select_alarm = 0 # 0 : 문제 없음
        #select_alarm =  1 # 아이스크림 가져가 주세요.
        #select_alarm = 2 # 손을 가까이 하지마세요.
        select_alarm = 3 # 아이스크림 바닥의 씰을 확인해 주세요.

        pic_url = "" # "./gui/main/image/main_pic.gif"
        is_gif = False
        alarm_text = ""



        # Repair 페이지 UI 파일 로드
        self.repair = uic.loadUi("./gui/main/repair_page.ui")

               # 스택 위젯 설정
        self.stacked_widget = QtWidgets.QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)
        self.stacked_widget.addWidget(self.repair)

        if select_alarm == 1:
            alarm_text = "아이스크림이 완성되었습니다. 아이스크림을 가져가 주세요."
            pic_url = "./gui/main/image/is_ice_cream_finished.png"
            is_gif = False
            self.change_msg(alarm_text, pic_url, is_gif)
        elif select_alarm == 2:
            alarm_text = "로봇이 작동중입니다. 뒤로 물러나 주세요."
            pic_url = "./gui/main/image/is_robot_moving.gif"
            is_gif = True
            self.change_msg(alarm_text, pic_url, is_gif)
        elif select_alarm == 3:
            alarm_text = "아이스크림 바닥의 씰을 확인해 주세요."
            pic_url = "./gui/main/image/check_seal.png"
            is_gif = True
            self.change_msg(alarm_text, pic_url, is_gif)




    def change_msg(self,alarm_text, pic_url, is_gif):
        # 알림창에 글자 변경하기
        self.repair.alarm_text.setStyleSheet("QLabel { color : red; font-size: 20px; }")
        self.repair.alarm_text.setText(alarm_text)

        if is_gif :
            #gif 그림 보여주기
            # QMovie로 GIF 로드
            self.movie = QMovie(pic_url)  # 파일 경로
            self.repair.alarm_pic.setMovie(self.movie)

            # GIF 재생 속도 변경
            self.movie.setSpeed(50)

            self.movie.setCacheMode(QMovie.CacheAll)
            #self.movie.setLoopCount(5)  # 5번 반복 (0은 무한 반복)
            self.movie.setScaledSize(QSize(900, 900))  # GIF 크기 조정

            # GIF 재생 시작
            self.movie.start()
        else:
            # 사진 보여주기
            self.pixmap = QPixmap()
            self.pixmap.load(pic_url)
            scaled_pixmap = self.pixmap.scaled(1620, 690, Qt.KeepAspectRatio)
            self.repair.alarm_pic.setPixmap(scaled_pixmap)
            self.repair.alarm_pic.resize(scaled_pixmap.width(), scaled_pixmap.height())




if __name__ == "__main__":
    app = QApplication([])
    window = Repair()
    window.show()
    app.exec_()