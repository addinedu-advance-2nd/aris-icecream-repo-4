# 아이스크림 키오스크 
** 아리스 아이스크림 로봇을 이용해 아이스크림 주문 서비스를 제공하기 위한 키오스크 구현


## 주요 기능
- PyQT5를 사용한 GUI 개발
   - 아이스크림 선택, 토핑 선택, 토핑 방식 선택
   - 로그인, 회원 가입 기능
- OpenCV, MediaPipe로 손 추적 및 제스처 인식, 영상처리
   - 게임 기능 구현 - 가위바위보, 틱택토
- ROS2를 이용한 로봇 제어
   - 주문한 아이스크림 맞춤 제조
   - 관리자 페이지 - 로봇의 실시간 관절 각도, 온도 확인, CCTV 확인


## 주요 라이브러리
- mysql
- PyQt5 : Version 5.14.2
- OpenCV : Version 4.10.0.84
- MediaPipe : Version 0.10.11
- NumPy : Version 1.26.4


## 의존성 설치
- pip install mysql-connector-python
- pip install PyQt5==5.14.2
- pip install opencv-python==4.10.0.84
- pip install mediapipe==0.10.11
- pip install numpy==1.26.4


## 경로 설정
- export PYTHONPATH="${PYTHONPATH}:/home/<user>/Documents/GitHub/aris-repo-4"