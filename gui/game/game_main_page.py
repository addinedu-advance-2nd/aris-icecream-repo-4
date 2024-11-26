import sys
import json
import cv2

#from gui.login.join_membership_page import Join_mem
from gui.game.rps_game import RpsGame
#from gui.game.game_test import TttGame #테스트 완료하고 수정할 것
from gui.game.ttt_game import TttGame
#from gui.game.cham import Wire_loop_game

from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtCore import *
#from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QGroupBox
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from database.gui.user.userConnect import *
from database.gui.game.gameConnect import *

# Game 클래스 정의
class Game(QtWidgets.QMainWindow):
    game_rank_change = pyqtSignal()
    def __init__(self):
        super(Game, self).__init__()

        # 각 페이지 UI 파일 로드
        self.game_main = uic.loadUi("./gui/game/game_main_page.ui")
        #self.page1 = uic.loadUi("./gui/main/main_page.ui")
        #self.rps_game_page = RpsGame()
        

        # 스택 위젯 설정
        self.stacked_widget = QtWidgets.QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)
        self.stacked_widget.addWidget(self.game_main)
        #self.stacked_widget.addWidget(self.rps_game_page)

        #self.stacked_widget.addWidget(self.page1)

        #self.stacked_widget.addWidget(self.game_main)
        #self.stacked_widget.addWidget(self.page2)
        #self.stacked_widget.addWidget(self.page3)

        #버튼을 누를 경우 해당 게임으로 이동 
        self.game_main.roc_paper_scissors_start.clicked.connect(self.show_rps_game)
        self.game_main.tic_tac_toe_start.clicked.connect(self.show_ttt_game)
        #self.game_main.roc_paper_scissors_start.clicked.connect(lambda: self.open_new_window(Rps_game))
        #self.game_main.tic_tac_toe_start.clicked.connect(lambda: self.open_new_window(Ttt_game))
        #self.game_main.wire_loop_start.clicked.connect(lambda: self.open_new_window(Wire_loop_game))
        
        #틱택토 버튼을 누를 경우 해당 게임으로 이동 
        #self.game_main.tic_tac_toe_start.clicked.connect(self.show_ttt_game)

        #와이어루프 버튼을 누를 경우 해당 게임으로 이동 
        #self.game_main.wire_loop_start.clicked.connect(self.show_wire_loop_game)

        # game 메인 이미지 표시 - gif
            # QMovie로 GIF 로드
        #self.movie = QMovie("./gui/game/image/game_pic.gif")  # 파일 경로
        #self.game_main.game_pic.setMovie(self.movie)
        
        # GIF 재생 속도 변경
        #self.movie.setSpeed(50)

        #self.movie.setCacheMode(QMovie.CacheAll)
        ##self.movie.setLoopCount(5)  # 5번 반복 (0은 무한 반복)
        #self.movie.setScaledSize(QSize(675, 675))  # GIF 크기 조정

        # GIF 재생 시작
        #self.movie.start()


        # 게임 메인 - 게임 타이틀
        self.pixmap = QPixmap()
        self.pixmap.load("./gui/game/image/game_page_title.png")
        label_width = self.game_main.game_pic.width()
        label_height = self.game_main.game_pic.height()
        scaled_pixmap = self.pixmap.scaled(label_width, label_height, Qt.KeepAspectRatio)
        self.game_main.game_pic.setPixmap(scaled_pixmap)
        self.game_main.game_pic.resize(scaled_pixmap.width(), scaled_pixmap.height())

       

        # 게임 메인 - 로고
        self.pixmap = QPixmap()
        self.pixmap.load("./gui/main/image/logo_green.png")
        label_width = self.game_main.logo.width()
        label_height = self.game_main.logo.height()
        caled_pixmap = self.pixmap.scaled(label_width, label_height, Qt.KeepAspectRatio)
        self.game_main.logo.setPixmap(caled_pixmap)
        self.game_main.logo.resize(caled_pixmap.width(), self.pixmap.height())


       
 
        self.game_main.game1_frame.setStyleSheet("color: #ffffff;"
                "background-color: #ffffff;"
                "border: none;" 
                "border-style: dashed;"
                "border-width: 2px;"
                "border-radius: 10px; "
                "border-color: #299b48")
        

        self.game_main.game2_frame.setStyleSheet("color: #ffffff;"
                "background-color: #ffffff;"
                "border-style: dashed;"
                "border-width: 2px;"
                "border-radius: 10px; "
                "border-color: #299b48")


        self.game_main.roc_paper_scissors_start.setStyleSheet("""
            QPushButton {
                background-color: #178f01;  /* 초록색 배경 */
                color: black;               /* 텍스트 흰색 */
                font-size: 30px;            /* 글자 크기 */
                border-radius: 15px;       /* 둥근 모서리 */
            }
            QPushButton:hover {
                background-color: #299b48; /* 호버 상태 색상 */
            }
            QPushButton:pressed {
                background-color: #4a6d42; /* 클릭 상태 색상 */
            }
        """)  #게임 선택 버튼 스타일 변경




        self.game_main.tic_tac_toe_start.setStyleSheet("""
            QPushButton {
                background-color: #178f01;  /* 초록색 배경 */
                color: black;               /* 텍스트 흰색 */
                font-size: 30px;            /* 글자 크기 */
                border-radius: 15px;       /* 둥근 모서리 */
            }
            QPushButton:hover {
                background-color: #299b48; /* 호버 상태 색상 */
            }
            QPushButton:pressed {
                background-color: #4a6d42; /* 클릭 상태 색상 */
            }
        """)  #게임 선택 버튼 스타일 변경


        """RANK 랭킹테이블 (가위바위보)"""
        #print(selectTotalRank("5"))# 전체 게임(취합) 랭킹 취합
        #print(selectGameByRank("1", "5")) #게임별 랭킹
        self.game_main.rank_table1 = self.game_main.findChild(QtWidgets.QTableWidget, "rank_table1")
      
        
          
        self.game_main.rank_table1.setStyleSheet("color: #000000;"
                        "background-color: #ffffff;"
                        "border-style: dashed;"
                        "border-width: 2px;"
                        "font-size: 20px;"
                        "border-radius: 10px; "
                        "border-color: #fea443")
        
        totalRankList =  selectGameByRank("0","10")
       
        tmp_idx  = 0
        for rowData in totalRankList :
            tmp_idx+=1
            row = self.game_main.rank_table1.rowCount()   
            self.game_main.rank_table1.insertRow(row)              
            self.game_main.rank_table1.setItem(row, 0, QTableWidgetItem(str(tmp_idx)+"위"))
            self.game_main.rank_table1.setItem(row, 1, QTableWidgetItem(str(rowData[1])))
            self.game_main.rank_table1.setItem(row, 2, QTableWidgetItem(str(rowData[4])+"점"))


            self.game_main.rank_table1.setColumnWidth(0, 100)
            self.game_main.rank_table1.setColumnWidth(1, 170)
            self.game_main.rank_table1.setColumnWidth(2, 150)   
 
    
     
        """RANK 랭킹테이블 (틱택토)"""   

        self.game_main.rank_table2 = self.game_main.findChild(QtWidgets.QTableWidget, "rank_table2")
        
        self.game_main.rank_table2.setStyleSheet("color: #000000;"
                        "background-color: #ffffff;"
                        "border-style: dashed;"
                        "border-width: 2px;"
                        "font-size: 20px;"
                        "border-radius: 10px; "
                        "border-color: #fea443")
        
       
        
            
        totalRankList =  selectGameByRank("1","10")
       
        tmp_idx  = 0
        for rowData in totalRankList :
            tmp_idx+=1
            row = self.game_main.rank_table2.rowCount()   
            self.game_main.rank_table2.insertRow(row)              
            self.game_main.rank_table2.setItem(row, 0, QTableWidgetItem(str(tmp_idx)+"위"))
            self.game_main.rank_table2.setItem(row, 1, QTableWidgetItem(str(rowData[1])))
            self.game_main.rank_table2.setItem(row, 2, QTableWidgetItem(str(rowData[4])+"점"))


            self.game_main.rank_table2.setColumnWidth(0, 100)
            self.game_main.rank_table2.setColumnWidth(1, 170)
            self.game_main.rank_table2.setColumnWidth(2, 150)   
 


        #이전 버튼을 누를 경우 창 닫기
        self.game_main.back.clicked.connect(self.close_window)

        # 점수 전달 형식 : game_result = [user_id, user_code, game_num, score]
        self.game_result = [None, None, None ,None]
        # id 읽어오기
        with open('./gui/login/label_text.txt', 'r') as file:
            file_content = file.read()
            content = json.loads(file_content)
           
            #사용자 ID
            global global_user_id
            global_user_id = content["id"]            
            self.game_result[0] = global_user_id

            #사용자 코드
            global global_user_code
            global_user_code = content["userCode"]
            
            self.game_result[0] = global_user_id
            self.game_result[1] = str(global_user_code)
            
            print("사용자 ID :" + self.game_result[0]+"//"+"사용자 CODE :" + self.game_result[1])

    def update_score(self, game_num, score):
        # game_result에 점수 저장
        self.game_result[2] = game_num  # 게임 번호 (예: 0 - RPS, 1 - TTT)
        self.game_result[3] = score     # 점수     
        insertGamePlayInfo(game_num, score, self.game_result[1])  
        print(f"점수 업데이트: {self.game_result}")
     


    def open_new_window(self, class_name):
        #self.new_window = class_name
        # 창을 최대화된 상태로 표시
        self.new_window = class_name()
        self.new_window.showMaximized()

    def show_rps_game(self):
        #self.game_main.close()
        self.rps_game_page = RpsGame()
        self.stacked_widget.addWidget(self.rps_game_page)
        self.stacked_widget.setCurrentWidget(self.rps_game_page)
        #self.game_main.close()
        # 게임 끝났을 때 점수 업데이트 시그널 연결
        self.rps_game_page.game_finished.connect(self.update_score_rps)
        # 이전 페이지 버튼 누르면 시그널 연결
        self.rps_game_page.goto_main_page.connect(self.close_window)

    def show_ttt_game(self):
        self.ttt_game_page = TttGame()
        self.stacked_widget.addWidget(self.ttt_game_page)
        self.stacked_widget.setCurrentWidget(self.ttt_game_page)
        # 게임 끝났을 때 점수 업데이트 시그널 연결
        self.ttt_game_page.game_finished.connect(self.update_score_ttt)
         # 이전 페이지 버튼 누르면 시그널 연결
        self.ttt_game_page.goto_main_page.connect(self.close_window)

    def update_score_rps(self, score):
        # RPS 게임이 끝나면 점수 업데이트
        self.update_score(0, score)

    def update_score_ttt(self, score):
        # TTT 게임이 끝나면 점수 업데이트
        self.update_score(1, score)
        

    def close_window(self):
        #self.stacked_widget.setCurrentWidget(self.page1)
        #self.game_main.close()
        #self.game_main.stop()
        self.parent().setCurrentIndex(0)
        QTimer.singleShot(100, self.game_rank_re)  # 1000ms 지연

    def game_rank_re(self):
        self.game_rank_change.emit()



    '''
    # 가위바위보 게임 열기
    def show_rps_game(self):
        self.rsp_window = Rps_game()
        self.rsp_window.showMaximized()
        self.rsp_window.show()

    # 틱택토 게임 열기
    def show_ttt_game(self):
        self.ttt_window = Ttt_game()
        self.ttt_window.showMaximized()
        self.ttt_window.show()

    # 와이어루프 게임 열기
    def show_wire_loop_game(self):
        self.wire_loop_window = Wire_loop_game()
        self.wire_loop_window.showMaximized()
        self.wire_loop_window.show()
    '''



if __name__ == "__main__":
    app = QApplication([])
    window = Game()
    window.show()
    app.exec_()