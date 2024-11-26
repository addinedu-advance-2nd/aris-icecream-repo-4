import sys
import cv2
import numpy as np
from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import mediapipe as mp
import random


class TttGame(QMainWindow):
    game_finished = pyqtSignal(int)  # 점수를 보낼 시그널
    goto_main_page = pyqtSignal()  # 앞 페이지의 함수를 호출하기 위한 시그널

    def __init__(self):
        super().__init__()

        # 로그인 상태인지 확인 - 예시
        #self.login_state = 0 # 로그인 안함
        self.login_state = 1  # 로그인 함

        # 게임 상태 변수
        self.game_count = 0

        #로그인 확인 후 
        if self.login_state == 1:
            self.max_games = 10  # 로그인하면 연속 10게임
        else:
            self.max_games = 3  # 로그인 안하면 3게임만 진행
        self.win_count = 0

        # 각 페이지 UI 파일 로드
        self.ttt_game = uic.loadUi("./gui/game/ttt_game.ui", self)
        self.ttt_game.setStyleSheet("QMainWindow {background: 'white';}")


        #page1 logo 그림 표시
        self.pixmap = QPixmap()
        self.pixmap.load("./gui/main/image/logo_green.png")
        label_width = self.ttt_game.logo.width()
        label_height = self.ttt_game.logo.height()
        caled_pixmap = self.pixmap.scaled(label_width, label_height, Qt.KeepAspectRatio)
        self.ttt_game.logo.setPixmap(caled_pixmap)
        self.ttt_game.logo.resize(caled_pixmap.width(), self.pixmap.height())

        # 게임 결과를 저장할 리스트
        self.game_results = []

        # 뒤로 가는 버튼 연결
        self.ttt_game.back.clicked.connect(self.close)

        # 게임 시작 버튼 연결
        self.ttt_game.start_button.clicked.connect(self.start_game)

        # 왼쪽 카메라 화면
        self.camera_label = QLabel(self)
        self.camera_label.setFixedSize(480, 380)  # 카메라 화면 크기 설정
        self.camera_label.move(100, 300)  # 카메라 화면을 (100, 100) 위치로 이동
        self.camera_label.setAlignment(Qt.AlignCenter)

        # UI 내의 레이아웃에 카메라 화면 추가
        if hasattr(self.ttt_game, 'camera_layout'):  # 레이아웃이 존재하는지 확인
            self.ttt_game.camera_layout.addWidget(self.camera_label)
        else:
            print("Error: camera_layout not found in ttt_game.")



        # MediaPipe 손 추적 초기화
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
        self.mp_drawing = mp.solutions.drawing_utils

        # 카메라 시작
        self.cap = cv2.VideoCapture(0)
        self.cap.release()
        self.cap = cv2.VideoCapture(0)

        # QTimer로 카메라 화면 업데이트
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_camera_feed)
        self.timer.start(30)

        self.current_player = 1  # 사용자(O)가 먼저 시작
        self.game_started = False  # 게임 시작 여부 상태, 시작 버튼을 눌러야만 True로 변경됨

    def start_game(self):
        # 이미 게임이 시작되었거나, 최대 게임 수에 도달했으면 실행하지 않도록
        #if self.game_started or self.game_count >= self.max_games:
        if self.game_count >= self.max_games:
            return
        
            # 100ms 후 game_rank_re 호출
        QTimer.singleShot(1000, lambda: None)  # 1000ms 딜레이 후 실행
        # 게임 시작 상태로 설정
        self.game_started = True

        #최초 1회 버튼 설정
        if self.game_count == 0:

            # 게임 보드
            self.board_widget = self.ttt_game.findChild(QWidget, "game_board")
            if self.board_widget:
                board_layout = QGridLayout(self.board_widget)
                self.board_widget.setFixedSize(500, 500)  # 게임 보드 크기 설정
                self.board = np.zeros((3, 3), dtype=int)  # 3x3 보드 초기화 (0: 빈 칸, 1: X, -1: O)
                self.buttons = [[QPushButton("", self) for _ in range(3)] for _ in range(3)]

                # 게임 버튼 배치
                for i in range(3):
                    for j in range(3):
                        button = self.buttons[i][j]
                        button.setFixedSize(160, 160)  # 버튼 크기 설정
                        button.clicked.connect(lambda _, x=i, y=j: self.make_move(x, y))
                        button.setStyleSheet("""
                            QPushButton {
                                font-size: 70px;     /* 글자 크기 */
                                font-weight: bold;   /* 글자 굵기 */
                                color: white;        /* 글자 색상 */
                                background-color: limegreen; /* 버튼 배경색 */
                                border-radius: 30px; /* 모서리 둥글게 */
                                padding: 5px;        /* 여백 */
                            }
                            QPushButton:hover {
                                background-color: palegreen; /* 버튼 위에 마우스 올렸을 때 */
                            }
                            QPushButton:pressed {
                                background-color: palegreen;     /* 버튼 클릭 시 */
                            }
                        """)
                        board_layout.addWidget(button, i, j)

        # 게임 보드 초기화
        self.board = np.zeros((3, 3), dtype=int)
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].setText("")
                self.buttons[i][j].setEnabled(True)
        self.current_player = 1  # 사용자부터 시작

        # 시작 버튼 비활성화
        self.ttt_game.start_button.setEnabled(False)

        # 게임 카운트 증가
        self.game_count += 1

    def make_move(self, x, y):
        # 사용자 움직임 처리
        if self.board[x][y] == 0 and self.current_player == 1:
            self.board[x][y] = 1
            self.buttons[x][y].setText("O") # "X"
            self.buttons[x][y].setEnabled(False)
            if self.check_win(1):
                print("O 승리!")
                self.end_game(winner="O")
            elif not np.any(self.board == 0):  # 빈 칸이 없으면 무승부 처리
                print("It's a Draw!")
                self.end_game(winner="비김")
            else:
                self.current_player = -1
                QTimer.singleShot(500, self.computer_move)

    def computer_move(self):
        # 컴퓨터 움직임 처리
        empty_cells = [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == 0]
        if empty_cells:
            x, y = random.choice(empty_cells)
            self.board[x][y] = -1
            self.buttons[x][y].setText("X") # "O"
            self.buttons[x][y].setEnabled(False)
            if self.check_win(-1):
                print("X 승리!")
                self.end_game(winner="X")
            elif not np.any(self.board == 0):  # 빈 칸이 없으면 무승부 처리
                print("It's a Draw!")
                self.end_game(winner="비김")
            else:
                self.current_player = 1


    def check_win(self, player):
        # 승리 체크
        for row in range(3):
            if all(self.board[row, col] == player for col in range(3)):
                return True
        for col in range(3):
            if all(self.board[row, col] == player for row in range(3)):
                return True
        if all(self.board[i, i] == player for i in range(3)):
            return True
        if all(self.board[i, 2 - i] == player for i in range(3)):
            return True
        return False

    def end_game(self, winner=None):
        # 게임 종료 처리
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].setEnabled(False)

        # 게임 결과 저장
        self.game_results.append({
            "winner": winner
        })

        print(self.game_results)

        #결과표에 게임 현황 보여주기
        i = self.game_count
        print(self.game_count)
        label = getattr(self.ttt_game, f'result_label_{i}')
        label.setText(f"{i}회")        
        #label = getattr(self.game_main, f'you_{i+1}')
        #label.setText(self.game_results[i]["user_choice"])
        #label = getattr(self.game_main, f'com_{i+1}')
        #label.setText(self.game_results[i]["computer_choice"])
        label = getattr(self.ttt_game, f'result_{i}')
        if self.game_results[i-1]["winner"] == "O" :
            label.setText("승리")
        elif self.game_results[i-1]["winner"] == "X" :
            label.setText("패배")
        else :
            label.setText("비김")

        # 게임 종료 상태로 설정
        self.game_started = False

        # 게임 종료 후, 최대 게임 수에 도달하면 시작 버튼을 다시 활성화
        if self.game_count >= self.max_games or winner == "X":
            print("게임이 모두 끝났습니다.")
            
            # 시작 버튼을 활성화
            self.ttt_game.start_button.setEnabled(True)

            # 게임 시작 버튼 연결
            self.ttt_game.start_button.clicked.connect(self.start_game)

            # 게임 스코어 계산
            #score = self.game_count *10
            count = self.game_count - 1
            if count > 0:
                score = count *10
            else :
                score = 0
            self.ttt_game.result.setText(f"{count}번 게임을 이겼습니다. 이번에 획득한 포인트는 {score} 입니다.")

            # 게임 끝났을 때 점수를 시그널로 전달
            self.game_finished.emit(int(score))
            print("제 점수는요 " + str(score))

            # 게임 카운트 초기화
            self.game_count = 0

            
        else:
            # 다음 게임 준비
            QTimer.singleShot(1000, self.start_game)  # 1초 후에 게임 시작



    def update_camera_feed(self):
    # 카메라 화면 업데이트
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.flip(frame, 1)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # 색상 체계 변환 후 덮어쓰기
            
            # 게임판 그리기 (2개의 수평선, 2개의 수직선)
            height, width, _ = frame.shape
            cell_width = width // 3
            cell_height = height // 3

            # 수평선 그리기 (2개)
            cv2.line(frame, (0, cell_height), (width, cell_height), (0, 150, 0), 2)  # 위쪽 수평선
            cv2.line(frame, (0, 2 * cell_height), (width, 2 * cell_height), (0, 150, 0), 2)  # 아래쪽 수평선

            # 수직선 그리기 (2개)
            cv2.line(frame, (cell_width, 0), (cell_width, height), (0, 150, 0), 2)  # 왼쪽 수직선
            cv2.line(frame, (2 * cell_width, 0), (2 * cell_width, height), (0, 150, 0), 2)  # 오른쪽 수직선
            
            # 손 추적 결과 처리
            results = self.hands.process(frame)
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # 엄지, 검지, 새끼손가락 팁의 랜드마크 인덱스
                    thumb_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
                    index_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
                    pinky_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.PINKY_TIP]

                    # 엄지, 검지, 새끼손가락의 x, y, z 좌표를 가져와서 화면 크기에 맞게 변환
                    thumb_x, thumb_y, thumb_z = thumb_tip.x, thumb_tip.y, thumb_tip.z
                    index_x, index_y, index_z = index_tip.x, index_tip.y, index_tip.z
                    pinky_x, pinky_y, pinky_z = pinky_tip.x, pinky_tip.y, pinky_tip.z

                    # 엄지와 검지, 검지와 새끼손가락 사이의 거리 계산
                    distance_thumb_index = np.sqrt((index_x - thumb_x) ** 2 + (index_y - thumb_y) ** 2 + (index_z - thumb_z) ** 2)
                    distance_index_pinky = np.sqrt((pinky_x - index_x) ** 2 + (pinky_y - index_y) ** 2 + (pinky_z - index_z) ** 2)
                    print(distance_thumb_index, distance_index_pinky, thumb_x, thumb_y, thumb_z)

                    # 일정 거리 이하로 가까워지면 해당 칸에 클릭 효과를 내기
                    if distance_thumb_index < 0.04 and distance_index_pinky < 0.1:  # 거리 임계값을 0.04로 설정 (조정 가능)
                        # 클릭할 셀을 계산 (간격을 기준으로)
                        cell_x = int(index_x * width / cell_width)
                        cell_y = int(index_y * height / cell_height)

                        # 버튼이 클릭 가능한 상태라면 클릭 처리
                        if self.board[cell_y][cell_x] == 0:
                            self.make_move(cell_y, cell_x)

                    # 손 모양 그리기
                    self.mp_drawing.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

            
            # QImage로 변환
            bytes_per_line = 3 * width
            q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap(q_image)
            self.camera_label.setPixmap(pixmap)



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
    window = TttGame()
    window.show()
    sys.exit(app.exec_())
