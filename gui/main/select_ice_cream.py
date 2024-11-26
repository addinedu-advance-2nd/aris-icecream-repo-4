
import sys
from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QGroupBox
from PyQt5.QtGui import *


from database.gui.sales.salesConnect import *
from database.gui.inventory.inventoryConnect import *


class SelectIceCream(QtWidgets.QMainWindow): 

    def __init__(self):
        super().__init__()


        # 각 페이지 UI 파일 로드
        self.select_ice_cream = uic.loadUi("./gui/main/select_ice_cream_page.ui")
        self.page1 = uic.loadUi("./gui/main/main_page.ui")
        self.page3 = uic.loadUi("./gui/main/payment_information_page.ui")
        self.page4 = uic.loadUi("./gui/main/wait_page_page.ui")

        # 'back_button' 클릭 시 'show_page1' 함수 호출
        self.select_ice_cream.back_button.clicked.connect(self.show_page1)
        self.select_ice_cream.select_complete.clicked.connect(self.show_page3)

        
        # 스택 위젯 생성 및 중앙 위젯으로 설정
        self.stacked_widget = QtWidgets.QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)

        # 페이지를 스택 위젯에 추가
        self.stacked_widget.addWidget(self.select_ice_cream)  # 아이스크림 선택 페이지
        #self.stacked_widget.addWidget(self.page1)
        
         

        #주문 선택 버튼 비활성화
        self.select_ice_cream.select_complete.setEnabled(False)

        self.ice_cream_selected = None
        self.topping_selected = []
        self.method_selected = None

        # DynamicButtonWidget 인스턴스 생성
        self.dynamic_button_widget = DynamicButtonWidget()
        self.select_ice_cream.layout().addWidget(self.dynamic_button_widget)  # page2에 동적 버튼 위젯 추가

        # 그룹별 버튼 설정
        self.ice_cream_buttons = self.dynamic_button_widget.ice_button_buttons  # DynamicButtonWidget에서 생성한 버튼 리스트 참조
        self.topping_buttons = self.dynamic_button_widget.topping
        self.method_buttons = self.dynamic_button_widget.topping_type

        print("이것은", self.ice_cream_buttons)

        # 단일,다중 선택
        self.setup_button_group(self.ice_cream_buttons, "magenta", multi_select=False)
        self.setup_button_group(self.topping_buttons, "orange", multi_select=True)
        self.setup_button_group(self.method_buttons, "cyan", multi_select=False)

        self.timer_1 = QtCore.QTimer(self)
        self.timer_1.setSingleShot(True)
        self.timer_1.timeout.connect(self.show_page4)

        self.timer_2 = QtCore.QTimer(self)
        self.timer_2.setSingleShot(True)
        self.timer_2.timeout.connect(self.show_page4)


    def setup_button_group(self, buttons, selected_color, multi_select):
        for button in buttons:
            button.setStyleSheet("background-color: #ffffff; color: black;")
            button.clicked.connect(lambda _, btn=button: self.select_button(buttons, btn, selected_color, multi_select))

    def select_button(self, button_group, selected_button, color, multi_select):
        if not multi_select:
            for button in button_group:
                button.setStyleSheet("background-color: #ffffff; color: black;")
        
        current_color = selected_button.styleSheet()
        selected_button.setStyleSheet(
            f"background-color: lightgray; color: black;" if "background-color: " + color in current_color else f"background-color: {color}; color: black;"
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
                selected_button.setStyleSheet("background-color: #ffffff; color: black;")
            else:
                self.topping_selected.append(selected_button.text())
                selected_button.setStyleSheet("background-color: #b2d761; color: black;")
            # self.topping_selected = selected_button.text()    # 예: "초코볼"
        elif button_group == self.method_buttons:
            self.method_selected = selected_button.text()     # 예: "가운데"
        print(self.ice_cream_selected, self.topping_selected, self.method_selected)

    def reset_button_colors(self):
        # 모든 선택 버튼 색상 초기화 및 'select_complete' 비활성화
        for button in self.ice_cream_buttons + self.topping_buttons + self.method_buttons:
        #for button in self.ice_cream_buttons + self.method_buttons:
            button.setStyleSheet("background-color: #ffffff; color: black;")
        self.select_ice_cream.select_complete.setEnabled(False)
        self.ice_cream_selected = None
        self.topping_selected = []
        self.method_selected = None


    def check_selection_complete(self):
        # 모든 그룹의 선택 상태 확인
        ice_cream_selected = any(button.styleSheet() == "background-color: magenta; color: black;" for button in self.ice_cream_buttons)
        topping_selected = any(button.styleSheet() == "background-color: orange; color: black;" for button in self.topping_buttons)
        method_selected = any(button.styleSheet() == "background-color: cyan; color: black;" for button in self.method_buttons)

        # 모든 그룹이 선택되었을 때 'select_complete' 버튼 활성화
        self.select_ice_cream.select_complete.setEnabled(ice_cream_selected and topping_selected and method_selected)

    def show_page1(self):
        self.stacked_widget.setCurrentWidget(self.page1)
        self.reset_button_colors()  # 페이지 전환 시 버튼 색상 초기화
        self.select_ice_cream.update() 
        self.close()
        self.parent().setCurrentIndex(0)
        self.remove_all_buttons()


    def show_page3(self):
        #self.close()
        #self.parent().setCurrentIndex(0)
        #self.publish_selection()
        self.stacked_widget.setCurrentWidget(self.page3)
        self.timer_1.start(1000)  # 1초 후에 show_page4 호출
    
    def show_page4(self):
        self.stacked_widget.setCurrentWidget(self.page4)
        self.timer_2.start(5000)

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

    def remove_all_buttons(self):
        """저장된 모든 버튼을 제거하고 레이아웃에서 삭제"""
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


class DynamicButtonWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('DB에서 동적으로 버튼 생성')
        self.setGeometry(30, 150, 1700, 500)

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
            self.page_layout.addWidget(group_box)

        self.setLayout(self.page_layout)

    def remove_all_buttons(self):
        """저장된 모든 버튼을 제거하고 레이아웃에서 삭제"""
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


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = SelectIceCream()  # MainWindow에서 AdminPage로 수정
    window.show()
    sys.exit(app.exec_())