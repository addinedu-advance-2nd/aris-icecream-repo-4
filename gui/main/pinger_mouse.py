import sys
import cv2
import mediapipe as mp
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt, QPoint, QTimer, pyqtSignal
from PyQt5 import QtWidgets, uic, QtGui, QtCore
import math

class Pinger_mouse(QWidget):
    # 페이지 전환을 요청하는 시그널 정의
    pageSwitchRequested = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Moving Circle")
        self.setGeometry(0, 0, 1920, 1080)

        # 첫 페이지 파일 로드
        #self.page1 = uic.loadUi("./gui/main/main_page.ui")
        
        # 모든 QPushButton 위젯을 리스트에 저장
        #self.buttons = self.page1.findChildren(QPushButton)
        #print(self.buttons)

        # Mediapipe 손 인식 초기화
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()
        self.capture = cv2.VideoCapture(0)

        # 초기 원의 위치
        self.circle_position = QPoint(400, 300)

        # 페이지와 버튼 리스트와 상태
        self.pages = []
        self.button_states = [False] * 5

        # 타이머 설정
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def update_frame(self):
        ret, frame = self.capture.read()
        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = self.hands.process(frame_rgb)

            if result.multi_hand_landmarks:
                for hand_landmarks in result.multi_hand_landmarks:
                    self.update_circle_position(hand_landmarks)

        self.check_button_collision()
        self.update()

    def update_circle_position(self, hand_landmarks):
        x = int(hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP].x * self.width())
        y = int(hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP].y * self.height())

        # X 좌표 반전
        x = self.width() - x
        
        self.circle_position = QPoint(x, y)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(QColor(255, 0, 0))
        painter.drawEllipse(self.circle_position.x() - 15, self.circle_position.y() - 15, 30, 30)

    def calculate_angle(self, a, b, c):
        # Calculate the angle ABC (in degrees) with points A, B, C
        ab = [a[0] - b[0], a[1] - b[1]]
        bc = [c[0] - b[0], c[1] - b[1]]
        dot_product = ab[0] * bc[0] + ab[1] * bc[1]
        magnitude_ab = math.sqrt(ab[0] ** 2 + ab[1] ** 2)
        magnitude_bc = math.sqrt(bc[0] ** 2 + bc[1] ** 2)
        angle = math.acos(dot_product / (magnitude_ab * magnitude_bc))
        return math.degrees(angle)

    def is_finger_bent(self, hand_landmarks):
        # Get the landmarks for the index finger
        base_joint = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_MCP]
        middle_joint = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_PIP]
        tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]

        # Convert landmarks to screen coordinates
        base = (int(base_joint.x * self.width()), int(base_joint.y * self.height()))
        middle = (int(middle_joint.x * self.width()), int(middle_joint.y * self.height()))
        tip = (int(tip.x * self.width()), int(tip.y * self.height()))

        # Calculate the angle at the middle joint
        angle = self.calculate_angle(base, middle, tip)
        return angle <= 90  # Return True if the angle is 90 degrees or less

    def check_button_collision(self):
        # 각 버튼과 원의 충돌 여부 확인
        for index, button in enumerate(self.buttons):
            button_rect = button.geometry()
            button_center = QPoint(button_rect.x() + button_rect.width() // 2, button_rect.y() + button_rect.height() // 2)
            distance = (button_center - self.circle_position).manhattanLength()

            # 원과 버튼이 접촉하고 손가락이 90도 이하로 구부러진 경우에만 클릭 처리
            if distance < 15 + button_rect.height() // 2 and self.is_finger_bent(self.hands.process(cv2.cvtColor(self.capture.read()[1], cv2.COLOR_BGR2RGB)).multi_hand_landmarks[0]):
                button.setStyleSheet("background-color: lightblue;")
                button.click()
                self.button_states[index] = True
                print("클릭")
                self.pageSwitchRequested.emit()
            else:
                button.setStyleSheet("")

    def button_clicked(self):
        button = self.sender()
        index = self.buttons.index(button)

        # 버튼 상태 토글
        self.button_states[index] = not self.button_states[index]

        if self.button_states[index]:
            print(f"{button.text()} activated")
        else:
            print(f"{button.text()} deactivated")

    def closeEvent(self, event):
        self.capture.release()
        event.accept()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Q:
            QApplication.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Pinger_mouse()
    window.show()
    sys.exit(app.exec_())
