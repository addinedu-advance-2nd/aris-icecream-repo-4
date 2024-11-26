# 경로 설정 터미널 창에 다음 입력 : export PYTHONPATH="${PYTHONPATH}:/home/abcd/Documents/GitHub/aris-repo-4"
# mysql 설치 : pip install mysql-connector-python


import sys
import json
from tokenize import String
import rclpy as rp

from admin_page import AdminPage
from gui.login.login import Login
from pinger_mouse import Pinger_mouse
from gui.game.game_main_page import Game
from gui.game.rps_game import RpsGame


from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
#from std_msgs.msg import String
from robot_msgs.msg import UserOrder
from robot_msgs.msg import RobotState

from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtCore import *
#from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QGroupBox
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from database.gui.sales.salesConnect import *
from database.gui.inventory.inventoryConnect import *
from database.gui.game.gameConnect import *

#전역변수
#사용자 코드
global_user_code = "-"
#사용자 ID
global_user_id = "-"
#관리자 여부
global_user_auth = "-"

        
        
        

'''     
        
# Order_ice_cream 클래스 정의
class Order_ice_cream(Node):
    def __init__(self):
        super().__init__('Order_ice_cream')
        self.publisher_ = self.create_publisher(String, 'order', 10)

    def publish_message(self):
        msg = String()
        msg.data = 'Hello, ROS 2!'
        self.get_logger().info(f'Publishing: "{msg.data}"')
        self.publisher_.publish(msg)
'''
#ros2 토픽 정의        
class RobotStateSubscriber(Node, QObject):
    msg_received = pyqtSignal(list)

    def __init__(self):
        Node.__init__(self, 'robot_state_subscriber_UI')
        QObject.__init__(self)

        self.subscription = self.create_subscription(RobotState, '/robot_state', self.robot_state_sub_callback, 10)
        self.subscription
    
    def robot_state_sub_callback(self, msg):
        temperature_list = list(msg.temperatures)
        self.msg_received.emit(temperature_list)

class Ros2ExecutorThread(QThread):
    def __init__(self):
        super().__init__()
        self.executor = MultiThreadedExecutor()
        self.robot_state_subscriber = RobotStateSubscriber()
        self.executor.add_node(self.robot_state_subscriber)
    
    def run(self):
        
        self.executor.spin()
    
    def stop(self):
        self.executor.shutdown()
        

class DynamicButtonWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('DB에서 동적으로 버튼 생성')
        self.setGeometry(50, 300, 1700, 500)

        # 버튼들을 관리할 리스트
        self.ice_button_buttons = []
        self.topping = []
        self.topping_type = []

        # DB에서 가져온 예시 데이터 (버튼 이름들)
        button_groups = {
            1: selectSaleIceCream(),  # 그룹 1
            2: selectSaleTopping(),  # 그룹 2
            3: ['Middle', 'Bottom']  # 그룹 3
        }

        # 페이지 2의 레이아웃 생성
        self.page_layout = QHBoxLayout(self)
        
        # 기존의 버튼들을 모두 제거
        #self.remove_all_buttons()

        # 각 그룹을 반복하면서 버튼 그룹을 생성
        for group_id, buttons in button_groups.items():
            
            # 각 그룹에 대해 그룹 박스를 생성
            group_box = QGroupBox()
            group_layout = QVBoxLayout()
            
            # 버튼을 생성하여 레이아웃에 추가
            for button_name in buttons:
                button = QPushButton(button_name)
                num_items = len(buttons)
                if num_items in (1, 2, 3):
                    global result
                    result = 120
                elif num_items == 4:
                    result = 100
                elif num_items == 5:
                    result = 80

                button.setFixedSize(200, result)
                group_layout.addWidget(button, alignment=Qt.AlignCenter)
                button.setObjectName(f"{button_name.lower()}_button")
                
                if group_id == 1:
                    self.ice_button_buttons.append(button)
                elif group_id == 2:
                    self.topping.append(button)
                elif group_id == 3:
                    self.topping_type.append(button)
                
                button.clicked.connect(lambda _, b=button_name: self.on_button_click(b))  # 버튼 클릭 시 이벤트 연결
            
            group_box.setLayout(group_layout)
            group_box.setStyleSheet("color: #ffffff;"
                "background-color: #ffffff;"
                "border-style: dashed;"
                "border-width: 2px;"
                "border-radius: 10px; "
                "border-color: #299b48")
                
            self.page_layout.addWidget(group_box)

        self.setLayout(self.page_layout)

    def remove_all_buttons(self):
        print("저장된 모든 버튼을 제거하고 레이아웃에서 삭제")
        for button in self.ice_button_buttons:
            self.page_layout.removeWidget(button)
            button.deleteLater()
        self.ice_button_buttons.clear()

        for button in self.topping:
            self.page_layout.removeWidget(button)
            button.deleteLater()
        self.topping.clear()

        for button in self.topping_type:
            self.page_layout.removeWidget(button)
            button.deleteLater()
        self.topping_type.clear()


    def on_button_click(self, button_name):
        print(f"클릭된 버튼: {button_name}")
        #self.sender().setStyleSheet("background-color: red;")

    

