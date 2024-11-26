import sys
import subprocess
import cv2
import numpy as np

from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal, QObject, QThread, QUrl, QTimer
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget

from database.gui.inventory.inventoryConnect import *

import rclpy as rp
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from robot_msgs.msg import RobotState



class RobotStateSubscriber(Node, QObject):
    msg_received = pyqtSignal(list)

    def __init__(self):
        Node.__init__(self, 'robot_state_subscriber_UI')
        QObject.__init__(self)

        self.subscription = self.create_subscription(RobotState, '/robot_state', self.robot_state_sub_callback, 10)
        self.subscription
    
    def robot_state_sub_callback(self, msg):
        angle_list = list(msg.angles)
        position_list = list(msg.temperatures)
        temperature_list = list(msg.temperatures)
        state_msg = [angle_list, position_list, temperature_list]
        self.msg_received.emit(state_msg)

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



class AdminPage(QtWidgets.QMainWindow):  # QMainWindow로 변경
    def __init__(self):
        super().__init__()

        #rp.init()
        self.executor_thread = Ros2ExecutorThread()
        self.executor_thread.robot_state_subscriber.msg_received.connect(self.update_robot_state)
        self.executor_thread.start()

        # UI 로드 및 스택 위젯 설정
        self.page5 = uic.loadUi("./gui/main/admin_page.ui")
        self.page1 = uic.loadUi("./gui/main/main_page.ui")

        # 스택 위젯 생성 및 중앙 위젯으로 설정
        self.stacked_widget = QtWidgets.QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)

        # 페이지를 스택 위젯에 추가
        self.stacked_widget.addWidget(self.page5)  # 관리자 페이지
        self.stacked_widget.addWidget(self.page1)

        # 창을 최대화된 상태로 표시
        self.showMaximized()

        # CCTV 설정
        # 웹캠 스트리밍 URL로 VideoCapture 객체 생성
        self.cap = cv2.VideoCapture('http://192.168.0.8:5757/stream')

        # 창 크기 설정
        self.resize(480, 360)  # 480x360 크기로 창 크기 설정

        # QLabel 크기 설정
        self.page5.cctv.resize(480, 360)  # 비디오를 표시할 QLabel의 크기 설정

        # 타이머 설정: 일정 간격마다 프레임을 캡처하고 표시
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # 30ms마다 프레임 업데이트 (약 30FPS)

        # 콤보박스 설정
        # 아이스크림
        ice_cream_list = selectIceCreamList()
        ice_cream_list.insert(0, " ")

        # 토핑
        topping_list = selectToppingList()
        topping_list.insert(0, " ")


        #ice_cream_list = (" ", "초코 아이스크림", "딸기 아이스크림", "바닐라 아이스크림", "품절")
        #topping_list = (" ", "초코", "캬라멜", "딸기", "품절")
        self.setup_combo_box(self.page5.ice_cream_combobox_1, ice_cream_list, "아이스크림 1")
        self.setup_combo_box(self.page5.ice_cream_combobox_2, ice_cream_list, "아이스크림 2")
        self.setup_combo_box(self.page5.ice_cream_combobox_3, ice_cream_list, "아이스크림 3")
        self.setup_combo_box(self.page5.topping_combobox_1, topping_list, "토핑 1")
        self.setup_combo_box(self.page5.topping_combobox_2, topping_list, "토핑 2")
        self.setup_combo_box(self.page5.topping_combobox_3, topping_list, "토핑 3")
        
        # 이미지 추가 (그래픽 뷰에 이미지 삽입)
        self.add_image_to_label("./gui/main/image/lite6.png", self.page5.lite6)

        # QLabel 딕셔너리 설정
        self.labels = {
            "J1_angle": self.page5.findChild(QtWidgets.QLabel, "J1_angle"),
            "J2_angle": self.page5.findChild(QtWidgets.QLabel, "J2_angle"),
            "J3_angle": self.page5.findChild(QtWidgets.QLabel, "J3_angle"),
            "J4_angle": self.page5.findChild(QtWidgets.QLabel, "J4_angle"),
            "J5_angle": self.page5.findChild(QtWidgets.QLabel, "J5_angle"),
            "J6_angle": self.page5.findChild(QtWidgets.QLabel, "J6_angle"),
        }

        self.temperature_labels = {
            "J1_temperature": self.page5.findChild(QtWidgets.QLabel, "J1_angle2"),
            "J2_temperature": self.page5.findChild(QtWidgets.QLabel, "J2_angle2"),
            "J3_temperature": self.page5.findChild(QtWidgets.QLabel, "J3_angle2"),
            "J4_temperature": self.page5.findChild(QtWidgets.QLabel, "J4_angle2"),
            "J5_temperature": self.page5.findChild(QtWidgets.QLabel, "J5_angle2"),
            "J6_temperature": self.page5.findChild(QtWidgets.QLabel, "J6_angle2"),
        }

        # data 딕셔너리를 사용하여 QLabel 업데이트
        data = {
            "J1": 10,
            "J2": 20,
            "J3": 30,
            "J4": 40,
            "J5": 50,
            "J6": 60
        }
        self.update_labels(data)

         # Close button 연결
        self.page5.admin_page_close_button.clicked.connect(self.close_with_data)
        
        # 재고 설정 리스트
        inventoryList = (selectInventoryIceList())
        print(inventoryList)
        inventoryToppingList = (selectInventoryToppingList())


        # 재고 표시 테이블
        self.inventory_table = self.findChild(QtWidgets.QTableWidget, "inventory_table")

        # 재고 가상 자료
        """
        row = self.inventory_table.rowCount()
        self.inventory_table.insertRow(row)        
        self.inventory_table.setItem(row, 0, QTableWidgetItem("딸기 아이스크림"))
        self.inventory_table.setItem(row, 1, QTableWidgetItem("12개"))
        self.inventory_table.setItem(row, 2, QTableWidgetItem("맛있다"))
        """
       #inventoryList = (selectInventoryList())
        for rowData in inventoryList :
            print(rowData)
            row = self.inventory_table.rowCount()            
            self.inventory_table.insertRow(row)   
            self.inventory_table.setItem(row, 0, QTableWidgetItem(str(rowData[1])))
            self.inventory_table.setItem(row, 1, QTableWidgetItem(str(rowData[2])))
            self.inventory_table.setItem(row, 2, QTableWidgetItem(str(rowData[3])))
            self.inventory_table.setItem(row, 3, QTableWidgetItem(str(rowData[4])))      
            self.inventory_table.setItem(row, 4, QTableWidgetItem(str(rowData[5])))      
    
            self.inventory_table.resizeColumnsToContents()


        #현재 재고 설정으로 아이스크림(콤보박스) 설정
        tmpIdx = 0       
        if(len(inventoryList)>0):
            for iceData in inventoryList:           
                if(tmpIdx==0):
                     self.page5.ice_cream_combobox_1.setCurrentText(str(iceData[1]))
                     self.page5.ice_cream_1_textEdit.setPlainText(str(iceData[2]))
                elif(tmpIdx==1):
                     self.page5.ice_cream_combobox_2.setCurrentText(str(iceData[1]))
                     self.page5.ice_cream_2_textEdit.setPlainText(str(iceData[2]))
                elif(tmpIdx==2):
                     self.page5.ice_cream_combobox_3.setCurrentText(str(iceData[1]))
                     self.page5.ice_cream_3_textEdit.setPlainText(str(iceData[2]))


                tmpIdx+=1
            
        #현재 재고 설정으로 토핑(콤보박스) 설정
        tmpIdx = 0       
        if(len(inventoryToppingList)>0):
            for toppingData in inventoryToppingList:           
                if(tmpIdx==0):
                     self.page5.topping_combobox_1.setCurrentText(str(toppingData[1]))
                elif(tmpIdx==1):
                     self.page5.topping_combobox_2.setCurrentText(str(toppingData[1]))
                elif(tmpIdx==2):
                     self.page5.topping_combobox_3.setCurrentText(str(toppingData[1]))

                tmpIdx+=1
                

                # 딕셔너리 초기화
        self.ice_cream_data = {}

        # QTextEdit 및 QPushButton 생성
        #self.ice_cream_1_textEdit = QTextEdit()
        #self.ice_cream_1_button = QPushButton("추가하기")

        
        # 버튼 클릭 시 이벤트 연결
        self.page5.ice_cream_1_button.clicked.connect(self.add_to_dict_1)
        self.page5.ice_cream_2_button.clicked.connect(self.add_to_dict_2)
        self.page5.ice_cream_3_button.clicked.connect(self.add_to_dict_3)


        # QProgressBar의 범위 설정
        self.page5.j1_angle_progressbar.setRange(-360, 360)  # 범위를 -180에서 180으로 변경
        self.page5.j2_angle_progressbar.setRange(-150, 150)
        self.page5.j3_angle_progressbar.setRange(-4, 301)
        self.page5.j4_angle_progressbar.setRange(-360, 360)
        self.page5.j5_angle_progressbar.setRange(-124, 124)
        self.page5.j6_angle_progressbar.setRange(-360, 360)

                # QProgressBar의 텍스트 형식을 실제 값으로 설정
        self.page5.j1_angle_progressbar.setFormat("%v")  # %v는 실제 값을 나타냄
        self.page5.j2_angle_progressbar.setFormat("%v")
        self.page5.j3_angle_progressbar.setFormat("%v")
        self.page5.j4_angle_progressbar.setFormat("%v")
        self.page5.j5_angle_progressbar.setFormat("%v")
        self.page5.j6_angle_progressbar.setFormat("%v")

        '''
        # 레이아웃 설정
        layout = QVBoxLayout()
        layout.addWidget(self.page5.ice_cream_1_textEdit)
        layout.addWidget(self.page5.ice_cream_1_button)

        # 중앙 위젯 설정
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        '''

    def update_frame(self):
        # 프레임을 캡처
        ret, frame = self.cap.read()
        if not ret:
            print("Failed to grab frame")
            return
        
        # OpenCV BGR 이미지를 RGB로 변환
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # 비디오 프레임 크기를 640x480으로 강제로 조정
        frame_resized = self.resize_frame(frame_rgb, 640, 480)
        
        # NumPy 배열을 QImage로 변환
        h, w, c = frame_resized.shape
        qimg = QImage(frame_resized.data, w, h, w * c, QImage.Format_RGB888)
        
        # QImage를 QPixmap으로 변환하여 QLabel에 설정
        pixmap = QPixmap.fromImage(qimg)

        # QLabel 크기에 맞게 비율을 유지하며 크기 조정
        pixmap = pixmap.scaled(self.page5.cctv.size(), aspectRatioMode=1)  # 비율 유지하며 크기 조정
        self.page5.cctv.setPixmap(pixmap)  # UI에서 QLabel에 비디오 출력

    def resize_frame(self, frame, target_width, target_height):
        # 비디오 프레임을 강제로 320x240으로 리사이즈
        return cv2.resize(frame, (target_width, target_height))

    def closeEvent(self, event):
        # 종료 시 VideoCapture 객체를 해제합니다.
        self.cap.release()
        event.accept()    
        


    def setup_combo_box(self, combo_box, items, combo_box_name):
        """콤보박스를 설정하고 선택된 항목 출력 연결"""
        combo_box.addItems(items)
        combo_box.currentTextChanged.connect(lambda: self.on_combo_box_change(combo_box, combo_box_name))

    def on_combo_box_change(self, combo_box, combo_box_name):
        """콤보박스에서 선택된 값 출력"""
        selected_menu = combo_box.currentText()
        #print(f"{combo_box_name}에서 선택된 메뉴는: {selected_menu}")
    
    def update_robot_state(self, state_msg):
        print(state_msg)
        angles = state_msg[0]
        positions = state_msg[1]
        temperatures = state_msg[2]

        self.page5.J1_angle.setText(str(angles[0]))
        self.page5.J2_angle.setText(str(angles[1]))
        self.page5.J3_angle.setText(str(angles[2]))
        self.page5.J4_angle.setText(str(angles[3]))
        self.page5.J5_angle.setText(str(angles[4]))
        self.page5.J6_angle.setText(str(angles[5]))

        self.page5.J1_angle_2.setText(str(temperatures[0])+"°C")
        self.page5.J2_angle_2.setText(str(temperatures[1])+"°C")
        self.page5.J3_angle_2.setText(str(temperatures[2])+"°C")
        self.page5.J4_angle_2.setText(str(temperatures[3])+"°C")
        self.page5.J5_angle_2.setText(str(temperatures[4])+"°C")
        self.page5.J6_angle_2.setText(str(temperatures[5])+"°C")

        #프로그래스바 값 입력
        #self.page5.j1_angle_progressbar.setValue(str(angles[0]))
        self.page5.j1_angle_progressbar.setValue(int(float(angles[0])))
        self.page5.j2_angle_progressbar.setValue(int(float(angles[1])))
        self.page5.j3_angle_progressbar.setValue(int(float(angles[2])))
        self.page5.j4_angle_progressbar.setValue(int(float(angles[3])))
        self.page5.j5_angle_progressbar.setValue(int(float(angles[4])))
        self.page5.j6_angle_progressbar.setValue(int(float(angles[5])))

            

    def update_labels(self, data):
        """data 딕셔너리의 값을 각 QLabel에 업데이트"""
        for joint, value in data.items():
            label_name = f"{joint}_angle"
            if label_name in self.labels and self.labels[label_name] is not None:
                self.labels[label_name].setText(str(value))

    def show_page5(self):
        """page5를 표시"""
        self.stacked_widget.setCurrentWidget(self.page5)

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


    def close_with_data(self):
    #콤보박스 선택 상태를 딕셔너리에 저장하고 출력한 후 창을 닫음
        combo_box_data = {
            "ice_cream_1": self.page5.ice_cream_combobox_1.currentText(),
            "ice_cream_2": self.page5.ice_cream_combobox_2.currentText(),
            "ice_cream_3": self.page5.ice_cream_combobox_3.currentText(),
            "topping_1": self.page5.topping_combobox_1.currentText(),
            "topping_2": self.page5.topping_combobox_2.currentText(),
            "topping_3": self.page5.topping_combobox_3.currentText(),
        }

        print("콤보박스 선택 상태:", combo_box_data)
        """ 재고 관리 데이터 저장 """
        """
        iceDict =  selectIceCreamDict()
        toppingDict = selectToppingDict()
        invertoryInfo = {}
        invertoryInfo['ice'] = "'{0}','{1}','{2}','{3}','{4}','{5}'".format(iceDict[combo_box_data['ice_cream_1']],10,iceDict[combo_box_data['ice_cream_2']],10,iceDict[combo_box_data['ice_cream_3']],10)
        invertoryInfo['topping'] = "'{0}','{1}','{2}'".format(toppingDict[combo_box_data['topping_1']],toppingDict[combo_box_data['topping_2']],toppingDict[combo_box_data['topping_3']])
        insertInventory(invertoryInfo)
        """

        """ 재고 관리 데이터 저장 """   
        if(combo_box_data['ice_cream_1'] == ' '
          and combo_box_data['ice_cream_2'] == ' ' and combo_box_data['ice_cream_3'] == ' '
          and combo_box_data['topping_1']== ' ' and combo_box_data['topping_2']== ' '  and combo_box_data['topping_3']== ' '
        ):
            print("재고관리를 설정하지 않았습니다.")
            QtWidgets.QMessageBox.information(self, '재고관리', '재고관리를 설정하지 않았습니다.')
            self.close()
            self.parent().setCurrentIndex(0)  
        else:
            iceDict =  selectIceCreamDict()
            toppingDict = selectToppingDict()
            invertoryInfo = {}

            """ 아이스크림 재고 설정 ( 맛, 수량 )"""
            iceMap = {}
            if combo_box_data['ice_cream_1'] != ' ' and self.page5.ice_cream_1_textEdit.toPlainText() != ' ':
                iceMap[iceDict[combo_box_data['ice_cream_1']]] = self.page5.ice_cream_1_textEdit.toPlainText()
            
            if combo_box_data['ice_cream_2'] != ' ' and self.page5.ice_cream_2_textEdit.toPlainText() != ' ':
                iceMap[iceDict[combo_box_data['ice_cream_2']]] = self.page5.ice_cream_2_textEdit.toPlainText()

            if combo_box_data['ice_cream_3'] != ' ' and self.page5.ice_cream_3_textEdit.toPlainText() != ' ':
                iceMap[iceDict[combo_box_data['ice_cream_3']]] = self.page5.ice_cream_3_textEdit.toPlainText()

            """ 토핑 재고 설정 ( 맛, 수량 )"""
            toopingSet = set()
            if combo_box_data['topping_1'] != ' ':                
                toopingSet.add(toppingDict[combo_box_data['topping_1']])
            if combo_box_data['topping_2'] != ' ':
                 toopingSet.add(toppingDict[combo_box_data['topping_2']])
            if combo_box_data['topping_3'] != ' ':
                 toopingSet.add(toppingDict[combo_box_data['topping_3']])

            """ 아이스크림 & 토핑 재고 설정 """            
            invertoryInfo['ice'] = iceMap
            invertoryInfo['topping'] =toopingSet
            
            insertInventory(invertoryInfo)
            self.close()
            self.parent().setCurrentIndex(1)
            #self.page5 = uic.loadUi("./gui/main/admin_page.ui")  

                    # 창을 닫을 때 카메라 해제
            self.cap.release()
            cv2.destroyAllWindows()

        '''
       # 창 닫기
        script_path = './gui/main/main.py'
        
        # subprocess를 사용하여 파이썬 스크립트 실행
        try:
            result = subprocess.run(['python3', script_path], check=True, capture_output=True, text=True)
            print(result.stdout)  # 실행 결과 출력
        except subprocess.CalledProcessError as e:
            print(f"Error occurred: {e}")
            print(f"stderr: {e.stderr}")        
        '''
        

    

    def add_to_dict_1(self):
        # QTextEdit에서 숫자 가져오기
        text = self.page5.ice_cream_1_textEdit.toPlainText()
        try:
            # 입력된 텍스트를 숫자로 변환
            value = int(text)
            # 딕셔너리에 추가 (예: 'ice_cream_1'이라는 키로)
            self.ice_cream_data['ice_cream_1'] = value
            print("딕셔너리에 추가된 값:", self.ice_cream_data)
        except ValueError:
            print("유효한 숫자를 입력하세요.")

    def add_to_dict_2(self):
        # QTextEdit에서 숫자 가져오기
        text = self.page5.ice_cream_2_textEdit.toPlainText()
        try:
            # 입력된 텍스트를 숫자로 변환
            value = int(text)
            # 딕셔너리에 추가 (예: 'ice_cream_1'이라는 키로)
            self.ice_cream_data['ice_cream_2'] = value
        except ValueError:
            print("유효한 숫자를 입력하세요.")

    def add_to_dict_3(self):
        # QTextEdit에서 숫자 가져오기
        text = self.page5.ice_cream_3_textEdit.toPlainText()
        try:
            # 입력된 텍스트를 숫자로 변환
            value = int(text)
            # 딕셔너리에 추가 (예: 'ice_cream_1'이라는 키로)
            self.ice_cream_data['ice_cream_3'] = value
            print("딕셔너리에 추가된 값:", self.ice_cream_data)
        except ValueError:
            print("유효한 숫자를 입력하세요.")



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = AdminPage()  # MainWindow에서 AdminPage로 수정
    window.show()
    sys.exit(app.exec_())
