'''
가위바위보 라이브러리 버전 확인
Name: mediapipe
Version: 0.10.11

Name: opencv-python
Version: 4.10.0.84

numpy
1.26.4
'''

import sys
import cv2
import random
import mediapipe as mp
from PyQt5 import uic
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import numpy as np

# Mediapipe 초기화
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Gesture recognition model setup
gesture = {
    0: 'fist', 1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five',
    6: 'six', 7: 'rock', 8: 'spiderman', 9: 'yeah', 10: 'ok',
}
rps_gesture = {0: 'Rock', 5: 'Paper', 9: 'Scissors'}

# Load gesture training data for KNN model
file = np.genfromtxt('./gui/game/data/gesture_train.csv', delimiter=',')
angle = file[:, :-1].astype(np.float32)
label = file[:, -1].astype(np.float32)
knn = cv2.ml.KNearest_create()
knn.train(angle, cv2.ml.ROW_SAMPLE, label)


class RpsGame(QMainWindow):
    game_finished = pyqtSignal(int)  # 점수를 보낼 시그널
    goto_main_page = pyqtSignal()  # 앞 페이지의 함수를 호출하기 위한 시그널
    

    def __init__(self):
        super().__init__()

        # 로그인 상태인지 확인 - 예시
        #self.login_state = 0 # 로그인 안함
        self.login_state = 1 # 로그인 함

        # 게임 상태 변수
        self.game_count = 0
        if self.login_state == 1:
            self.max_games = 10  # 로그인하면 연속 10게임
        else:
            self.max_games = 3 # 로그인 안하면 1게임만 진행
        self.win_count = 0

        # UI 파일 로드
        self.game_main = uic.loadUi("./gui/game/rps_game.ui", self)
        self.game_main.setStyleSheet("QMainWindow {background: 'white';}")


        #page1 logo 그림 표시
        self.pixmap = QPixmap()
        self.pixmap.load("./gui/main/image/logo_green.png")
        label_width = self.game_main.logo.width()
        label_height = self.game_main.logo.height()
        caled_pixmap = self.pixmap.scaled(label_width, label_height, Qt.KeepAspectRatio)
        self.game_main.logo.setPixmap(caled_pixmap)
        self.game_main.logo.resize(caled_pixmap.width(), self.pixmap.height())

        # 게임 결과를 저장할 리스트
        self.game_results = []

        # 카메라 캡처 설정
        self.cap = cv2.VideoCapture(0)
        self.cap.release()
        self.cap = cv2.VideoCapture(0)  # 첫 번째 카메라 사용 (0은 기본값)
        #if not self.cap.isOpened():
        #    print("Error: Camera could not be opened.")
        #    sys.exit()

        # MediaPipe 손 추적 모듈 설정
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.mp_drawing = mp.solutions.drawing_utils

        # QTimer를 사용해 비디오 피드를 주기적으로 업데이트
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # 30ms마다 업데이트
        
        # 뒤로 가는 버튼 연결
        self.game_main.back.clicked.connect(self.close)

        # 게임 시작 버튼 연결
        self.game_main.start_button.clicked.connect(self.start_game)

        # 카운트다운 타이머 연결
        self.countdown_timer = QTimer(self)
        self.countdown_timer.timeout.connect(self.update_countdown)
        
        # 카운트다운 초기값
        self.countdown_time = 3  # 3초 카운트다운
        self.game_main.time_count.setText("")  # time_count QLabel에 초기값 표시

        # 게임 시작 여부
        self.game_started = False
    '''
    def trigger_front_function(self):
        """앞 페이지로 시그널 송출"""
        self.goto_main_page.emit()
    '''
    def start_game(self):
        # 이미 게임이 시작되었으면 다시 시작하지 않도록 함
        #if self.game_started:
        #    return

        # 게임 시작 상태로 설정
        self.game_started = True

        # 카운트다운 시작
        self.countdown_time = 3  # 3초 카운트다운 초기화
        self.game_main.time_count.setText("가위")   # QLabel에 카운트다운 시간 표시
        self.countdown_timer.start(1000)  # 1초마다 카운트다운 업데이트 (1000ms)

        # 게임 시작 버튼 비활성화
        self.game_main.start_button.setEnabled(False)

    def update_countdown(self):
        # 카운트다운 타이머 업데이트
        if self.countdown_time > 0:
            self.countdown_time -= 1
            if self.countdown_time == 3:
                self.game_main.time_count.setText("가위")
            elif self.countdown_time ==2:
                self.game_main.time_count.setText("바위")
            elif  self.countdown_time ==1:
                self.game_main.time_count.setText("보")
            else:
                self.game_main.time_count.setText("")

        else:
            self.countdown_timer.stop()  # 카운트다운 종료
            self.start_game_logic()

    def start_game_logic(self):
        # 게임 시작 로직 (카운트다운 후)
        choices = ['바위', '보', '가위']
        computer_choice = []
        computer_choice = random.choice(choices)

        print(f"Computer's choice: {computer_choice}")

        # 실제 사용자 손 추적을 통해 선택을 받아올 예정
        user_choice = self.recognize_gesture()

        print(f"Your choice: {user_choice}")

        # 승자를 결정
        winner = self.determine_winner(user_choice, computer_choice)

        # 결과를 리스트에 저장 및 화면에 표시
        self.game_results.append({
            "user_choice": user_choice,
            "computer_choice": computer_choice,
            "winner": winner
        })

        #결과표에 게임 현황 보여주기
        i = self.game_count
        label = getattr(self.game_main, f'result_label_{i+1}')
        label.setText(f"{i+1}회")        
        label = getattr(self.game_main, f'you_{i+1}')
        label.setText(self.game_results[i]["user_choice"])
        label = getattr(self.game_main, f'com_{i+1}')
        label.setText(self.game_results[i]["computer_choice"])
        label = getattr(self.game_main, f'result_{i+1}')
        label.setText(self.game_results[i]["winner"])



        #self.game_main.you_1.setText("바위")
        print(self.game_results)

        # 결과를 QLabel에 표시
        #self.game_main.result.setText(f"Your choice: {user_choice}\nComputer's choice: {computer_choice}\nResult: {winner}")
        print(f"Game results: {self.game_results}")

        # 이기면 계속 게임 진행, 지면 게임 결과 보여주고 종료
        self.game_count += 1
        if self.game_count >= self.max_games:
            self.final_result(self.win_count)
            #self.show_final_result()
            self.game_count = 0  # 게임 카운트 초기화
            if self.login_state == 0:
                self.login_prompt()
        else:
            if self.game_results[i]["winner"] == '패배': # 게임에서 지면 점수 화면에 나오면서 종료, 이기면 계속 게임 진행
                self.final_result(self.win_count)
                if self.login_state == 0:
                    self.login_prompt()
            else:
                self.start_game()

    # 게임 종료 시 회원 가입 유도 알림창
    def login_prompt(self):
        # 알림창 생성
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("로그인")
        msg.setText("포인트 적립을 원하시면 로그인을 해주세요.")

        login_button = msg.addButton("로그인", QMessageBox.AcceptRole)
        close_button = msg.addButton("확인", QMessageBox.AcceptRole)

        login_button.clicked.connect(self.show_login_page)
        close_button = (self, QMessageBox.Ok )
        #QMessageBox.warning(self, "포인트 적립을 원하시면 회원 가입을 해주세요.", QMessageBox.Ok)
        msg.exec_()



    # 로그인 알림창에서 로그인 버튼 누를 경우 페이지 이동
    def show_login_page(self):
        print("로그인 페이지로 이동")

    # 게임 종료 시 결과창에 포인트 내용 표시         
    def final_result(self, count):
        #count = self.game_count -1
        if count > 0:
            score = count *10
        else :
            score = 0
        self.game_main.result.setText(f"{count}번 게임을 이겼습니다. 이번에 획득한 포인트는 {score} 입니다.")
                # 게임 끝났을 때 점수를 시그널로 전달
        self.game_finished.emit(score)
            # 점수 계산 : 연속 이긴 횟수 * 10점



    def determine_winner(self, user_choice, computer_choice):
        # 게임 승자 결정
        if user_choice == computer_choice:
            self.win_count += 1
            return '비김'  # 비김
        elif (user_choice == '바위' and computer_choice == '가위') or \
             (user_choice == '가위' and computer_choice == '보') or \
             (user_choice == '보' and computer_choice == '바위'):
            self.win_count += 1
            return '승리'  # 승리
        else:
            return '패배'  # 패배

    def recognize_gesture(self):
        # 카메라에서 프레임 캡처
        ret, img = self.cap.read()
        if not ret:
            return '바위'

        img = cv2.flip(img, 1)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # 손과 랜드마크 추적

        result = self.hands.process(img)
        if result.multi_hand_landmarks:
            for res in result.multi_hand_landmarks:
                joint = np.zeros((21, 3))
                for j, lm in enumerate(res.landmark):
                    joint[j] = [lm.x, lm.y, lm.z]

                # Compute angles between joints
                v1 = joint[[0,1,2,3,0,5,6,7,0,9,10,11,0,13,14,15,0,17,18,19],:]
                v2 = joint[[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],:]
                v = v2 - v1
                v = v / np.linalg.norm(v, axis=1)[:, np.newaxis]

                angle = np.arccos(np.einsum('nt,nt->n',
                    v[[0,1,2,4,5,6,8,9,10,12,13,14,16,17,18],:], 
                    v[[1,2,3,5,6,7,9,10,11,13,14,15,17,18,19],:]))
                angle = np.degrees(angle)

                # Inference gesture
                data = np.array([angle], dtype=np.float32)
                ret, results, neighbours, dist = knn.findNearest(data, 3)
                idx = int(results[0][0])

                if idx in rps_gesture.keys():
                    print("제 선택은요 =", idx)
                    if idx == 0:
                        return "바위"
                    elif idx == 5:
                        return "보"
                    elif idx == 9:
                        return "가위"
        self.game_main.result.setText("화면에 손이 보이도록 해주세요.")
        return '바위'  # Default choice if no gesture is detected

    def update_frame(self):
        # 카메라에서 프레임 캡처
        ret, frame = self.cap.read()
        if ret:
            
            # 좌우 반전 (1)
            frame = cv2.flip(frame, 1)
            # BGR에서 RGB로 변환 (MediaPipe는 RGB를 사용)
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # 이미지에서 손과 랜드마크를 추적
            results = self.hands.process(rgb_image)

            if results.multi_hand_landmarks:
                for landmarks in results.multi_hand_landmarks:
                    # 손의 랜드마크를 화면에 그림
                    self.mp_drawing.draw_landmarks(frame, landmarks, self.mp_hands.HAND_CONNECTIONS)

            # 다시 RGB로 변환하여 PyQt에서 사용
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qimg = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)

            # QLabel에 이미지 표시
            self.game_main.main_cam.setPixmap(QPixmap.fromImage(qimg))

    def show_final_result(self):
        # 두 게임이 끝난 후 전체 결과를 표시하는 메서드
        if len(self.game_results) == self.max_games:
            user_wins = sum(1 for result in self.game_results if result["winner"] == "승리")
            computer_wins = sum(1 for result in self.game_results if result["winner"] == "패배")
            draws = sum(1 for result in self.game_results if result["winner"] == "패배")

            final_message = f"Final Result:\nYou Win: {user_wins}\nComputer Wins: {computer_wins}\nDraws: {draws}"

            # 최종 결과를 QLabel에 표시
            self.game_main.result.setText(final_message)
            print(final_message)
            #str_list = str(self.game_results)
            #self.game_main.result.setText(str_list)



    #이전 페이지 버튼 누를 때
    def close(self):
        # 창을 닫을 때 카메라 해제
        self.cap.release()
        cv2.destroyAllWindows()
        #super().close()
        #self.stacked_widget.setCurrentWidget(self.game_main_page)
        self.goto_main_page.emit()
        #self.parent().setCurrentIndex(0)
        # QTimer 종료
        self.timer.stop()
        




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RpsGame()
    window.show()
    sys.exit(app.exec_())