# MainWindow 클래스 정의
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        rp.init()
        self.node = rp.create_node('ice_cream_selector')
        self.publisher = self.node.create_publisher(UserOrder, '/user_order',10)
        self.executor_thread = Ros2ExecutorThread()
        self.executor_thread.robot_state_subscriber.msg_received.connect(self.update_state)
        self.executor_thread.start()

        # 각 페이지 UI 파일 로드
        self.page1 = uic.loadUi("./gui/main/main_page.ui")
        self.page2 = uic.loadUi("./gui/main/select_ice_cream_page.ui")
        self.page3 = uic.loadUi("./gui/main/payment_information_page.ui")
        self.page4 = uic.loadUi("./gui/main/wait_page_page.ui")
        #self.page5 = AdminPage()
        #self.rps_game_page = RpsGame()
        self.login_page = Login()

        self.ice_cream_selected = None
        self.topping_selected = []
        self.method_selected = None

        # 파일명만 안 보이게 하기 위해 제목을 빈 문자열로 설정
        self.setWindowTitle(" ")  # 제목을 빈 문자열로 설정

        # 스택 위젯 설정
        self.stacked_widget = QtWidgets.QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)

        self.stacked_widget.addWidget(self.page1)
        self.stacked_widget.addWidget(self.page2)
        self.stacked_widget.addWidget(self.page3)
        self.stacked_widget.addWidget(self.page4)
        #self.stacked_widget.addWidget(self.page5)  # 관리자 페이지
        self.stacked_widget.addWidget(self.login_page)  #로그인 페이지

        #주문 선택 버튼 비활성화
        self.page2.select_complete.setEnabled(False)

        #배경색 변경
        self.page1.setStyleSheet("QMainWindow {background: 'white';}")
        self.page3.setStyleSheet("QMainWindow {background: 'white';}")
        self.page4.setStyleSheet("QMainWindow {background: 'white';}")


        #버튼 디자인 효과
        self.page1.select_ice_cream_button.setStyleSheet("""
            QPushButton {
                background-color: #178f01;  /* 초록색 배경 */
                color: white;               /* 텍스트 흰색 */
                font-size: 30px;            /* 글자 크기 */
                border-radius: 15px;       /* 둥근 모서리 */
            }
            QPushButton:hover {
                background-color: #299b48; /* 호버 상태 색상 */
            }
            QPushButton:pressed {
                background-color: #4a6d42; /* 클릭 상태 색상 */
            }
        """)  # 아이스크림 선택 버튼 스타일 변경



        self.page1.select_game.setStyleSheet("""
            QPushButton {
                background-color: #178f01;  /* 초록색 배경 */
                color: white;               /* 텍스트 흰색 */
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


        self.page1.log_in_button.setStyleSheet("""
            QPushButton {
                background-color: #b2d761;  /* 초록색 배경 */
                color: white;               /* 텍스트 흰색 */
                font-size: 13px;            /* 글자 크기 */
                border-radius: 5px;       /* 둥근 모서리 */
            }
            QPushButton:hover {
                background-color: #299b48; /* 호버 상태 색상 */
            }
            QPushButton:pressed {
                background-color: #4a6d42; /* 클릭 상태 색상 */
            }
        """)  #로그인/로그아웃 선택 버튼 스타일 변경

        #버튼 글꼴 변경
        font = QFont("Ubuntu", 30, QFont.Bold)  # Arial, 크기 14, 굵게
        self.page1.select_ice_cream_button.setFont(font)
        self.page1.select_game.setFont(font)
      

        #page1 logo 그림 표시
        self.pixmap = QPixmap()
        self.pixmap.load("./gui/main/image/logo_green.png")
        label_width = self.page1.logo.width()
        label_height = self.page1.logo.height()
        caled_pixmap = self.pixmap.scaled(label_width, label_height, Qt.KeepAspectRatio)
        self.page1.logo.setPixmap(caled_pixmap)
        self.page1.logo.resize(caled_pixmap.width(), self.pixmap.height())

        # page1 게임 타이틀 이미지 표시
        self.pixmap = QPixmap()
        self.pixmap.load("./gui/main/image/gameRankTitle.png")
        label_width = self.page1.game_rank_title.width()
        label_height = self.page1.game_rank_title.height()
        scaled_pixmap = self.pixmap.scaled(label_width, label_height, Qt.KeepAspectRatio)
        self.page1.game_rank_title.setPixmap(scaled_pixmap)     
        
        #page2 - 주문하기 logo 그림 표시
        self.pixmap = QPixmap()
        self.pixmap.load("./gui/main/image/logo_green.png")
        label_width = self.page2.logo.width()
        label_height = self.page2.logo.height()
        caled_pixmap = self.pixmap.scaled(label_width, label_height, Qt.KeepAspectRatio)
        self.page2.logo.setPixmap(caled_pixmap)
        self.page2.logo.resize(caled_pixmap.width(), self.pixmap.height())



       #page3 - 결제 logo 그림 표시
        self.pixmap = QPixmap()
        self.pixmap.load("./gui/main/image/logo_green.png")
        label_width = self.page3.logo.width()
        label_height = self.page3.logo.height()
        caled_pixmap = self.pixmap.scaled(label_width, label_height, Qt.KeepAspectRatio)
        self.page3.logo.setPixmap(caled_pixmap)
        self.page3.logo.resize(caled_pixmap.width(), self.pixmap.height())
 


       #page4 - 웨이팅 페이지 logo 그림 표시
        self.pixmap = QPixmap()
        self.pixmap.load("./gui/main/image/logo_green.png")
        label_width = self.page4.logo.width()
        label_height = self.page4.logo.height()
        caled_pixmap = self.pixmap.scaled(label_width, label_height, Qt.KeepAspectRatio)
        self.page4.logo.setPixmap(caled_pixmap)
        self.page4.logo.resize(caled_pixmap.width(), self.pixmap.height())
        self.page1.game_rank_title.resize(scaled_pixmap.width(), scaled_pixmap.height())



        '''
        # page1 메인 이미지 표시
        self.pixmap = QPixmap()
        self.pixmap.load("./gui/main/image/main_pic.png")
        label_width = self.page1.main_pic.width()
        label_height = self.page1.main_pic.height()
        scaled_pixmap = self.pixmap.scaled(label_width, label_height, Qt.KeepAspectRatio)
        self.page1.main_pic.setPixmap(scaled_pixmap)
        self.page1.main_pic.resize(scaled_pixmap.width(), scaled_pixmap.height())
        '''

        # page1 메인 이미지 표시 - gif
            # QMovie로 GIF 로드
        self.movie = QMovie("./gui/main/image/main_pic.gif")  # 파일 경로
        self.page1.main_pic.setMovie(self.movie)

        # GIF 재생 속도 변경
        self.movie.setSpeed(50)

        self.movie.setCacheMode(QMovie.CacheAll)
        #self.movie.setLoopCount(5)  # 5번 반복 (0은 무한 반복)
        self.movie.setScaledSize(QSize(900, 900))  # GIF 크기 조정

        # GIF 재생 시작
        self.movie.start()

        # page43 이미지 표시
        self.pixmap = QPixmap()
        self.pixmap.load("./gui/main/image/main_pic.png")
        scaled_pixmap = self.pixmap.scaled(1620, 690, Qt.KeepAspectRatio)
        self.page3.last_pic.setPixmap(scaled_pixmap)
        self.page3.last_pic.resize(scaled_pixmap.width(), scaled_pixmap.height())

        # page4 이미지 표시
        self.pixmap = QPixmap()
        self.pixmap.load("./gui/main/image/last_pic.png")
        scaled_pixmap = self.pixmap.scaled(1620, 690, Qt.KeepAspectRatio)
        self.page4.last_pic.setPixmap(scaled_pixmap)
        self.page4.last_pic.resize(scaled_pixmap.width(), scaled_pixmap.height())
        
        # 페이지 전환을 위한 버튼 클릭 이벤트 설정
        self.page1.select_ice_cream_button.clicked.connect(self.show_page2)
        self.page2.back_button.clicked.connect(self.show_page1)
        self.page2.select_complete.clicked.connect(self.show_page3)
        self.page3.back_button.clicked.connect(self.show_page2)
        self.page1.log_in_button.clicked.connect(self.show_login_page)
        self.page1.select_game.clicked.connect(self.show_game_page)



        """RANK 랭킹테이블 """
        self.game_rank_view()
        #print(selectTotalRank("5"))# 전체 게임(취합) 랭킹 취합
        #print(selectGameByRank("1", "5")) #게임별 랭킹
        '''
        self.rank_table = self.page1.findChild(QtWidgets.QTableWidget, "rank_table")
        
        self.rank_table.setStyleSheet("color: #ffffff;"
                        "background-color: #f9da4a;"
                        "border-style: dashed;"
                        "border-width: 2px;"
                        "border-radius: 10px; "
                        "border-color: #fea443")
        
       
        
            
        totalRankList =  selectTotalRank("5")

        #item1 = self.rank_table.horizontalHeaderItem(0)
        #item2 = self.rank_table.horizontalHeaderItem(1)
      
        #item1.setBackground(QtGui.QColor(132, 0, 224))
        #item2.setBackground(QtGui.QColor(132, 0, 224))
      
        #self.rank_table.setHorizontalHeaderItem(0, item1)
        #self.rank_table.setHorizontalHeaderItem(1, item2)        
        tmp_idx  = 0
        for rowData in totalRankList :
            tmp_idx+=1
            row = self.rank_table.rowCount()   
            self.rank_table.insertRow(row)              
            self.rank_table.setItem(row, 0, QTableWidgetItem(str(tmp_idx)+"위"))
            self.rank_table.setItem(row, 1, QTableWidgetItem(str(rowData[1])))
            self.rank_table.setItem(row, 2, QTableWidgetItem(str(rowData[4])+"점"))
            
          
        self.rank_table.resizeColumnsToContents()

        '''
        
        
        
        # 다음 페이지로 이동하도록 타이머 설정
        self.timer_1 = QtCore.QTimer(self)
        self.timer_1.setSingleShot(True)
        self.timer_1.timeout.connect(self.show_page4)

        self.timer_2 = QtCore.QTimer(self)
        self.timer_2.setSingleShot(True)
        self.timer_2.timeout.connect(self.show_page1)  
        
         
        
        # 페이지 전환 버튼 연결 (예시로 이미지 클릭 시 다른 페이지로 이동)
        self.page1.logo.mouseDoubleClickEvent = self.on_image_click


        # 창을 최대화된 상태로 표시
        self.showMaximized()
        self.load_text_from_file()

        # 파일 시스템 감시기 초기화
        self.file_watcher = QFileSystemWatcher()
        
        # 감시할 파일 경로 설정
        self.file_path = './gui/login/label_text.txt'  # 모니터링할 파일 경로
        
        # 파일 변경 시 호출될 함수 연결
        self.file_watcher.fileChanged.connect(self.update_label_from_file)
        
        # 파일 감시 시작
        self.file_watcher.addPath(self.file_path)

        # 계속해서 감시할 수 있도록 설정
        self.file_watcher.addPath(self.file_path)  # 계속해서 파일을 감시하도록 추가

        # 초기 상태 설정
        self.is_logged_in = False
        self.toggle_login()

        # 페이지 추가
        #self.game = Game()
        #self.rps_game = RpsGame()

        # 시그널/슬롯 연결
        #self.rps_game.goto_main_page.connect(self.game.close_window)
        #self.stacked_widget.addWidget(self.game)
        #self.stacked_widget.addWidget(self.rps_game)

    def game_rank_view(self):
        """RANK 랭킹테이블 """
        #print(selectTotalRank("5"))# 전체 게임(취합) 랭킹 취합
        #print(selectGameByRank("1", "5")) #게임별 랭킹
        self.rank_table = self.page1.findChild(QtWidgets.QTableWidget, "rank_table")
        # 테이블 초기화 (기존 데이터 삭제)
        self.rank_table.setRowCount(0)

        
        self.rank_table.setStyleSheet("color: #ffffff;"
                        "background-color: #f9da4a;"
                        "border-style: dashed;"
                        "border-width: 2px;"
                        "border-radius: 10px; "
                        "border-color: #fea443")
        
       
        
        totalRankList =[]
        totalRankList =  selectTotalRank("5")
        #print("전체 랭킹 값", totalRankList)

        #item1 = self.rank_table.horizontalHeaderItem(0)
        #item2 = self.rank_table.horizontalHeaderItem(1)
      
        #item1.setBackground(QtGui.QColor(132, 0, 224))
        #item2.setBackground(QtGui.QColor(132, 0, 224))
      
        #self.rank_table.setHorizontalHeaderItem(0, item1)
        #self.rank_table.setHorizontalHeaderItem(1, item2)        

        tmp_idx  = 0
        for rowData in totalRankList :
            tmp_idx+=1
            row = self.rank_table.rowCount()   
            self.rank_table.insertRow(row)              
            self.rank_table.setItem(row, 0, QTableWidgetItem(str(tmp_idx)+"위"))
            #self.rank_table.setItem(row, 0, "위")
            self.rank_table.setItem(row, 1, QTableWidgetItem(str(rowData[1])))
            self.rank_table.setItem(row, 2, QTableWidgetItem(str(rowData[4])+"점"))

          
        self.rank_table.resizeColumnsToContents()



    def toggle_login(self):
        """로그인 상태 변경 및 버튼 텍스트 업데이트"""
        self.is_logged_in = not self.is_logged_in
        if self.is_logged_in:
            self.page1.log_in_button.setText("로그아웃")
        else:
            self.page1.log_in_button.setText("로그인")




        # mouseDoubleClickEvent를 재정의하여 로고 더블클릭 시 이벤트 처리
    def mouseDoubleClickEvent(self, event):
        # 더블클릭이 로고에서 발생한 경우에만 처리
        #if event.source() == self.page1.logo:
            print("로고 클릭! 관리자 페이지로 전환합니다.")
           # self.show_page5()  # 관리자 페이지로 전환     

        
    def add_image_to_label(self, pic_link, graphics_view):
        # QGraphicsView에 이미지를 로드하고 자동으로 크기를 조정
        scene = QtWidgets.QGraphicsScene(self)
        pixmap = QtGui.QPixmap(pic_link)
        if not pixmap.isNull():  # 이미지가 유효한지 확인
            item = scene.addPixmap(pixmap)
            graphics_view.setScene(scene)
            graphics_view.setRenderHint(QtGui.QPainter.Antialiasing)
            graphics_view.setRenderHint(QtGui.QPainter.SmoothPixmapTransform)
            graphics_view.setAlignment(QtCore.Qt.AlignCenter)
            self.fit_image_to_graphics_view(graphics_view, item)
        else:
            print("이미지를 로드할 수 없습니다:", pic_link)

    def fit_image_to_graphics_view(self, graphics_view, pixmap_item):
        # QGraphicsView의 크기에 맞춰 이미지를 비율에 맞게 조정
        graphics_view.fitInView(pixmap_item, QtCore.Qt.KeepAspectRatio)
        #최소 크기 설정 및 이미지 확대
        min_size = 500 # 최소 크기 지정
        view_rect = graphics_view.rect()

            # fitInView 사용 후, 크기가 너무 작으면 scale을 사용하여 이미지 크기 확대
        graphics_view.fitInView(pixmap_item, QtCore.Qt.KeepAspectRatio)
        if pixmap_item.pixmap().width() < min_size or pixmap_item.pixmap().height() < min_size:
            scale_factor = max(min_size / pixmap_item.pixmap().width(), min_size / pixmap_item.pixmap().height())
            graphics_view.scale(scale_factor, scale_factor)
    
    def on_image_click(self, event):
        # 이미지 더블클릭 시 관리자 페이지로 전환
        print("Logo clicked! Switching to AdminPage.")
        if str(global_user_auth) == 'Y' :
            self.page5 = AdminPage()
            self.stacked_widget.setCurrentWidget(self.page5)
        else : 
            QtWidgets.QMessageBox.information(self, '관리자 페이지 접속', "관리자페이지 접속 권한이 없습니다.")
    
    
    '''
    def resizeEvent(self, event):
        # 창 크기가 변경될 때마다 각 QGraphicsView의 이미지 크기 자동 조정
        for page, view_attr in [(self.page1, 'logo'), (self.page1, 'main_pic'), (self.page4, 'last_pic')]:
            graphics_view = getattr(page, view_attr, None)
            if graphics_view and graphics_view.scene():
                pixmap_item = graphics_view.scene().items()[0]
                self.fit_image_to_graphics_view(graphics_view, pixmap_item)
        super().resizeEvent(event)
        '''
        

    def setup_button_group(self, buttons, selected_color, multi_select):
        for button in buttons:
            button.setStyleSheet("background-color: white; color: black;")
            button.clicked.connect(lambda _, btn=button: self.select_button(buttons, btn, selected_color, multi_select))

    def select_button(self, button_group, selected_button, color, multi_select):
        if not multi_select:
            for button in button_group:
                button.setStyleSheet("background-color: white; color: black;")
        
        current_color = selected_button.styleSheet()
        selected_button.setStyleSheet(
            f"background-color: white; color: black;" if "background-color: " + color in current_color else f"background-color: {color}; color: black;"
        )
        self.update_selection(button_group, selected_button)
        self.check_selection_complete()


    def update_selection(self, button_group, selected_button):
        # 선택 상태를 업데이트
        if button_group == self.ice_cream_buttons:
            self.ice_cream_selected = selected_button.text()  # 예: "초코 아이스크림"
        elif button_group == self.topping_buttons:
            if selected_button.text() in self.topping_selected:
                self.topping_selected.remove(selected_button.text())
                selected_button.setStyleSheet("background-color: white; color: black;")
            else:
                self.topping_selected.append(selected_button.text())
                selected_button.setStyleSheet("background-color: orange; color: black;")
            # self.topping_selected = selected_button.text()    # 예: "초코볼"
        elif button_group == self.method_buttons:
            self.method_selected = selected_button.text()     # 예: "가운데"
        print(self.ice_cream_selected, self.topping_selected, self.method_selected)

    def reset_button_colors(self):
        # 모든 선택 버튼 색상 초기화 및 'select_complete' 비활성화
        for button in self.ice_cream_buttons + self.topping_buttons + self.method_buttons:
        #for button in self.ice_cream_buttons + self.method_buttons:
            button.setStyleSheet("background-color: white; color: black;")
        self.page2.select_complete.setEnabled(False)
        self.ice_cream_selected = None
        self.topping_selected = []
        self.method_selected = None


    def check_selection_complete(self):
        # 모든 그룹의 선택 상태 확인
        ice_cream_selected = any(button.styleSheet() == "background-color: magenta; color: black;" for button in self.ice_cream_buttons)
        topping_selected = any(button.styleSheet() == "background-color: orange; color: black;" for button in self.topping_buttons)
        method_selected = any(button.styleSheet() == "background-color: cyan; color: black;" for button in self.method_buttons)

        # 모든 그룹이 선택되었을 때 'select_complete' 버튼 활성화
        self.page2.select_complete.setEnabled(ice_cream_selected and topping_selected and method_selected)

    def show_page2(self):
        self.show_dynamic_button_widget_on_page2()
    
    def show_page1(self):
        self.stacked_widget.setCurrentWidget(self.page1)
        self.reset_button_colors()  # 페이지 전환 시 버튼 색상 초기화
        self.dynamicButtonWidget.remove_all_buttons()
        #with open('./gui/login/label_text.txt', 'r') as file:
        #    content = file.read()
        #    USER_ID = content
        #    self.page1.login_id.setText(USER_ID)  # QLabel의 텍스트를 파일 내용으로 업데이트

                # 파일에서 텍스트 읽기
        with open('./gui/login/label_text.txt', 'r') as file:
            file_content = file.read()
            content = json.loads(file_content)

            #사용자 ID
            global global_user_id
            global_user_id = content["id"]
 
        # QLabel에 텍스트 설정
        self.page1.login_id.setText(global_user_id)
        #text = USER_ID
        #self.page1.login_id.setText(text)
        #print(text)

    def show_page3(self):
        self.publish_selection()
        self.stacked_widget.setCurrentWidget(self.page3)
        self.timer_1.start(1000)  # 1초 후에 show_page4 호출

    def show_page4(self):
        self.stacked_widget.setCurrentWidget(self.page4)
        self.timer_2.start(5000)

    def show_page5(self):
        self.stacked_widget.setCurrentWidget(self.page5)


    def show_game_page(self):
        self.page1.close()
        self.game_page = Game()

        # 게임 완료 후 첫페이지로 돌아 올때 랭킹 갱신 
        self.game_page.game_rank_change.connect(self.game_rank_view)
        self.game_page.game_rank_change.connect(self.test)

        self.stacked_widget.addWidget(self.game_page)  # 게임 시작 페이지
        self.stacked_widget.setCurrentWidget(self.game_page)

    def test(self):
        print("왜 안 눌리는가?")


    def show_rps_game_page(self):
        self.stacked_widget.setCurrentWidget(self.rps_game_page)

    def publish_selection(self):
        iceDict =  selectIceCreamDict()
        toppingDict = selectToppingDict()     
        
        toppings = []
        for t in self.topping_selected :
            # print(str(toppingDict[t]))
            toppings.append(toppingDict[t])      

        # ROS2 메시지에 선택 상태를 설정하고 발행
        msg = UserOrder()
        msg.action = 'icecreaming'
        #msg.icecream = self.ice_cream_selected
        msg.icecream = iceDict[self.ice_cream_selected]
        #msg.topping = self.topping_selected
        msg.topping  =  toppings
 
        msg.topping_type = self.method_selected
        print(iceDict[self.ice_cream_selected])
        print(toppings)
        self.publisher.publish(msg)
        self.node.get_logger().info(f"Ice Cream: {self.ice_cream_selected}, Topping: {self.topping_selected}, Topping_type: {self.method_selected}")
        print('publish complete')

    
    def show_login_page(self):
        current_text = self.page1.log_in_button.text()  # 버튼 텍스트 읽기
        if current_text == "로그인":
            self.stacked_widget.addWidget(self.login_page)  #로그인 페이지
            self.stacked_widget.setCurrentWidget(self.login_page)
            self.login_page.login_button_change.connect(self.button_change)
            #self.toggle_login()
            #self.page1.log_in_button.setText("로그아웃")
        else :
            self.page1.log_in_button.setText("로그인")
            # QLabel에 텍스트 설정
            self.page1.login_id.setText("-")

    def button_change(self):
        self.page1.log_in_button.setText("로그아웃")


        #self.page1.deleteLater()  # 위젯을 삭제

    def update_state(self, msg):
        print(msg)

    def closeEvent(self, event):
        self.executor_thread.stop()
        self.robot_state_subscriber.destroy_node()
        rp.shutdown()
        event.accept()

    def open_new_window(self, class_name):
        #self.new_window = class_name
        # 창을 최대화된 상태로 표시
        self.new_window = class_name()
        self.new_window.showMaximized()
        

    def pinger_mouse_open(self, event=None):
        # Pinger_mouse 인스턴스 생성
        self.pinger_mouse = Pinger_mouse()
        self.page1.layout().addWidget(self.pinger_mouse)

    def remove_specific_widget(self, layout, widget):
    #레이아웃에서 특정 위젯을 찾아서 삭제
        if layout.indexOf(widget) != -1:  # 위젯이 레이아웃에 존재하는지 확인
            layout.removeWidget(widget)  # 위젯을 레이아웃에서 제거
            widget.deleteLater()  # 위젯을 메모리에서 삭제

    def show_dynamic_button_widget_on_page2(self):
        """페이지 2에 동적 버튼을 새로 불러오기 전에 기존 버튼을 삭제하고 새로운 버튼을 생성"""
        
        # 기존의 버튼들을 모두 제거
        #self.remove_all_buttons()

        # 새로 DynamicButtonWidget을 생성
        self.dynamicButtonWidget = DynamicButtonWidget()
        self.dynamicButtonWidget.setObjectName('dynamicButtonWidget')  # objectName 설정

        # page2의 레이아웃에 위젯을 추가
        self.page2.layout().addWidget(self.dynamicButtonWidget)

        # 페이지를 스택 위젯에 표시
        self.stacked_widget.setCurrentWidget(self.page2)

        # 그룹별 버튼 설정
        self.ice_cream_buttons = self.dynamicButtonWidget.ice_button_buttons  # DynamicButtonWidget에서 생성한 버튼 리스트 참조
        self.topping_buttons = self.dynamicButtonWidget.topping
        self.method_buttons = self.dynamicButtonWidget.topping_type

        print(self.ice_cream_buttons)

        # 단일,다중 선택
        self.setup_button_group(self.ice_cream_buttons, "magenta", multi_select=False)
        self.setup_button_group(self.topping_buttons, "orange", multi_select=True)
        self.setup_button_group(self.method_buttons, "cyan", multi_select=False)

    #모든 동적 버튼 삭제하기
    def remove_all_buttons(self):
        # 버튼들을 관리할 리스트
        self.ice_button_buttons = []
        self.topping = []
        self.topping_type = []
        print("저장된 모든 버튼을 제거하고 레이아웃에서 삭제")
        for button in self.ice_button_buttons:
            self.page_layout.removeWidget(button)
            button.deleteLater()
        self.ice_button_buttons.clear()

        for button in self.topping:
            self.page_layout.removeWidget(button)
            button.deleteLater()
        self.topping.clear()

        for button in self.topping_type:
            self.page_layout.removeWidget(button)
            button.deleteLater()
        self.topping_type.clear()

    def load_text_from_file(self):
        try:
            # 파일에서 텍스트 읽기
            with open('./gui/login/label_text.txt', 'r') as file:
                file_content = file.read()
                content = json.loads(file_content)
                #사용자 코드
                global global_user_code
                global_user_code = content["userCode"]
                #사용자 ID
                global global_user_id
                global_user_id = content["id"]

                #관리자 여부
                global global_user_auth
                global_user_auth = content["auth"]
            # QLabel에 텍스트 설정
            self.page1.login_id.setText(global_user_id)
        
        except FileNotFoundError:
            self.page1.login_id.setText("File not found!")
        except Exception as e:
            self.page1.login_id.setText(f"Error: {str(e)}")

    def update_label(self, new_text):
        self.page1.login_id.setText(new_text)

    def update_label_from_file(self, path):
        # 파일이 변경되었을 때 호출되는 메서드
        with open('./gui/login/label_text.txt', 'r') as file:
            content = json.loads(file.read())           
            #사용자 코드
            global global_user_code
            global_user_code = content["userCode"]
            #사용자 ID
            global global_user_id
            global_user_id = content["id"]

            #관리자 여부
            global global_user_auth
            global_user_auth = content["auth"]
            
            self.page1.login_id.setText(global_user_id)  # QLabel의 텍스트를 파일 내용으로 업데이트




# 메인 함수 정의
def main(args=None):
    #rclpy.init(args=args)  # ROS 2 초기화

    # PyQt 애플리케이션 초기화
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()

    # PyQt 애플리케이션 실행
    sys.exit(app.exec_())

# 스크립트 실행 시 main() 함수 호출
if __name__ == "__main__":
    main()
    